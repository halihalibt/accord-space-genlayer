# 本地 / Studio 执行包 — 尚未部署

固定网络：Stable Studionet，61999 (`0xf22f`)，
https://studio.genlayer.com/api 。现金预算 0；只用 Faucet GEN。

当前没有签名账户、冻结交易范围、部署地址或真实 AI 共识记录。
本包不借用旧项目的交易授权，也没有后台签名器。

## 直接使用

1. 解压预构建交付包，Windows 双击 START_WINDOWS.cmd。需要 Python；
   也可访问已发布试玩。用本地 Chrome + OKX Wallet 打开真实会话。
2. 演练无需钱包。先完成三人固定教程，理解本人撤回与全员确认。
3. 钱包切到 Stable 61999，准备两个不同且可签名的账户 A/B，
   只使用 Faucet GEN。网页连接只读取账户，不会自行签名。
4. 真实模式中检查完整源码，逐字节 SHA256 必须为
   `f99a6395f539c718027f2b6ab39801ccc22c2c0197fb7cbc27307b64563e886f`。
5. 在本机设置本次签名请求上限，并逐笔核对钱包请求。
   失败也计入。账户/网络变化后重新设置；不自动重发。

## 最小真实冲突验收方案（供本人冻结范围，不自动执行）

推荐使用 2 人、1 个变量、两条互斥条件，最多 **8 次签名请求**。
每笔必须读取最终结果后继续；失败计入这 8 笔，不补发、不 Appeal。

| 次序 | 签名者 | 方法 | 参数 / 预期 |
|---|---|---|---|
| 1 | A | deploy | 完整冻结源码，构造参数为空 |
| 2 | A | create_session | 独特 ID，名单 [A,B]，下方范围 JSON |
| 3 | A | seal_conditions | `["夜间场必须启用，即 x 等于 1。"]` |
| 4 | B | seal_conditions | `["夜间场必须关闭，即 x 等于 0。"]` |
| 5 | A | compile_session | 应为 BLOCKED，保留各条规则及冲突见证 |
| 6 | B | waive_condition | C1 和最新 state_hash；应为 FEASIBLE |
| 7 | A | approve_plan | world_id=1 和最新 state_hash |
| 8 | B | approve_plan | world_id=1，同一约束版本；应为 COMMITTED |

范围 JSON：

```json
[{"id":"x","meaning":"是否启用夜间场","values":[0,1]}]
```

创建者必须是名单成员。A/B 必须各自封存，不能由一个钱包伪装两人。
每次切换账户后点连接并重新设置剩余范围；总量不能超过冻结的 8 笔。
前端的单次本地预算不能替代本人对跨账户总笔数的记录。

“仅可行方案”路线可用 7 笔（无撤回）：A 约束 x=1，B 约束
x 不等于 0。但它不覆盖冲突及撤回流程，不是推荐的完整验收。

## 如何判断每笔完成

收到 hash 不代表成功。手动点“查询一次”，保存原始返回与导出的记录。
必须同时保留：最终状态 FINALIZED、实际成功执行（常见字段
`txExecutionResultName=FINISHED_WITH_RETURN` / leader receipt 的 SUCCESS）、
MAJORITY_AGREE 或等价可核实共识字段、实际 get_session 最终读取。
字段必须按真实响应解释，缺字段就标缺证，不能自行补写。

部署地址从真实 receipt 中取得，复制到网页后核验链上完整源码。
部署后对 get_protocol / get_session 的读取才能确认 Stable runner
兼容性；本地 lint 或链 ID 查询不能替代它。

## 失败与不确定结果

出现错误立即停止写入；查看钱包历史与原交易。前端锁定待查询状态，
不自动重试。只有本人核查后才可解除锁定；解锁不会重发交易。
未知结果不能通过再次部署“试试看”。SOURCE_MISMATCH、UNKNOWN、
解析拒绝、共识分歧均应保留原始结果。新文本/新范围需要新会话，
不是对原交易 Retry。此时不要消耗剩余额度反复调查同一网络阻断。

如果前端无法连接，使用 https://studio.genlayer.com 的用户钱包签名流程
粘贴完整 contracts/accord_space.py；仍按同一方法与 8 笔范围逐笔执行。
Studio 可用性未在本轮认证，不得切换到其他网络。

## 发布与提交

Repository A（Intelligent Contracts）和 Repository B（Projects）的源码与
材料已准备。真实链上验收完成前，保持 NOT_READY_FOR_PORTAL 标记。
不要写已获批、已提交或链上验证通过。
