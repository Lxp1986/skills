# 速查 Cheatsheet

## 一句话决策

- 制裁/发行方黑名单命中 → **拒**（CRITICAL）
- 混币直连 / 高 AML 风险 → **停**（HIGH，要求证明）
- 可疑授权 / 新地址 → **查**（MEDIUM，加强审查）
- 无命中 → **放**（LOW，留档；≠保证干净）

## 地址格式速查

- EVM: `^0x[0-9a-fA-F]{40}$`
- TRON: base58check（T 开头，25 字节）
- BTC: bech32 / base58

## 免费数据源清单

OFAC SDN（treasury.gov）· eth-phishing-detect（GitHub）· ScamSniffer 名单 · GoPlus（address/token_security）· PublicAML enrich · 链上直读（isBlackListed / allowance / EIP-1967）

## 常见误报/漏报

- 混币暴露 ≠ 制裁命中（别把信号当定罪）
- GoPlus 未知 flag key 不要默认升级，标 UNMAPPED
- 公共 RPC 回应隐含信任节点假设
- 数据源失败 → INCOMPLETE，绝不报"干净"

## 计费触发点（防烧配额）

- `--deep` → MistTrack + Chainabuse 计费
- `--deposit-txid`（即使不带 --deep）→ MistTrack 计费
- 生产环境：显式开关 + 速率限制 + 结果缓存
