# AccordSpace — Bounded Semantic Negotiation

AccordSpace turns independently owned natural-language conditions into a shared finite planning space. Each participant seals their own conditions; GenLayer independently compiles those conditions into typed predicates, while deterministic protocol code enumerates feasible worlds, minimal conflicts, and minimal corrections. A condition can only be relaxed by its owner, and a plan becomes committed only after every participant approves the same world at the same revision.

## Stable Studionet verification

The canonical Intelligent Contract is deployed on GenLayer Stable Studionet.

- Network: Stable Studionet
- Chain ID: 61999
- Contract: `0x0F4A3Aa94A55ef41e8f4108a1513c7a4cB8e1ffe`
- Canonical source: `contracts/accord_space.py`
- Canonical source SHA256: `84eec53fc6d9ed0c1fc3fd30b50983dfacd1a6308ff016303840c055660e7d72`
- Canonical source commit: `ceaef239fb4792bfb921f562cb94c1b472338be2`

The deployed contract and source were verified against the same canonical SHA256. The repository records the finalized deployment receipt and the complete end-to-end session evidence.

## Verified session

Session `jijing_20261016_1442` used two participants and one declared variable, `x ∈ {0,1}`, meaning whether the night scene is enabled.

The real session reached these protocol states:

1. Both participants sealed their own conditions.
2. GenLayer compilation finalized with majority agreement and successful execution, producing `BLOCKED · R0` because the conditions conflicted.
3. Participant B waived only their own condition (`C1`), after which the session finalized as `FEASIBLE · R1` with the unique feasible world `#1 / x=1`.
4. Participant A and participant B each finalized an approval for world `#1`.
5. The session reached `COMMITTED · R1` with `x=1`.

The recorded receipts are real Stable Studionet results. Offline fixtures are not presented as network evidence.

## What the contract demonstrates

- Finite-domain semantic compilation with independent consensus.
- Exact per-condition behavioral comparison over the complete declared domain.
- Exhaustive feasible-world enumeration within bounded limits.
- Inclusion-minimal conflict and correction witnesses.
- Owner-only condition relaxation.
- Revisioned approvals cleared by a waiver.
- Unanimous commitment to one exact feasible assignment.
- Strict rejection of malformed or uninterpreted semantic results.

The protocol is intentionally bounded. It does not claim to control real-world delivery, calendars, or external events; its guarantees apply to the declared formal domain and onchain protocol state.

## Engineering validation

The repository contains deterministic reference tests and pinned-SDK validation for the implementation. These are engineering checks; the finalized Stable Studionet receipts in `evidence/` are the separate source of real network evidence.

## Canonical source

`contracts/accord_space.py` is the complete single-file Intelligent Contract, not a wrapper or abbreviated excerpt. Repository B contains the same file byte-for-byte.

See `contracts/README.md`, `docs/PROTOCOL_V1.md`, `docs/ORIGINALITY.md`, `docs/SUBMISSION_CONTRACTS.md`, and `evidence/FINAL_E2E_20261016.json`.

MIT licensed.
