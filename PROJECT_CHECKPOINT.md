# Phase 2 native candidate checkpoint — 2026-10-16 Asia/Shanghai

Repository A: https://github.com/halihalibt/accord-space-genlayer
Authoritative Phase 1 main: `93101a9079d6e7e0e911669d003cf0652602e559`.
Current work is a separate Phase 2 Draft PR candidate; main is preserved.

**Phase 2 offline SDK gate: PASS. Real Stable gate: NOT VERIFIED.**
No deployment, actual model call, chain write, wallet, Portal, Repository B or
frontend work occurred. The approved ice-jade visual assets remain unchanged.

## Complete source

`contracts/accord_space.py` is a complete single-file candidate, not a wrapper.
SHA256: `f99a6395f539c718027f2b6ab39801ccc22c2c0197fb7cbc27307b64563e886f`.
`SOURCE_PROVENANCE.json` records assembly inputs and the pinned official SDK.
The deterministic core remains unchanged from Phase 1.

The adapter derives identity from the runtime, uses actual SDK storage, and
installs compilation results only after native Leader/Validator execution.
Every Validator independently recompiles and compares each condition's entire
finite-domain behavior. No public AST/mask/result write exists. Text mode
preserves raw JSON for strict duplicate-key checking.

## Verified evidence

- Python 3.12.14; 54 actually resolved packages in requirements.lock.txt.
- Official GenVM v0.2.16 release SHA256 matched the published GitHub asset digest.
- 46 tests PASS: 24 deterministic and 22 SDK Direct Mode tests. One pure test
  includes 4,681 oracle families, not 4,681 separate test functions.
- Native lint PASS; SDK semantic validation PASS; actual ABI extraction PASS:
  6 writes, 4 views, 0 constructor parameters, no payable writes.
- Callback pickling checks enabled; no storage/self capture in callbacks.
- Exact generated-source assembly and phase guard PASS.

See evidence/phase2-tests.txt, phase2-lint.json, phase2-schema.json and
`docs/PHASE2_NATIVE_ADAPTER.md` for details and limits.

The official test framework auto-decodes text-mode JSON mocks; a documented
narrow test-only correction preserves registered raw text. It does not replace
SDK storage or model the network. Direct Mode's provisional Leader write is
explicitly restored with snapshot/revert in the rejection test. This is harness
recovery, not real consensus rollback evidence.

## Quota stopping point

The user reported 27% allowance and authorized autonomous progress with a chosen
pause. Stop after a verified remote Draft PR. Do not start an extended live-model
or network investigation. The actual current quota is not observable here.

Previous Stable read-only RPC attempts returned HTTP 403. This batch reused that
result rather than repeating it. Local SDK validation does not certify current
Stable runner compatibility, chain identity, model agreement, cost or finality.
No alternative network was used.

Resume from docs/NEXT_RESUME.md and the actual remote PR/head. Do not repeat
screening, history deduplication or SDK installation when the pinned cache exists.
No new routine approval is needed for authorized code work. This checkpoint is
not transaction authorization and contains no chain evidence.
