# Intelligent Contracts submission

Status: READY FOR PORTAL

## Name

**AccordSpace — Bounded Semantic Negotiation**

## Repository

https://github.com/halihalibt/accord-space-genlayer

## Description

AccordSpace lets independently owned natural-language conditions become a shared, finite planning space. Each participant seals their own conditions. GenLayer independently compiles those conditions into typed predicates and reaches consensus on their meaning; deterministic code then evaluates the complete declared domain, exposes minimal conflicts and corrections, and enforces owner-only relaxation. A final plan is committed only when every participant approves the same feasible assignment at the same revision.

The contract is intentionally bounded and explicit: it does not claim to enforce real-world events. Its job is to turn ambiguous human conditions into shared, inspectable protocol state.

## Canonical source

- File: `contracts/accord_space.py`
- SHA256: `84eec53fc6d9ed0c1fc3fd30b50983dfacd1a6308ff016303840c055660e7d72`
- Commit: `ceaef239fb4792bfb921f562cb94c1b472338be2`

## Stable Studionet deployment

- Network: Stable Studionet
- Chain ID: 61999
- Contract: `0x0F4A3Aa94A55ef41e8f4108a1513c7a4cB8e1ffe`
- Deployment transaction: `0x38396b6bdb9490404d8edb0c3da172e1317555675d6b408274de91c0cb97463b`
- Deployment receipt: FINALIZED / SUCCESS / MAJORITY_AGREE

## Real session evidence

Session `jijing_20261016_1442`

- `create_session`: `0x415551aa94660bd78a93188eaff50a238c1004b9703ab497055f6bf95f171080` — FINALIZED / SUCCESS / MAJORITY_AGREE
- `seal_conditions` A: `0xa7615e65ebcd737627e203d6ec79d6a88c42b23a4b10b5dfd8ff74c1bb3bf295` — FINALIZED / SUCCESS / MAJORITY_AGREE
- `seal_conditions` B: `0x405799fbb9d48b484c4ca557851b0cf35d09fbe3f1f05f2e9d68031decf87805` — FINALIZED / SUCCESS / MAJORITY_AGREE
- `compile_session`: `0x090edb124208ae9d8fa2fb1bcb93be81050d5c6cc725f1732d0bc45b7251ba4d` — FINALIZED / SUCCESS / MAJORITY_AGREE; 5 validators, 3 AGREE and 2 IDLE after quorum
- `waive_condition`: `0x7f6d91cd677e43ec4338fa6cacf3fe89602bb63eb9b496b507012c2be545168f` — FINALIZED / SUCCESS / MAJORITY_AGREE; participant B waived C1
- `approve_plan` A: `0xdd51da6d2b527c9713458cb6e1a47add815583202b9e2c9772da1ab485dfd2d6` — FINALIZED; world #1
- `approve_plan` B: `0x86a93c879ba66430f4305ff9d5a1fff5040e272ed5c81d5c817c9533254dacac` — FINALIZED; world #1

Final state: **COMMITTED · R1**, world **#1**, `x=1`.

## Evidence

The repository contains the complete canonical source, protocol specification, provenance, and recorded network evidence. Test fixtures are kept separate from the real Stable Studionet results.
