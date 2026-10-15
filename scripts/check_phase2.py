"""Check the complete single-file assembly and native security boundaries."""
import ast
from pathlib import Path
from scripts.build_contract import ROOT, assembled

source = (ROOT / "contracts/accord_space.py").read_text()
assert source == assembled(), "Canonical source drift"
tree = ast.parse(source)
contract = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "AccordSpace")
public = {n.name: n for n in contract.body if isinstance(n, ast.FunctionDef) and n.decorator_list}
assert set(public) == {"create_session", "seal_conditions", "compile_session", "waive_condition",
                       "approve_plan", "cancel_session", "get_session", "get_state_hash",
                       "list_sessions", "get_protocol"}
assert [a.arg for a in public["compile_session"].args.args] == ["self", "session_id"]
assert all(not any(a.arg in {"sender", "raw", "masks", "expr"} for a in n.args.args)
           for n in public.values())
compile_method = public["compile_session"]
nested = {n.name: n for n in compile_method.body if isinstance(n, ast.FunctionDef)}
assert set(nested) == {"leader_fn", "validator_fn"}
assert not any(isinstance(n, ast.Name) and n.id == "self"
               for fn in nested.values() for n in ast.walk(fn)), "Storage capture"
assert "independent_raw = leader_fn()" in source
assert 'response_format="text"' in source
for n in ast.walk(tree):
    if isinstance(n, ast.Call) and isinstance(n.func, ast.Name):
        assert n.func.id not in {"eval", "exec", "compile", "open", "__import__"}, "Dynamic code/I/O"
assert not (ROOT / "frontend").exists()
print("PHASE2_GUARD_PASS: exact full assembly, independent callback, no supplied-result ABI")
