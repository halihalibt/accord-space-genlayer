# Deployment header correction — 2026-10-16

## Recorded failure

The user's exported receipt records deployment transaction
`0x2035cc1f57f6ed01ee4aae5aa6d3448bc606a3bf300a5e0c95aca82e6ce4d470`
on Stable Studionet 61999 from `0x22Acaa233b7b985b36ef168f2de9295334065b15`.
Status FINALIZED; consensus MAJORITY_AGREE with five AGREE votes; execution
ERROR, result bytes `02 696e76616c69645f636f6e7472616374` (invalid_contract).
The receipt's proposed address is NOT evidence of successful deployment.
No usable deployment or real AI compilation has been established.

The supplied full source hashes to the previous frozen hash
`f99a6395f539c718027f2b6ab39801ccc22c2c0197fb7cbc27307b64563e886f`.
The local source therefore matches what the user signed.
Selected receipt fields and the original export hash are retained in
`evidence/deployment-failure-20261016.json`. No fresh RPC verification is claimed.

## Reproduced defect and correction

GenVM treats the contiguous leading comment block as runner configuration.
Our generated source appended `# v0.2.16` and the generation notice directly
after the JSON dependency. Parsing the whole block fails with JSON Extra data.
The dependency remains pinned to the exact same official runner. Replace the
misplaced version comment with a blank line so the configuration ends before
the generation notice. The runtime version remains pinned in source provenance.

Official specification:
https://sdk.genlayer.com/main/spec/02-execution-environment/04-runners.html

New complete canonical source SHA256:
`84eec53fc6d9ed0c1fc3fd30b50983dfacd1a6308ff016303840c055660e7d72`.
Python AST before/after is identical. Core, compiler prompt, adapter, ABI and
constructor arguments (empty) are unchanged. This is a packaging correction,
not an upgrade of an existing deployed instance.

The recorded error is generic and contains no detailed VM error. The malformed
header is a proven defect, but not proof that all future runtime gates pass.

## Validation

- Complete assembly and leading-comment JSON regression checks passed.
- 49 Python tests and 36 SDK subtests passed using pinned genlayer-test 0.29.2.
- Native linter 0.11.0 and SDK semantic/schema checks passed: six writes,
  four views, zero constructor parameters, pinned GenVM v0.2.16 bundle verified
  against SHA256 4f0b358ec98ec148be9b95cdfb0f0e1a6cbe64da0194fdfac3fffc6f5d1d93e2.
- Jijing has 22 passing assertion groups, including the actual error replay
  through its shipped app bundle: failure is visible in both languages and the
  remaining signing allowance becomes zero without another wallet send.
- Browser tests use synthetic DOM and stubbed canvas; no real GPU/audio claim.
- Automatic approval review blocked the full-source RPC schema request because
  explicit disclosure authorization to the external Studio endpoint was not
  recognized. The retained local request diagnostic is a proxy tunnel HTTP 403,
  with no schema response obtained. No workaround or alternate endpoint was used. Local SDK checks
  completed instead; Stable runner acceptance remains unverified.

## Recovery scope

One failed request has already been used. Under the user's subsequent maximum
execution authorization, prepare a fresh batch of at most eight wallet requests
for the corrected source: deploy + seven session operations. Including the
recorded failure this would be nine lifetime requests if all new steps succeed.
Failures still count. The browser default remains one request at a time; no
automatic retries, Appeal, alternative network or backend signer.
Only the user can confirm the actual OKX signatures. No recovery transaction
has been sent by this repair. Stop and inspect any failure or uncertain result.
Portal remains NOT_READY_FOR_PORTAL.
