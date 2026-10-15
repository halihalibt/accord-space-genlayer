import copy
import itertools
import json
import unittest

from accord_space.core import (
    ProtocolError, MAX_WORLDS, approve, behavior, cancel, canonical, create,
    diagnose, domain, equivalent, install_accepted_compilation, parse_compilation,
    seal, state_hash, strict_json, validated_expr, waive, worlds,
)

A, B, C, X = ["0x" + c * 40 for c in "1234"]
SPEC = [{"id": k, "meaning": k + " event position", "values": [0, 1, 2]} for k in "abc"]


def cmp(op, a, b):
    return {"op": op, "left": {"var": a}, "right": {"var": b}}


def eq(k, v):
    return {"op": "eq", "left": {"var": k}, "right": {"lit": v}}


def ready(spec=SPEC, roster=None, clauses=None):
    roster = roster or [A, B, C]
    s = create("demo", roster, spec)
    for i, owner in enumerate(roster):
        s = seal(s, owner, (clauses or [["a before b"], ["b before c"], ["c before a"]])[i])
    return s


def artifact(s, expressions):
    return canonical({"input_hash": s["input_hash"], "rules": [
        {"clause_id": f"C{i}", "status": "COMPILED" if e is not None else "UNKNOWN", "expr": e}
        for i, e in enumerate(expressions)]})


def cycle():
    s = ready()
    return install_accepted_compilation(s, artifact(s, [cmp("lt", "a", "b"),
        cmp("lt", "b", "c"), cmp("lt", "c", "a")]))


class DomainTests(unittest.TestCase):
    def test_cartesian_complete_and_order_pinned(self):
        w = worlds(SPEC)
        self.assertEqual(len(w), 27)
        self.assertEqual(w[0], {"a": 0, "b": 0, "c": 0})
        self.assertEqual(w[-1], {"a": 2, "b": 2, "c": 2})
        self.assertEqual(len({canonical(x) for x in w}), 27)

    def test_domain_hard_bounds_and_scalar_types(self):
        bad = [[], SPEC + [SPEC[0]], [{**SPEC[0], "values": [0, False]}],
               [{**SPEC[0], "values": [1, 1]}], [{**SPEC[0], "values": [0.1, 0.2]}],
               [{**SPEC[0], "values": [0, 1001]}], [{**SPEC[0], "values": ["", "b"]}],
               [{**SPEC[0], "unknown": 1}], [{**SPEC[0], "id": "__import__"}],
               [{"id": k, "meaning": k, "values": [0, 1, 2, 3]} for k in "abcd"]]
        for value in bad:
            with self.subTest(value=value), self.assertRaises(ProtocolError):
                domain(value)
        self.assertEqual(len(worlds([{"id": k, "meaning": k,
                                    "values": [0, 1, 2, 3]} for k in "abc"])), MAX_WORLDS)

    def test_defensive_copy_and_typed_boolean(self):
        source = copy.deepcopy(SPEC)
        result = domain(source)
        source[0]["values"][0] = 99
        self.assertEqual(result[0]["values"][0], 0)
        spec = [{"id": "x", "meaning": "flag", "values": [False, True]}]
        self.assertEqual(behavior(eq("x", True), spec), 2)
        with self.assertRaises(ProtocolError):
            behavior(eq("x", 1), spec)

    def test_strict_json_rejects_duplicate_nonfinite_code_and_bad_shapes(self):
        for raw in ['{"x":1,"x":2}', '{"a":{"b":0,"b":1}}', '{"x":NaN}',
                    '{"x":Infinity}', '```json\n{}\n```', '__import__("os")',
                    'x' * 32769, 7]:
            with self.subTest(raw=str(raw)[:40]), self.assertRaises(ProtocolError):
                strict_json(raw)


