"""Validate the complete leading GenVM configuration, not just the first line."""
import json
from pathlib import Path

RUNNER = "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6"


def runner_config(source):
    lines = source.splitlines()
    header = []
    for line in lines:
        if not line.startswith("#"):
            break
        header.append(line[1:])
    if header and header[0].strip().startswith("v"):
        header = header[1:]
    result = json.loads("\n".join(header))
    if result != {"Depends": RUNNER}:
        raise ValueError("Unexpected pinned runner configuration")
    return result


if __name__ == "__main__":
    source = (Path(__file__).resolve().parents[1] / "contracts/accord_space.py").read_text()
    runner_config(source)
    print("RUNNER_HEADER_PASS: complete leading comment block is valid pinned JSON")
