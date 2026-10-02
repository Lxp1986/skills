---
name: "site-maintenance"
description: "维护三色风博客（Lxp1986/Lxp1986.github.io，Hexo + Butterfly）：写新文章、配封面与插图、走发布流程。用于站点内容更新、改版、排障场景。"
---

# 站点维护 (Site Maintenance)

目标站点：**三色风** `https://www.lxpyll.top`
仓库：`Lxp1986/Lxp1986.github.io`，分支 `main`
技术栈：Hexo + Butterfly 主题，GitHub Actions 自动部署（push 到 main 即触发 `hexo clean && hexo generate`）

## 写新文章

文件位置：`source/_posts/<文件名>.md`，文件名用英文短横线命名，如 `ai-skill-first-tutorial.md`

Front-matter（照抄这个格式）：

```yaml
---
title: 文章标题
date: 2026-10-02 10:00:00
permalink: posts/2026/10/02/ai-skill-first-tutorial/
categories:
  - AI工具
tags:
  - AI Skill
  - 教程
description: 一句话摘要，140 字以内，会显示在列表页。
cover: /img/ai-skill-first-cover.svg
---
```

规则：
- `permalink` 必须唯一，格式 `posts/:year/:month/:day/:英文slug/`
- `categories` 用站内已有分类（AI工具、数码工具等），不要 invent 新分类除非用户要求
- `cover` 指向 `source/img/` 下已存在的文件
- `date` 用北京时间，格式 `YYYY-MM-DD HH:mm:ss`

## 配图规范（硬性）

- **全部透明背景**：封面和插图一律用手写 SVG，**不画全幅底色矩形**，外层保持透明
- 封面尺寸：`1200x620`，`viewBox="0 0 1200 620"`
- 风格：深色卡片 + 浅色文字，参考 `source/img/agent-trio-compare.svg`（卡片 `rx=14`，半透明填充 + 描边）
- 中文字体栈：`'PingFang SC','Hiragino Sans GB','Microsoft YaHei','Noto Sans CJK SC',sans-serif`
- 插图同理，尺寸按内容定，同样透明背景
- SVG 里不要内嵌 base64 图片，保持纯矢量

## 文笔（去 AI 味）

- 开头**先给结论**，一句话说清这篇能解决什么
- 第一人称"我"，写自己真实做过的事，带具体数字、名称、版本号
- 短句为主；不用"首先、其次、最后""值得一提的是""总而言之""在当今时代"
- 多用表格做对比，少用排比长句
- 事实部分注明核对日期和来源，感受部分明说"是我的判断"
- 站内相关文章互相链一下（`/posts/...` 相对路径）

## 发布流程

1. 写 `source/_posts/xxx.md`，配图放 `source/img/`
2. 本地能跑就 `npx hexo generate` 验证无报错（可选）
3. 经用户确认后 push 到 `main`（Contents API 或 git），Actions 自动部署
4. 回验：`curl -s -o /dev/null -w "%{http_code}" https://www.lxpyll.top/<permalink>`

**发布是公开动作**：写完先给用户看，确认后再 push。不要把草稿直接推上去。

## 派单（subagent briefing 模板）

- 角色：你是站点维护员
- 目标：完成指定的站点更新（写文章/改页面/修图），一句话
- 输入：用户原话、相关文件路径、图片要求
- 约束：遵守上文写作规范与配图规范；不确定的分类/链接先查站内现有文章；发布前必须经用户确认
- 输出契约：改了哪些文件、预览方式、待用户确认的事项
