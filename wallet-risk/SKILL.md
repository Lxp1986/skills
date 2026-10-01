---
name: wallet-risk
description: "加密货币钱包风险筛查：查地址 AML 信号、制裁/黑名单、混币关联、恶意授权、貔貅盘等人为风险。覆盖 OTC 收款前、交易所入金前、交互 DApp 前三类筛查场景，含信号解读与数据源选用。Use when screening a crypto wallet address for risk, reviewing exchange deposit safety, or checking token approvals."
---

# 钱包风险筛查

目标：对一个钱包地址（或一笔入金交易）给出**风险信号清单 + 等级 + 行动建议**。结论永远是"筛查线索"不是"安全保证"——没有任何筛查能保证某家交易所一定接收。

## 风险等级

- **CRITICAL** — 制裁名单命中、发行方黑名单（USDT/USDC 冻结地址）、确认的混币/暗网资金直连。行动：拒绝交互，上报。
- **HIGH** — AML 高风险标签、混币间接关联（多跳内）、可疑诈骗举报。行动：要求资金来源证明，暂停。
- **MEDIUM** — 异常行为（粉尘攻击、异常授权）、新地址无历史。行动：加强审查。
- **LOW / CLEAN** — 无已知命中。注意：CLEAN ≠ 干净，只是"本次筛查未发现"。

## 筛查场景（按场景查，不要按数据源查）

### 场景 A：OTC 收款前筛查对方地址
1. 校验地址格式（EVM 正则 / BTC bech32 / TRON base58check），链别先定死，防跨链误判。
2. 查 AML 标签与风险分（PublicAML enrich / GoPlus address_security）。
3. 查制裁名单：**优先本地 OFAC SDN 直查**（免费公开名单，定时更新），不要只依赖第三方 flag。
4. 查混币关联：已知混币合约名单 + 跳数分析；区分"混币暴露"与"制裁命中"，前者是信号不是定罪。
5. 查发行方黑名单：ETH/USDT·USDC `isBlackListed`、TRON USDT 合约直读；BSC 同理补上。
6. 任一 CRITICAL → 拒收；HIGH → 要求对方提供资金来源证明后再定。

### 场景 B：交易所入金前自查
1. 先跑场景 A 全套。
2. 对入金 tx 做专项：查该笔交易的对手方与资金路径（MistTrack deposit 方向）。
3. 准备材料清单：资金来源证明（OTC 聊天记录、完税/收入证明）、钱包归属证明（签名验证）、路径说明。
4. 注意：筛查通过不等于交易所放行，交易所自有风控规则是独立的。

### 场景 C：交互 DApp / 持有代币前检查
1. 恶意 approve 检查：查目标地址对可疑 spender 的无限授权（`allowance` 批量读），参考 Revoke.cash 逻辑列出待撤销项。
2. 代币合约检查（GoPlus token_security）：honeypot、买卖税、mintable、可暂停、owner 权限、代理/可升级（EIP-1967）。
3. 诈骗标签：eth-phishing-detect、ScamSniffer 本地名单匹配。
4. 粉尘攻击：近期异常小额入账 + 其后 approve 交互 → 钓鱼前兆。

## 信号解读铁律

1. **多源交叉**：单一数据源的 HIGH 不定罪，两个独立源同时命中才升级。
2. **区分信号强度**：直连混币池 ≠ 多跳后间接接触 ≠ 同一交易所热钱包的普通对手方。
3. **fail-safe**：数据源失败时标 `INCOMPLETE`/`UNKNOWN`，绝不输出"干净"。
4. **时效性**：名单类信号（OFAC、黑名单）注明名单版本日期；静态名单要写更新节奏。

## 已知缺陷与规避（来自 crypto-risk-checker 实审）

- GoPlus 的 `sanctioned` 等 flag key 名若与真实 schema 不符，CRITICAL 会静默不可达：**用真实响应 fixture 锁定期望 key，未知 key 标 UNMAPPED 而不默认升级**。
- 发行方黑名单查的是公共 RPC 回应，隐含信任节点：高风险场景用自有节点或双 RPC 交叉验证，并在报告里声明该假设。
- 付费 API（MistTrack/Chainabuse deep 查询）无节流：明确标注计费触发条件，生产环境加显式开关与速率限制。

## Scope & Limits

- 本 skill 是筛查方法论，不替代持牌合规审查；大额/涉诉场景请走专业机构。
- 名单与 API schema 会变：实现时以各数据源官方文档为准，定期回归 fixture。
- 详细信号矩阵见 [signals.md](signals.md)，场景 playbook 见 [scenarios.md](scenarios.md)，速查见 [cheatsheet.md](cheatsheet.md)。
