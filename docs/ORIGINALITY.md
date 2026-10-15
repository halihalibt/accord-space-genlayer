# Design comparison and evidence boundary

This is a bounded engineering comparison, not a global novelty claim, patent
analysis, or prediction of Portal acceptance. Historical implementations are
comparison objects, not implementation sources. This core was written for the
current design and imports no prior project or competitor code.

| Neighbor | Substantive comparison |
|---|---|
| [Concord](https://github.com/Zhekinmaksim/genlayer-concord/blob/c37c43d205a2ea694ba89d4d3cc602501070714b/contract.py) | Fixed source read in full. Its model returns whole-set consistency and pairwise conflict bits; an inconsistent result exposes all statement indices. It does not install executable predicates, enumerate a finite domain, extract all minimal cores/corrections, or enforce owner-specific constraint waivers and unanimous plan commitment. A basic higher-order contradiction checker was rejected because of this neighbor. |
| [ClauseMesh](https://github.com/halihalibt/clausemesh-genlayer/blob/ba2b57059645d8ecbb5faf640472c10f1ca4b838/README.md) | Current README verified. A bilateral relation matrix does not encode complete feasible assignments or derive N-way cores and revision-safe execution. Pairwise compatibility cannot reconstruct the shared feasible space. |
| MAM / BriefProof | Prior fixed-source evidence reused. Evaluates an existing delivery against criteria. AccordSpace builds owner-specific executable functions over every declared world, then supports deterministic re-solving without another AI judgment. Relabeling a matrix alone would not satisfy this distinction. |
| PolicyDrift | Prior source reused for comparison: temporal semantic extraction and adopted baselines; not joint finite-domain negotiation or authorized constraint relaxation. |
| ContextPass | Reused prior scope summary: contextual coverage, access and revocation; not solving a shared set of predicates for a unanimously chosen assignment. |
| EIM / SCA | Prior summaries reused: source-dependency graph/max independent set and directed exchange cycles. Neither specifies the present constraint semantics, complete finite models, MUS/MCS witnesses or owner-held clause relaxation protocol. |
| [SemanticConstraint](https://github.com/GIFTEDLOV/semantic-constraint) / [Mandate](https://github.com/JspIIV/mandate) | README only. Both judge a particular candidate against criteria; no claim that their full current code was audited. Their README-described interfaces do not install the present multiowner feasible domain. |
| [Pantry Constellation](https://github.com/liwaw008-svg/pantry-constellation) | README only. Sequential acceptance of a dish against shared menu constraints and existing plates; different from full-domain executable predicates and owner-authorized relaxation. |
| [Agent Negotiator](https://github.com/Tunde505055555/Agent-Negotiator-) | README only. Marketplace proposal evaluation, counteroffers, agreement verification and challenges; no formal whole-domain solver/complete minimal correction enumeration described. |

Natural-language compilation and finite behavioral comparison are general
techniques, not unique to this project. Earlier candidate research identified
SourceTariffVM and PlanCast in that category; those earlier findings are reused,
not independently re-audited here. This session's GitHub repository searches
for `SourceTariffVM` and `SourceTariff in:readme` returned no results, which does
not invalidate earlier evidence or establish absence. Compared with the earlier
single-program/compiler design, this protocol's installed object is a vector of
separately owned conditions with a live feasible set. Every subsequent waiver,
conflict explanation and commitment must execute against it. This difference
requires solver and authorization/state changes, not just changing a prompt.
If Phase 2 reveals an existing implementation of this combined protocol, reopen
the gate before implementing a production adapter.

## Two discriminating cases

1. Three strict ordering conditions have nonempty pairwise intersections but an
empty triple intersection. The core provides the complete three-way minimal
conflict, a deletion witness for each condition, every minimal correction, and
permits only the relevant owner to execute a chosen waiver. A full-set AI
inconsistency label does not supply this machinery.
2. Predicates `[a=0,a=1,b=0]` and `[a=0,a=1,b=1]` both yield an empty current
feasible set. Treating them as equivalent would be unsafe: removing the first
owner's condition yields different feasible plans. Validation must preserve each
condition's entire behavior rather than the final label or current intersection.

Minimal unsatisfiable cores and correction sets are established CSP concepts:
[Liffiton and Sakallah](https://sun.iwu.edu/~mliffito/publications/jar_liffiton_CAMUS.pdf),
[IJCAI core/correction enumeration](https://www.ijcai.org/Proceedings/2018/188).
The contribution is a specific bounded semantic-consensus and authorization
protocol, not a new MUS algorithm. Translation fidelity and real-model agreement
remain unmeasured. Neutral, shared onchain rule enforcement is the intended
GenLayer role; see [official fit guidance](https://docs.genlayer.com/developers/intelligent-contracts/when-to-use-genlayer).
