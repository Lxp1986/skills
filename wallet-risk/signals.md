# 信号维度 × 数据源矩阵

| 信号维度 | 数据源 | 成本 | 备注 |
|---|---|---|---|
| AML 评分/标签 | PublicAML enrich | 免费层 | score/level/label/资金来源/对手方 |
| 恶意地址 flag | GoPlus address_security | 免费 | 仅 EVM；**key 名以真实响应 fixture 为准** |
| 发行方黑名单 | 链上直读（USDT/USDC 合约） | 免费（RPC） | ETH/TRON/BSC；信任 RPC 节点假设 |
| OFAC 制裁名单 | treasury.gov SDN（本地拉取） | 免费 | 命中即 CRITICAL；定时更新 |
| 混币关联 | 静态池名单 + MistTrack | 免费/付费 | 区分暴露 vs 制裁命中 |
| 诈骗举报 | Chainabuse / eth-phishing-detect / ScamSniffer | 免费-付费 | 本地名单零成本优先 |
| 深度路径分析 | MistTrack（--deep） | 付费 key | hop 跳数、资金占比 |
| 代币安全 | GoPlus token_security | 免费 | honeypot/税/mint/代理 |
| 授权面 | 链上 eth_call 批量 | 免费（RPC） | 无限授权清单 |
| 行为画像 | 纯 RPC（nonce/余额/首笔） | 免费 | 零第三方依赖 |

## 能力路线图（按优先级）

**P0（先补的盲区）**
1. OFAC SDN 本地直查 —— 交易所风控最硬红线，不能只依赖 GoPlus。
2. 多链覆盖（Solana/Polygon/Arbitrum/Base/TON）—— 资金早就不只在 ETH/BSC/TRON。
3. Honeypot/貔貅盘检测 —— 散户最高频的真实损失场景。
4. 恶意 approve 检查 —— 钱包被盗主因之一，现有维度零覆盖。
5. 代理/可升级合约风险 —— 跑路前兆，与 honeypot 互补。

**P1**：跨链桥关联、免费诈骗标签聚合、粉尘攻击检测、地址行为画像、发行方黑名单补齐（BSC）。
**P2**：NFT 钓鱼、ENS 仿冒、持仓集中度、结果缓存（省付费配额）、多源评分归一化。

## 数据源选用原则

1. 免费本地名单优先（OFAC、eth-phishing-detect）：零成本、零隐私泄露。
2. 付费 API 只在 `--deep` / 高风险场景触发，并设配额开关。
3. 链上直读（黑名单、allowance）优于第三方转述，但要声明 RPC 信任假设。
4. 每个数据源失败时独立降级为 INCOMPLETE，不污染其他信号。