class ASTTests(unittest.TestCase):
    def test_nonidentical_asts_full_domain_equivalent(self):
        p = cmp("lt", "a", "b")
        q = {"op": "not", "arg": cmp("le", "b", "a")}
        self.assertEqual(behavior(p, SPEC), behavior(q, SPEC))
        s = ready()
        self.assertTrue(equivalent(s, artifact(s, [p, p, p]), artifact(s, [q, p, q])))

    def test_boolean_composition(self):
        p = {"op": "or", "args": [eq("a", 0), eq("a", 1)]}
        q = {"op": "and", "args": [p, cmp("ne", "b", "c")]}
        expected = [i for i, w in enumerate(worlds(SPEC)) if w["a"] in (0, 1) and w["b"] != w["c"]]
        mask = behavior(q, SPEC)
        self.assertEqual([i for i in range(27) if mask & (1 << i)], expected)

    def test_unknown_operator_variables_arity_type_and_code(self):
        bad = ["True", {"op": "eval", "code": "1"}, cmp("lt", "a", "missing"),
               {"op": "or", "args": []}, {"op": "not", "arg": eq("a", 0), "extra": 1},
               {"op": "eq", "left": {"var": "a"}, "right": {"lit": "0"}},
               {"op": "eq", "left": {"var": "a"}, "right": {"lit": None}},
               {"op": "and", "args": [eq("a", 0)] * 9}]
        for value in bad:
            with self.subTest(value=value), self.assertRaises(ProtocolError):
                validated_expr(value, SPEC)
        strings = [{"id": "x", "meaning": "name", "values": ["a", "b"]}]
        with self.assertRaises(ProtocolError):
            behavior({"op": "lt", "left": {"var": "x"}, "right": {"lit": "a"}}, strings)

    def test_depth_node_and_cycle_bounds(self):
        deep = eq("a", 0)
        for _ in range(9):
            deep = {"op": "not", "arg": deep}
        wide = {"op": "and", "args": [
            {"op": "or", "args": [eq("a", 0)] * 8}] * 8}
        cyclic = {"op": "not"}
        cyclic["arg"] = cyclic
        for expr in (deep, wide, cyclic):
            with self.assertRaises(ProtocolError):
                behavior(expr, SPEC)

    def test_same_current_verdict_hides_material_future_disagreement(self):
        spec = [{"id": k, "meaning": k, "values": [0, 1]} for k in "ab"]
        s = ready(spec)
        p = artifact(s, [eq("a", 0), eq("a", 1), eq("b", 0)])
        q = artifact(s, [eq("a", 0), eq("a", 1), eq("b", 1)])
        a = install_accepted_compilation(s, p)
        b = install_accepted_compilation(s, q)
        self.assertEqual(a["diagnosis"]["feasible_mask"], b["diagnosis"]["feasible_mask"])
        self.assertFalse(equivalent(s, p, q))
        a = waive(a, A, "C0", state_hash(a))
        b = waive(b, A, "C0", state_hash(b))
        self.assertNotEqual(a["diagnosis"]["feasible_mask"], b["diagnosis"]["feasible_mask"])


class SolverTests(unittest.TestCase):
    def test_three_way_obstruction_with_pairwise_witnesses(self):
        s = cycle()
        self.assertEqual(s["status"], "BLOCKED")
        self.assertEqual(s["diagnosis"]["minimal_cores"][0]["members"], [0, 1, 2])
        for i, j in itertools.combinations(range(3), 2):
            self.assertTrue(s["masks"][i] & s["masks"][j])
        self.assertEqual(len(s["diagnosis"]["minimal_corrections"]), 3)
        for core in s["diagnosis"]["minimal_cores"]:
            for witness in core["deletion_witnesses"]:
                for i in set(core["members"]) - {witness["removed"]}:
                    self.assertTrue(s["masks"][i] & (1 << witness["world"]))

    def test_all_small_masks_against_independent_set_oracle(self):
        """4,681 families: all 0..4 clause families over a 3-world universe.
        Oracle uses Python sets, all proper subsets and definition, not the
        production bit intersection DP/immediate-predecessor implementation.
        """
        families = 0
        for n in range(5):
            subsets = [set(c) for r in range(n + 1) for c in itertools.combinations(range(n), r)]
            for masks in itertools.product(range(8), repeat=n):
                rows = [{w for w in range(3) if mask & (1 << w)} for mask in masks]

                def sat(ids):
                    return {w for w in range(3) if all(w in rows[i] for i in ids)}

                full = set(range(n))
                feasible = sat(full)
                cores = [ids for ids in subsets if not sat(ids) and
                         all(sat(j) for j in subsets if j < ids)]
                repairs = ([] if feasible else [ids for ids in subsets if sat(full - ids) and
                           all(not sat(full - j) for j in subsets if j < ids)])
                d = diagnose(list(masks), 3)
                self.assertEqual(d["world_ids"], sorted(feasible))
                self.assertEqual({tuple(sorted(x)) for x in cores},
                                 {tuple(x["members"]) for x in d["minimal_cores"]})
                self.assertEqual({tuple(sorted(x)) for x in repairs},
                                 {tuple(x["remove"]) for x in d["minimal_corrections"]})
                for core in d["minimal_cores"]:
                    for w in core["deletion_witnesses"]:
                        self.assertIn(w["world"], sat(set(core["members"]) - {w["removed"]}))
                for repair in d["minimal_corrections"]:
                    self.assertIn(repair["world"], sat(full - set(repair["remove"])))
                families += 1
        self.assertEqual(families, 4681)

    def test_single_impossible_clause_and_independent_multiple_cores(self):
        d = diagnose([0, 3], 2)
        self.assertEqual([x["members"] for x in d["minimal_cores"]], [[0]])
        self.assertEqual([x["remove"] for x in d["minimal_corrections"]], [[0]])
        d = diagnose([3, 12, 5, 10], 4)
        self.assertIn([0, 1], [x["members"] for x in d["minimal_cores"]])
        self.assertIn([2, 3], [x["members"] for x in d["minimal_cores"]])

    def test_empty_active_set_tautology_bounds_and_no_silent_clamp(self):
        self.assertEqual(diagnose([], 4)["world_ids"], [0, 1, 2, 3])
        d = diagnose([(1 << 64) - 1] * 8, 64)
        self.assertEqual(len(d["world_ids"]), 64)
        self.assertEqual(d["minimal_cores"], [])
        for masks, n in [([True], 1), ([-1], 3), ([8], 3), ([0] * 9, 1), ([0], True), ([], 65)]:
            with self.assertRaises(ProtocolError):
                diagnose(masks, n)


