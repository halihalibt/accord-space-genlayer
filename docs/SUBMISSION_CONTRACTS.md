# Intelligent Contracts submission draft

Status: NOT_READY_FOR_PORTAL — real Stable deployment/consensus/readback missing.

Name: AccordSpace — Bounded Semantic Negotiation

Repository: https://github.com/halihalibt/accord-space-genlayer

Description:

AccordSpace lets a small group freeze a finite planning domain and seal their
own natural-language conditions. Independent GenLayer executions compile each
condition into a typed predicate and compare its behavior over every declared
assignment. Deterministic code then finds all feasible plans and all
inclusion-minimal conflict/correction sets with concrete witnesses. Only a
condition's owner can waive it; any waiver invalidates existing approvals.
A plan commits only when every member approves the same world and revision.

GenLayer is used as a shared independent semantic boundary; the solver and
authorization rules stay deterministic. The public ABI accepts neither a
supplied AST nor a caller-selected result. UNKNOWN stops approval and cannot
be relaxed into a successful result.

Canonical source: contracts/accord_space.py (complete single file).

SHA256: 84eec53fc6d9ed0c1fc3fd30b50983dfacd1a6308ff016303840c055660e7d72

Offline evidence: 46 tests plus 36 SDK subtests, native lint and 10-method ABI.
Models are mocked in those tests. No real deployment or consensus is claimed.

Fill only from actual evidence before submitting:

- Stable deployed address: MISSING
- Deployment transaction and final receipt: MISSING
- Compilation MAJORITY_AGREE / successful execution: MISSING
- Final get_session readback and commitment: MISSING
- Public app visual/browser acceptance: PENDING

See DEPLOYMENT_RUNBOOK.md. Portal has not been submitted.

Deployment recovery: first attempt FINALIZED / ERROR / invalid_contract; header
corrected, awaiting a verified new deployment. NOT_READY_FOR_PORTAL.
