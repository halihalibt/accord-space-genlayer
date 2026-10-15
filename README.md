# AccordSpace — Bounded Semantic Negotiation

Turn independently owned natural-language conditions into a shared finite feasible
space. When no plan satisfies every condition, compute all inclusion-minimal
conflict cores and correction sets with concrete witnesses. Only a condition's
owner can waive it. A plan commits only after every named participant approves
the same feasible assignment at the same revision.

**Status: Phase 1 deterministic reference core. Not deployed. No model calls,
GenVM execution, or onchain consensus has been tested.** There is no deployable
Intelligent Contract yet; the production adapter belongs to Phase 2.

## A concrete example

Three program coordinators agree on the domain: A, B and C each have a position
in `{0,1,2}`. They independently seal `A before B`, `B before C`, and `C before A`.
Every pair has a satisfying assignment; all three together have none. The core
finds the three-clause minimal conflict and three possible single-owner waivers.
It cannot execute any waiver for another person. If A's owner waives only their
condition, `(A=2, B=0, C=1)` is feasible and becomes binding protocol state only
after all three participants explicitly approve it.

This records a shared program plan, not proof that the real event occurred.
Participants do not edit a frontend world. The companion product is planned as
霁境 / Jijing: an ice-jade reading and negotiation space using an already approved
visual baseline. Repository B and its frontend have not been created in Phase 1.

## Run offline

Python 3.12; standard library only. From this directory:

```sh
python -m unittest discover -s tests -v
python -m scripts.check_phase1
python -m scripts.demo
```

The suite contains 24 tests, including an independent set-based oracle that
checks all 4,681 families of zero to four masks over a three-world universe.
Fixture ASTs enter an explicitly internal boundary; they are not AI results.
The demo is labelled `OFFLINE_DETERMINISTIC_FIXTURE`.

## What is different

The output is not an AI `consistent` label or a pairwise relation matrix. A
bounded compiler is planned to produce executable, typed predicates. Independent
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
`https://studio.genlayer.com/api`. The current workspace's read-only checks
returned HTTP 403, so current chain identity, SDK compatibility, latency and
faucet access are unverified. No alternative network is authorized.

See [protocol](docs/PROTOCOL_V1.md), [integration boundary](contracts/README.md),
[checkpoint](PROJECT_CHECKPOINT.md), and [stage rules](AGENTS.md). MIT licensed.