class LifecycleTests(unittest.TestCase):
    def test_roster_sealing_and_input_order_determinism(self):
        one = ready()
        two = create("demo", [A, B, C], SPEC)
        for owner, clause in [(C, "c before a"), (A, "a before b"), (B, "b before c")]:
            two = seal(two, owner, [clause])
        self.assertEqual(one["input_hash"], two["input_hash"])
        other = create("different", [A, B, C], SPEC)
        for owner, clause in [(C, "c before a"), (A, "a before b"), (B, "b before c")]:
            other = seal(other, owner, [clause])
        self.assertNotEqual(one["input_hash"], other["input_hash"])

    def test_reject_outsider_zero_duplicate_and_bad_seals(self):
        for roster in [[A, A], [A], [A, "0x" + "0" * 40], [A, "bad"]]:
            with self.assertRaises(ProtocolError):
                create("demo", roster, SPEC)
        s = create("demo", [A, B], SPEC)
        for sender, clauses in [(X, ["x"]), (A, []), (A, [" "]), (A, ["x", "x"]),
                                (A, ["x"] * 3), (A, ["x" * 481])]:
            before = copy.deepcopy(s)
            with self.assertRaises(ProtocolError):
                seal(s, sender, clauses)
            self.assertEqual(s, before)
        s = seal(s, A, ["x"])
        with self.assertRaises(ProtocolError):
            seal(s, A, ["changed"])

    def test_input_hash_covers_every_semantic_input(self):
        base = ready()
        variants = [ready(clauses=[["changed"], ["b before c"], ["c before a"]]),
                    ready(spec=[{**SPEC[0], "meaning": "different scope"}] + SPEC[1:]),
                    ready(spec=[{**SPEC[0], "values": [2, 1, 0]}] + SPEC[1:]),
                    ready(roster=[B, A, C])]
        for other in variants:
            self.assertNotEqual(base["input_hash"], other["input_hash"])

    def test_compilation_errors_atomic_and_never_unknown_fallback(self):
        s = ready()
        good = json.loads(artifact(s, [cmp("lt", "a", "b")] * 3))
        bads = []
        for mut in [lambda d: d.update(input_hash="wrong"),
                    lambda d: d["rules"].pop(),
                    lambda d: d["rules"][0].update(clause_id="C1"),
                    lambda d: d["rules"][0].update(status="ACCEPT"),
                    lambda d: d["rules"][0].update(status="UNKNOWN"),
                    lambda d: d["rules"][0].update(expr={"op": "eval"}),
                    lambda d: d.update(approved=True)]:
            bad = copy.deepcopy(good)
            mut(bad)
            bads.append(canonical(bad))
        bads += ["{broken", "null", "[]"]
        for raw in bads:
            before = copy.deepcopy(s)
            with self.subTest(raw=raw[:80]), self.assertRaises(ProtocolError):
                install_accepted_compilation(s, raw)
            self.assertEqual(s, before)

    def test_unknown_blocks_waive_approval_and_reinstallation(self):
        s = ready()
        s = install_accepted_compilation(s, artifact(s, [None, eq("a", 0), eq("a", 1)]))
        self.assertEqual(s["status"], "REVIEW_REQUIRED")
        for fn in [lambda: waive(s, A, "C0", state_hash(s)),
                   lambda: approve(s, A, 0, state_hash(s)),
                   lambda: install_accepted_compilation(s, "{}")]:
            with self.assertRaises(ProtocolError):
                fn()

    def test_only_owner_waives_and_remaining_ids_not_reindexed(self):
        s = cycle()
        with self.assertRaises(ProtocolError):
            waive(s, A, "C1", state_hash(s))
        s = waive(s, A, "C0", state_hash(s))
        self.assertEqual(s["status"], "FEASIBLE")
        self.assertEqual(s["waived"], [0])
        self.assertEqual(s["revision"], 1)
        with self.assertRaises(ProtocolError):
            waive(s, A, "C0", state_hash(s))
        with self.assertRaises(ProtocolError):
            waive(s, A, "C9", state_hash(s))

    def test_waiver_invalidates_all_old_approvals_and_stale_calls(self):
        s = ready()
        s = install_accepted_compilation(s, artifact(s, [eq("a", 0)] * 3))
        old = state_hash(s)
        s = approve(s, A, 0, old)
        s = waive(s, B, "C1", old)
        self.assertEqual(s["approvals"], {})
        with self.assertRaises(ProtocolError):
            approve(s, C, 0, old)
        with self.assertRaises(ProtocolError):
            waive(s, C, "C2", old)

    def test_all_members_same_plan_required_and_commit_terminal(self):
        s = cycle()
        s = waive(s, A, "C0", state_hash(s))
        ids = s["diagnosis"]["world_ids"]
        self.assertEqual(len(ids), 1)
        h = state_hash(s)
        for member in [A, B]:
            s = approve(s, member, ids[0], h)
            self.assertEqual(s["status"], "FEASIBLE")
        s = approve(s, C, ids[0], h)
        self.assertEqual(s["status"], "COMMITTED")
        self.assertEqual(s["committed"]["plan"], {"a": 2, "b": 0, "c": 1})
        for fn in [lambda: approve(s, A, ids[0], h), lambda: cancel(s, B),
                   lambda: waive(s, C, "C2", state_hash(s))]:
            with self.assertRaises(ProtocolError):
                fn()

    def test_different_choices_never_commit_and_own_choice_can_change(self):
        s = ready()
        s = install_accepted_compilation(s, artifact(s, [eq("a", 0)] * 3))
        h = state_hash(s)
        s = approve(s, A, 0, h)
        s = approve(s, B, 1, h)
        s = approve(s, C, 0, h)
        self.assertEqual(s["status"], "FEASIBLE")
        s = approve(s, B, 0, h)
        self.assertEqual(s["status"], "COMMITTED")

    def test_invalid_world_and_outsider_cannot_act(self):
        s = cycle()
        with self.assertRaises(ProtocolError):
            approve(s, A, 0, state_hash(s))
        s = waive(s, A, "C0", state_hash(s))
        for who, w in [(X, s["diagnosis"]["world_ids"][0]), (A, True), (A, -1), (A, 999), (A, 0)]:
            with self.assertRaises(ProtocolError):
                approve(s, who, w, state_hash(s))

    def test_cancel_from_every_nonfinal_phase(self):
        states = [create("demo", [A, B, C], SPEC), ready(), cycle()]
        unknown = ready()
        states.append(install_accepted_compilation(unknown, artifact(unknown, [None] * 3)))
        for s in states:
            old = copy.deepcopy(s)
            with self.assertRaises(ProtocolError):
                cancel(s, X)
            new = cancel(s, B)
            self.assertEqual(new["status"], "CANCELLED")
            self.assertEqual(s, old)
            with self.assertRaises(ProtocolError):
                cancel(new, B)


if __name__ == "__main__":
    unittest.main()
