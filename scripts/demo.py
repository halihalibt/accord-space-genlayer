"""Offline fixtures only. Does not call a model, SDK, wallet, or RPC."""
import json
from accord_space.core import *

roster = ["0x" + n * 40 for n in "123"]
spec = [{"id": k, "meaning": f"Position of program {k}", "values": [0, 1, 2]} for k in "abc"]
s = create("jijing-gathering-001", roster, spec)
for owner, rule in zip(roster, ["A must precede B", "B must precede C", "C must precede A"]):
    s = seal(s, owner, [rule])
rules = [{"clause_id": f"C{i}", "status": "COMPILED", "expr": {
    "op": "lt", "left": {"var": a}, "right": {"var": b}}}
    for i, (a, b) in enumerate([("a", "b"), ("b", "c"), ("c", "a")])]
s = install_accepted_compilation(s, canonical({"input_hash": s["input_hash"], "rules": rules}))
trace = [{"step": "FIXTURE_COMPILATION", "state": s}]
s = waive(s, roster[0], "C0", state_hash(s))
trace.append({"step": "OWNER_WAIVES_OWN_CLAUSE", "state": s})
h = state_hash(s)
for owner in roster:
    s = approve(s, owner, s["diagnosis"]["world_ids"][0], h)
trace.append({"step": "ALL_MEMBERS_APPROVE_SAME_PLAN", "state": s})
print(json.dumps({"evidence_type": "OFFLINE_DETERMINISTIC_FIXTURE", "trace": trace},
                 ensure_ascii=False, sort_keys=True, indent=2))
