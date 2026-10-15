# Production Intelligent Contract boundary

No deployable contract is provided in Phase 1. `accord_space/core.py` is the
deterministic reference implementation; it must not be uploaded to Studio as if
it were a finished Intelligent Contract.

Phase 2 must implement a complete native GenLayer adapter with real persistent
storage, runtime-derived sender identity, a permissionless compilation write,
independent Leader/Validator execution, and accepted-result-only state mutation.
`install_accepted_compilation` is an internal reference seam for offline fixtures,
never a public ABI endpoint. No public method may accept user-chosen masks or
pretend that input validation is semantic consensus.

The complete future canonical production source belongs in this directory. The
later Repository B must include its complete byte-identical copy and provenance
with SHA256, not a wrapper. There is no production source hash or deployed
contract address to report yet. SDK pins and adapter ABI remain unverified until
Stable access and runner compatibility are restored. Do not migrate networks.
