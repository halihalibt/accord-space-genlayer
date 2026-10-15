"""Native SDK boundary appended by scripts/build_contract.py.

This file is an assembly input, not a standalone deployment source.
"""
from genlayer import Address, TreeMap, u64, gl


class AccordSpace(gl.Contract):
    sessions: TreeMap[str, str]
    session_ids: TreeMap[str, str]
    session_count: u64

    def __init__(self):
        self.session_count = u64(0)

    def _read(self, session_id: str) -> dict:
        if not (type(session_id) is str and re.fullmatch(r"[A-Za-z0-9_-]{1,64}", session_id)):
            raise gl.vm.UserError("BAD_ID")
        if session_id not in self.sessions:
            raise gl.vm.UserError("NO_SESSION")
        return json.loads(self.sessions[session_id])

    def _save(self, state: dict) -> None:
        self.sessions[state["id"]] = canonical(state)

    @gl.public.write
    def create_session(self, session_id: str, participants: list[Address], domain_json: str) -> None:
        try:
            # Direct Mode/ABI inputs may be raw 20-byte values; normalize through
            # the actual SDK Address constructor, never Python's bytes repr.
            state = create(session_id, [str(Address(a)) for a in participants], strict_json(domain_json))
            _member(state, str(gl.message.sender_address))
            require(session_id not in self.sessions, "SESSION_EXISTS")
        except ProtocolError as exc:
            raise gl.vm.UserError(str(exc))
        self._save(state)
        self.session_ids[str(int(self.session_count))] = session_id
        self.session_count = u64(int(self.session_count) + 1)

    @gl.public.write
    def seal_conditions(self, session_id: str, conditions: list[str]) -> None:
        try:
            state = seal(self._read(session_id), str(gl.message.sender_address), conditions)
        except ProtocolError as exc:
            raise gl.vm.UserError(str(exc))
        self._save(state)

    @gl.public.write
    def compile_session(self, session_id: str) -> None:
        snapshot = self._read(session_id)
        if snapshot["status"] != "AWAITING_COMPILATION":
            raise gl.vm.UserError("NOT_AWAITING_COMPILATION")
        # Only ordinary immutable strings cross into the nondeterministic block.
        # No self, storage proxy, wallet input or user-supplied candidate is used.
        snapshot_json = canonical(snapshot)
        prompt = build_prompt(snapshot)

        def leader_fn() -> str:
            # Text mode preserves raw JSON for duplicate-key/nonfinite checks.
            # SDK JSON mode predecodes to dict and loses duplicate-key evidence.
            raw = gl.nondet.exec_prompt(prompt, response_format="text")
            try:
                parse_compilation(json.loads(snapshot_json), raw)
                return canonical(strict_json(raw))
            except ProtocolError as exc:
                raise gl.vm.UserError("MODEL_ERROR:" + str(exc))

        def validator_fn(result) -> bool:
            if not isinstance(result, gl.vm.Return):
                return False
            try:
                independent_raw = leader_fn()
                return equivalent(json.loads(snapshot_json), result.calldata, independent_raw)
            except Exception:
                # Reject errors; never turn provider/parse/VM failure into UNKNOWN.
                return False

        accepted_raw = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)
        if canonical(self._read(session_id)) != snapshot_json:
            raise gl.vm.UserError("STATE_CHANGED")
        try:
            # This is internal and runs ONLY after the native consensus boundary.
            new_state = install_accepted_compilation(snapshot, accepted_raw)
        except ProtocolError as exc:
            raise gl.vm.UserError("MODEL_ERROR:" + str(exc))
        self._save(new_state)

    @gl.public.write
    def waive_condition(self, session_id: str, clause_id: str, expected_hash: str) -> None:
        try:
            state = waive(self._read(session_id), str(gl.message.sender_address), clause_id, expected_hash)
        except ProtocolError as exc:
            raise gl.vm.UserError(str(exc))
        self._save(state)

    @gl.public.write
    def approve_plan(self, session_id: str, world_id: int, expected_hash: str) -> None:
        try:
            state = approve(self._read(session_id), str(gl.message.sender_address), world_id, expected_hash)
        except ProtocolError as exc:
            raise gl.vm.UserError(str(exc))
        self._save(state)

    @gl.public.write
    def cancel_session(self, session_id: str) -> None:
        try:
            state = cancel(self._read(session_id), str(gl.message.sender_address))
        except ProtocolError as exc:
            raise gl.vm.UserError(str(exc))
        self._save(state)

    @gl.public.view
    def get_session(self, session_id: str) -> str:
        return canonical(self._read(session_id))

    @gl.public.view
    def get_state_hash(self, session_id: str) -> str:
        return state_hash(self._read(session_id))

    @gl.public.view
    def list_sessions(self, offset: int, limit: int) -> list[str]:
        if not (type(offset) is int and 0 <= offset <= int(self.session_count)
                and type(limit) is int and 1 <= limit <= 20):
            raise gl.vm.UserError("BAD_PAGE")
        return [self.session_ids[str(i)] for i in
                range(offset, min(offset + limit, int(self.session_count)))]

    @gl.public.view
    def get_protocol(self) -> str:
        return canonical({"protocol": PROTOCOL, "prompt_version": PROMPT_VERSION,
                          "max_worlds": MAX_WORLDS, "max_clauses": MAX_CLAUSES,
                          "network": "Stable Studionet", "chain_id": 61999})
