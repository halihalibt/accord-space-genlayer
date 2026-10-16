# ACCORD-SPACE-V1 — Protocol Specification

## Purpose

AccordSpace provides a neutral shared protocol for groups that need to turn independently owned natural-language conditions into one explicit plan inside a finite declared domain.

The protocol freezes the participant roster and domain, records each owner's conditions, obtains an independently agreed semantic compilation, solves the resulting formal constraints, and requires unanimous approval before commitment.

## Semantic compilation

Each condition is compiled into a typed predicate over the frozen vocabulary. The accepted artifact is compared by behavior over the complete Cartesian domain, not by prose similarity or only by the final aggregate feasibility result.

Independent compilation matters because two syntactically different predicates can be behaviorally equivalent, while two currently blocked compilations can become distinguishable after a later owner relaxation.

Model errors, parse failures, unsupported meaning, and failed consensus are not converted into successful results.

## Finite solver

For the active condition masks, feasible worlds are the intersection of all active masks. The protocol enumerates all inclusion-minimal conflict cores and all inclusion-minimal correction sets within the bounded domain, with concrete witnesses.

Current limits:

- 2–4 participants
- 1–2 conditions per participant
- up to 8 conditions
- 1–4 variables
- 2–4 values per variable
- at most 64 Cartesian worlds

## Authorization and revision

Only a condition's owner may waive that condition.

Every waiver increments the revision and clears prior approvals. A participant may approve only a feasible world at the current revision. Commitment requires every participant to approve the same exact world.

Once committed, the session is terminal.

## GenLayer boundary

The public contract obtains caller identity from the GenLayer runtime. The public ABI does not accept a caller-selected semantic result, AST, or mask.

The nondeterministic semantic compilation is isolated behind the GenLayer consensus boundary. Deterministic state transitions, authorization, hashing, solving, and commitment remain explicit protocol logic.

## Verification

The canonical implementation is deployed and exercised on Stable Studionet chain 61999. See `evidence/FINAL_E2E_20261016.json` for the recorded deployment and session evidence.

The protocol makes bounded guarantees only: it does not prove that natural language was interpreted correctly in every real-world context, and it does not enforce external events outside the declared domain.
