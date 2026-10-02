# skills

钱多多团队自研 skill 资产库。可被任何智能体（Muse、Claude Code、Copilot CLI、OpenCode 等）读取使用。

## 给智能体：如何使用

1. **发现**：读 [`skills.json`](skills.json)——机器可读索引，含每个 skill 的名称、一句话描述、入口文件和完整文件清单。
2. **加载**：需要某个 skill 时，读取其目录下的 `SKILL.md`（入口），按其中指引再读配套知识文件。
3. **安装**（可选）：把整个 skill 目录复制到你自己的 skills 目录即可使用，无需改名。
4. **Skill 规范**：每个 skill 目录必含 `SKILL.md`，frontmatter 含 `name` 与 `description`；description 里的 Triggers/触发词用于意图匹配。

## Skill 清单

| Skill | 说明 |
|---|---|
| `team` | 团队调度框架：常设角色、第一原则（第一性原理 / 法无禁止即可为 / 效率导向）、派单协议 |
| `minfadian` | 中华人民共和国民法典知识库（7 编 1260 条）：法务助手 |
| `wallet-risk` | 加密货币钱包风险筛查：OTC 收款前 / 交易所入金前 / 交互 DApp 前 |
| `yingxiangli` | 西奥迪尼《影响力》七原则：说服、谈判、攻防 |
| `renxing-ruodian` | 卡耐基《人性的弱点》：与人相处、说服、批评的艺术 |
| `houheixue` | 李宗吾《厚黑学》（公版）：脸厚心黑心法、十二字真言、锯箭/补锅法、商战转译 |
| `guiguzi` | 《鬼谷子》（公版）：捭阖、揣情、飞箝、内楗，谈判话术与识人 |
| `sunzi` | 《孙子兵法》（公版）：庙算、诡道、虚实，竞争战略与商战转译 |

## 同步约定

- 本地 `~/workspace/skills/<name>/` 与本仓库保持同步；新增或大改 skill 时同步推送。
- 新增 skill 时同步更新 `skills.json` 索引。
- 内容均为原创提炼，不含受版权保护的完整正文或译文；公版书 skill 已在 SKILL.md 注明底本。

## 博客

配套实战教程见 [三色风博客](https://www.lxpyll.top)——《从 0 写出第一个 AI Skill》等系列文章，讲 skill 的写法、资产库搭建和多 agent 复用。
