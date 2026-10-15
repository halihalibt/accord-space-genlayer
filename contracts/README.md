# Complete native candidate source

`accord_space.py` contains the COMPLETE Phase 2 candidate: deterministic core,
frozen prompt and native SDK consensus/storage adapter. It has no local imports
and is assembled from the project's own inputs by `scripts/build_contract.py`.
Source provenance and exact SHA256 are recorded in `SOURCE_PROVENANCE.json`.

The native candidate passed local pinned-SDK semantic validation and mocked
Direct Mode tests. It has NOT been deployed or run with real models/validators;
current Stable compatibility remains unverified. Do not treat an offline pass
as deployment authorization or chain evidence.

`install_accepted_compilation` remains internal to the native accepted-result
path. There is no public AST/mask/result endpoint. See
`docs/PHASE2_NATIVE_ADAPTER.md` for the complete API and test limitations.

Future Repository B must copy this ENTIRE canonical file byte-for-byte, with
SHA256 and provenance, after the production version is frozen. No abbreviated
wrapper is acceptable. No Repository B exists in this batch.
