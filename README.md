# AccordSpace — Bounded Semantic Negotiation

Turn independently owned natural-language conditions into a shared finite feasible
space. When no plan satisfies every condition, compute all inclusion-minimal
conflict cores and correction sets with concrete witnesses. Only a condition's
owner can waive it. A plan commits only after every named participant approves
the same feasible assignment at the same revision.

**Status: Phase 2 native candidate, offline verification only. Not deployed.**
The complete single-file contract is in `contracts/accord_space.py`. Native SDK
semantic validation and mocked Direct Mode tests pass. No real models,
WebAssembly execution, or onchain consensus have been tested. See the
[native adapter report](docs/PHASE2_NATIVE_ADAPTER.md).

## A concrete example

Three program coordinators agree on the domain: A, B and C each have a position
in `{0,1,2}`. They independently seal `A before B`, `B before C`, and `C before A`.
Every pair has a satisfying assignment; all three together have none. The core
finds the three-clause minimal conflict and three possible single-owner waivers.
It cannot execute any waiver for another person. If A's owner waives only their
condition, `(A=2, B=0, C=1)` is feasible and becomes binding protocol state only
after all three participants explicitly approve it.

This records a shared program plan, not proof that the real event occurred.
Participants do not edit a frontend world. The companion product is [霁境 / Jijing](https://github.com/halihalibt/jijing-accordspace):
an ice-jade negotiation space preserving the approved original visual, with
a fixed tutorial and wallet client. Real chain E2E remains pending.

## Run offline

The deterministic core needs only Python 3.12's standard library. From this directory:

```sh
python -m unittest discover -s tests -v
python -m scripts.demo
```

The core suite contains 24 tests, including an independent set-based oracle that
checks all 4,681 families of zero to four masks over a three-world universe.
Fixture ASTs enter an explicitly internal boundary; they are not AI results.
The demo is labelled `OFFLINE_DETERMINISTIC_FIXTURE`. An additional 22 native
Direct Mode tests use the pinned official SDK and mocked model outputs; setup
and reproduction are in [the Phase 2 report](docs/PHASE2_NATIVE_ADAPTER.md).

## What is different

The output is not an AI `consistent` label or a pairwise relation matrix. A
bounded compiler produces executable, typed predicates. Independent
validators must compile separately and compare each predicate's complete behavior
over the frozen Cartesian domain. Deterministic code then solves and enforces
the shared constraint state, including later owner-authorized relaxations.

Different AST syntax may be equivalent. Equal *current aggregate* feasibility
is insufficient: two presently blocked compilations can allow different plans
after the same owner relaxes a condition. Per-clause full-domain agreement is
therefore a load-bearing validation rule, not a comparison of explanations.

Solvers and minimal unsatisfiable subsets are established techniques. This
project claims a particular protocol design, not invention of constraint solving
or global uniqueness. See [comparison](docs/ORIGINALITY.md).

## Boundaries

- 2–4 fixed participants, 1–2 conditions each, at most 8 total.
- 1–4 typed variables, 2–4 values each, at most 64 Cartesian assignments.
- Whitelisted comparisons and Boolean expressions; no arbitrary executable code.
- `UNKNOWN` blocks negotiation; malformed output is an error, never a result.
- Only the bounded formal model is exhaustively solved. Translation fidelity
  remains a semantic consensus problem and can be wrong even with consensus.
- All inputs are public. No assets, payouts, identity claims, scores or rewards.
- Every participant can cancel before commitment; inactivity can prevent progress.

Planned network is **Stable Studionet only**, chain ID **61999**,
`https://studio.genlayer.com/api`. The latest chain-ID read returned 61999 on 2026-10-15 UTC, while source-schema
preflight remained blocked by HTTP 403. Runner compatibility, model agreement,
latency and faucet access are unverified. No alternative network is authorized.

See [protocol](docs/PROTOCOL_V1.md), [integration boundary](contracts/README.md),
[checkpoint](PROJECT_CHECKPOINT.md), and [stage rules](AGENTS.md). MIT licensed.
