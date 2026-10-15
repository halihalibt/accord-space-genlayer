"""Fail if Phase 1 grows a model/network/deploy adapter or generated debris."""
import ast
from pathlib import Path

root = Path(__file__).resolve().parents[1]
core = root / "accord_space" / "core.py"
tree = ast.parse(core.read_text())
allowed = {"copy", "hashlib", "itertools", "json", "re"}
for node in ast.walk(tree):
    if isinstance(node, ast.Import):
        assert all(n.name in allowed for n in node.names), "Out-of-scope core import"
    elif isinstance(node, ast.ImportFrom):
        assert node.module in allowed, "Out-of-scope core import"
    elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        assert node.func.id not in {"eval", "exec", "compile", "__import__", "open"}, "Dynamic code/I/O"
assert not list((root / "contracts").glob("*.py")), "Phase 2 contract entered Phase 1"
assert not (root / "frontend").exists(), "Frontend is out of scope"
print("PHASE1_GUARD_PASS: deterministic-only core, no SDK/model/deploy/frontend path")
