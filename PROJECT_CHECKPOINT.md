# AccordSpace checkpoint — deployment header recovery

2026-10-16 Asia/Shanghai. See docs/DEPLOYMENT_HEADER_FIX.md for the recorded
failed transaction, reproduced defect, exact changes and validation limits.

Current canonical SHA256: `84eec53fc6d9ed0c1fc3fd30b50983dfacd1a6308ff016303840c055660e7d72`.
The previously reviewed mechanism and Python AST are unchanged. Only the
leading runtime configuration was separated from documentation by a blank line.
Assembly guard now validates the complete leading configuration block.

49 tests + 36 SDK subtests, native lint/semantic checks and ABI pass.
Source is copied byte-for-byte to Repository B. B now checks execution results
separately from finality/consensus and disarms the allowance on execution error.

Real status: one FINALIZED deployment with ERROR / invalid_contract; zero
successful deployments, zero real model compilations, zero Portal submissions.
Native SDK checks do not certify Stable network compatibility. Full-source RPC
preflight was blocked by automatic approval review; no workaround was attempted.

User authorized autonomous repair and continuation. New recovery scope: at most
8 wallet requests including corrected deployment, failures count, user signs;
original failed request remains recorded separately. Next step is one corrected
deployment, then verify execution/consensus/source/get_protocol before creating
any session. No automatic Retry/Appeal/resend. Stable 61999 only; cash zero.
