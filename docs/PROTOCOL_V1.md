# ACCORD-SPACE-V1 — frozen Phase 1 design

## Trust and product contract

The users are small, preidentified teams that want a common approved program
plan without one coordinator owning everyone else's conditions or choosing an
AI interpretation unilaterally. A session freezes the roster and variable domain.
Each roster member's first seal both joins these terms and commits their own
conditions. Naming a wallet at creation is not evidence that its owner joined.
Nobody can compile a session until all named members seal.

The protocol's common object is the official approved plan. The contract must
refuse to commit a plan outside the accepted feasible domain, with somebody else's
condition silently waived, or with missing/stale participant approvals. Offchain
programs may read the final plan; enforcement is limited to protocol state. It
does not control a venue, calendar provider, delivery, or real-world behavior.

A normal backend remains appropriate if everyone already trusts its operator.
This design is for parties who choose a neutral, shared interpreter and want
independent clients to enforce the same constraints. Actual user adoption has
not been established through interviews; that remains a product risk.

## Exact bounded input

Session ID: ASCII `[A-Za-z0-9_-]{1,64}`. Roster: 2–4 distinct nonzero EVM
addresses, normalized to lowercase, ordered and immutable. Variable declarations
are ordered `{id,meaning,values}` records. ID matches `[a-z][a-z0-9_]{0,15}`;
meaning is 1–160 characters after outer trimming. There are 1–4 variables,
2–4 distinct values each, no more than 64 full Cartesian assignments. Values
are homogeneous per variable: bool, integer in [-1000,1000], or exact nonempty
strings up to 40 characters. No numeric/string coercion. Declaration and value
order fix the world index; the last variable changes fastest. This is the full
declared Cartesian domain, not a curated catalog of convenient candidates.

Each member seals 1–2 distinct conditions, 1–480 characters after outer trimming.
Conditions retain their text; no semantic deduplication. IDs C0…C(n-1) follow
roster order, then each member's original condition order, irrespective of which
wallet seals first. Identical text from different owners remains separate.

The input SHA256 binds protocol version, session ID, roster, variable meanings,
value order, and every condition with its ID and owner. Serialization is
UTF-8 JSON, sorted object keys, compact separators, `ensure_ascii=False`,
no NaN or Infinity. Array order is significant. This is not Keccak256.

## Compilation boundary — planned, not implemented in Phase 1

Leader compiles every natural-language condition against exactly this vocabulary
into a typed predicate, or returns `UNKNOWN` if unsupported, ambiguous, or needing
information outside the domain. It cannot invent variables or facts. If a
condition genuinely asserts something impossible in the declared domain, its
predicate can be false everywhere. A tautology may be true everywhere. `UNKNOWN`
is not equivalent to either. No repair of input meaning is attempted.

Artifact: exactly `{input_hash,rules}`. Rules in clause order are exactly
`{clause_id,status,expr}`, where status is COMPILED or UNKNOWN; UNKNOWN requires
`expr:null`. Strict JSON, at most 32,768 UTF-8 bytes, rejects duplicate keys,
code fences, nonfinite constants, invalid types and extra keys.

Expression grammar:

```text
operand := {"var": variable_id} | {"lit": typed_scalar}
predicate := {"op": "eq"|"ne"|"lt"|"le", "left": operand, "right": operand}
           | {"op":"not", "arg": predicate}
           | {"op":"and"|"or", "args": [2..8 predicates]}
```

Operands of a comparison have identical types. `lt`/`le` require integers.
Depth <=8 and total nodes <=64 per predicate, counting operands. The evaluator
never uses `eval`, dynamic imports, arithmetic, loops, calls, or raw Python.
Logical predicates are evaluated for every indexed world to form a bitmask.

Validators must independently compile from the sealed inputs without using the
Leader's candidate as their source of meaning. After validation, compare each
clause's status and FULL world mask exactly. Syntactically different predicates
are allowed when they have identical finite behavior. Never compare only the
whole-session feasible mask or MUS output; owner-specific future waivers can
expose masked discrepancies. No fuzzy prose comparison or voting on explanations.
Model errors, parse failures and failed consensus do not become UNKNOWN and
must not mutate application state. Phase 1's `equivalent` is only a deterministic
comparison utility; no real Leader or Validator has been run.

## Solver and proofs

For active constraint indices S, feasible worlds are the intersection of their
accepted masks. The empty conjunction is the complete declared domain.
`minimal_cores` enumerate ALL inclusion-minimal unsatisfiable active subsets;
for every member deletion a concrete satisfying world is provided.
`minimal_corrections` enumerate ALL inclusion-minimal removal subsets whose
complements are satisfiable, each with a concrete remaining-world witness.
Inclusion-minimal is not necessarily minimum cardinality or fairest. There is
no scalar repair ranking, automatic preferred owner, or automatic relaxation.

At 8 conditions, at most 256 subsets are checked with <=64-bit masks. Completeness
holds only for accepted formal predicates in the declared domain. It cannot prove
that natural language was interpreted correctly or that no real-world solution
exists outside the domain. The UI must say “no plan in this agreed domain.”

## State transitions and authorization

| State | Allowed transition | Consequence |
|---|---|---|
| COLLECTING | member `seal` once | own conditions immutable; all seals -> AWAITING_COMPILATION |
| AWAITING_COMPILATION | future permissionless `compile` | consensus output only -> FEASIBLE / BLOCKED / REVIEW_REQUIRED |
| FEASIBLE / BLOCKED | owner `waive(own_clause,expected_hash)` | irreversible waiver, revision+1, approvals cleared, deterministic re-solve |
| FEASIBLE | member `approve(world_id,expected_hash)` | sets only own choice; unanimous same world -> COMMITTED |
| Any nonfinal state | member `cancel` | CANCELLED, approvals cleared |
| COMMITTED / CANCELLED | no writes | terminal |

REVIEW_REQUIRED permits cancellation, not a new model roll or waiving an
uninterpreted condition. New text/domain requires a new, explicitly joined
session; no automatic recreation or retry. Cancel is free of asset consequences,
but any member can stop progress. There are no deadlines or timeouts in V1.

The state hash binds input hash, revision, all accepted masks, waived original
indices, and current status. It intentionally excludes participant approval
choices, so independently submitted approvals on the same constraint revision
can accumulate. An approval can be changed only by its signer before commitment.
Waiver invalidates ALL approvals, even when it does not change feasible worlds.
World IDs are zero-based exact integers; Python bool is rejected as an index.

The deterministic reference uses explicit sender parameters only to model future
runtime identity. The real adapter MUST obtain sender from `gl.message` and
never accept a caller-provided owner/sender parameter. Compilation installation
MUST be internal to the accepted nondeterministic path. Accepting ASTs or masks
from a public write would destroy the trust design and is prohibited.

## Frozen phase scope

Phase 1 implements data/AST validation, finite evaluator, semantic equivalence,
solver, witnesses, immutable-value transitions and their offline tests. No model
prompts, SDK adapter, network deployment, frontend, Repository B, wallet writes,
or Portal operations. Phase 2 will preserve this protocol and implement the
native SDK boundary, independent roles, error rollback and actual storage tests.
Current runner compatibility must be re-established on Stable; historical pins
are evidence references, not current environment certification.
