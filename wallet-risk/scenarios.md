# 筛查场景 Playbook

## 场景 A：OTC 收款前筛查对方地址

**输入**：对方地址 + 链（ETH/BSC/TRON/BTC/SOL…）
**参数建议**：`--deep`（首次交易对手必开）

| 步骤 | 查什么 | 怎么查 | 判读 |
|---|---|---|---|
| 1 | 地址合法性 | EVM `^0x[0-9a-fA-F]{40}$`；TRON base58check；BTC bech32/base58 | 非法直接拒，后续免查 |
| 2 | AML 标签/评分 | PublicAML enrich（score/level/label/资金来源/对手方） | score 高 / level=high → HIGH |
| 3 | 制裁命中 | 本地 OFAC SDN 名单精确匹配（定时拉取 treasury.gov） | 命中 = CRITICAL，流程终止 |
| 4 | 恶意标记 | GoPlus address_security（key 名以 fixture 为准） | sanctioned/money_laundering=1 → CRITICAL |
| 5 | 发行方黑名单 | ETH：USDT/USDC `isBlackListed`；TRON：USDT 合约；BSC 补齐 | 命中 = CRITICAL（币会被冻结） |
| 6 | 混币关联 | 已知池合约名单 + hop 分析（MistTrack） | 直连=HIGH，间接=MEDIUM；≠制裁 |
| 7 | 诈骗举报 | Chainabuse / eth-phishing-detect 本地名单 | 命中 → HIGH |

**决策**：任一 CRITICAL 拒收；HIGH 要求资金来源证明；全 LOW 以下放行并留档。

## 场景 B：交易所入金前自查

在场景 A 基础上加：

1. 入金 tx 专项：`--deposit-txid <hash>` 查该笔交易的对手方与上游路径。
2. 路径上有混币/高风险标签 → 先做"清洗说明"：准备 OTC 记录、收入证明、钱包签名归属证明。
3. 常见被卡原因：对手方是混币池直连地址、短时间内多跳归集、与被制裁地址同簇。
4. **预期管理**：筛查通过 ≠ 交易所放行；被风控后第一时间提交证明材料，不要多笔小额试探（会被判定为 structuring）。

## 场景 C：交互 DApp / 持有代币前检查

| 步骤 | 查什么 | 怎么查 |
|---|---|---|
| 1 | 无限授权 | 批量 `eth_call` 查 allowance，列出 spender 非白名单的无限授权 |
| 2 | 代币 honeypot | GoPlus token_security：honeypot、buy/sell tax、mintable、pausable、owner 权限 |
| 3 | 可升级/代理 | EIP-1967 implementation slot；proxy 字段 |
| 4 | 钓鱼标签 | eth-phishing-detect、ScamSniffer 名单 |
| 5 | 粉尘攻击 | 近期异常小额入账 + 其后 approve → 预警 |

**决策**：honeypot/恶意 spender 授权 = CRITICAL（不要交互）；高税/可 mint = HIGH（仓位控制）。

## 场景 D：定期钱包体检（建议每月）

1. 重跑场景 C 的授权检查，撤销不再用的无限授权。
2. 查持仓代币的 honeypot 状态（项目方可能后门升级）。
3. 查地址是否新上公开黑名单/举报库。
