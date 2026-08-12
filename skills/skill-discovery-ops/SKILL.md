---
name: skill-discovery-ops
description: 按需发现、评估并实装 AI 智能体技能（skills.sh 开放生态）。适用于用户说"有没有做 X 的技能 / 找技能 / 评估某个技能是否值得安装 / 安装技能 / 技能是否与现有能力重复或冲突 / 为运营配置技能 / 技能分析报告"。覆盖 find-skills/skills CLI 检索、质量三查（安装量/来源/star）、与 Codex 原生能力冲突排除、Node 与 CLI 前置检查、GitHub 镜像安装、双保险目录同步、实装验证与经验沉淀。
---

# Skill Discovery Ops

## Overview

从开放 agent 技能生态（skills.sh）按需发现技能、评估是否值得安装、实装并沉淀经验。核心理念：**先核实后安装、与原生能力冲突的不装、装完双保险同步并留痕**。

## 工作流

### 1. 理解需求

确认用户要解决的任务领域与具体场景（如「有没有小红书发布前审核的技能」→ 领域=小红书运营，任务=发布审核）。

### 2. 检索

- 先查 skills.sh 榜单确认知名技能（`https://skills.sh/`）；
- 再 `skills find <关键词> [--owner <作者>]` 检索（输出按安装量排序，含 skills.sh 链接）；
- 同一领域用多组关键词交叉检索（如平台名+中英文、功能词+场景词）。

### 3. 质量三查（未核实不推荐）

1. **安装量**：≥1K 优先，<100 谨慎；
2. **来源**：官方来源优先（vercel-labs/anthropics/microsoft/tavily-ai 等）；无名作者需额外核实；
3. **star**：来源仓库 <100 star 谨慎对待。

再用 GitHub API 读取 SKILL.md 源码核实真实能力与依赖（`api.github.com/repos/<owner>/<repo>/contents/<path>`，Accept: raw）。skills.sh 索引可能过期，**以源码存在性为准**。

### 4. 冲突排除（Codex 原生不装原则）

与 Codex 原生能力重复或不适用的不安装：

- 与内置工具重复（如网页搜索类技能与内置 search 重复）；
- 依赖其他 agent 专属机制（hooks/MCP/brew 等）或付费第三方 API；
- 配置对象非 Codex（如 Clawdbot/OpenClaw 专属配置）；
- 生态索引过期或路径为其他 agent 专用。

### 5. 实装

1. **前置检查**：skills CLI 要求 Node ≥22.20.0（`node --version` 核实；不满足先升级最新 LTS）；skills CLI 未装则 `npm install -g skills`；
2. **安装**：`skills add <owner/repo> --skill <名> -a codex -g -y`；
3. **GitHub 直连失败时**：`git clone` 走镜像（如 `https://ghfast.top/https://github.com/<owner>/<repo>.git`）到临时目录，再 `skills add <本地路径> --skill <名> -a codex -g -y`；
4. **双保险同步**：skills CLI 装到 `~\.agents\skills\`，复制副本到 `~/.codex/skills/`（Codex 实际加载目录）；
5. 读安装器安全评估（Gen/Socket/Snyk），Snyk Med 通常为 shell 执行通用提示，仍需人工复核行为。

### 6. 验证

- `skills list -g` 确认注册；
- 有外部 API 的技能实测端点可用性（如 hot-topics 的 60s API）；
- 检查 SKILL.md 完整性（frontmatter/正文/依赖）。

### 7. 记录沉淀

- 更新 Wiki 技能库实体页（`llm-wiki/entities/技能库.md`）技能清单与运营矩阵；
- 技能分析结论与实装经验写入 references 并留痕（任务总览 + log）；
- 产出可对外复用的分析报告/经验（如 GitHub 运营素材）。

## 资源

### references/analysis-template.md

技能分析报告模板：六维评估框架 + 逐项核实字段 + 可直接发布的 GitHub 素材文案结构。评估技能时读取。

### references/practice-notes.md

实装经验库：Node 升级、npm 缓存坑、GitHub 镜像安装、双保险同步、安全评估解读、真实案例（2026-08-12）。实装遇到问题时读取。
