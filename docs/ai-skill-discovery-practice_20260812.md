# GitHub 运营素材：AI 智能体技能发现与实装实战（2026-08-12）

> 定位：GitHub 平台（asksky6718/edu-ai-skills 仓库方向）
> 人设：懂 AI 的职业教育架构师——「验证过才分享」
> 用途：仓库 README / 技术文章 / skill 包发布素材，可直接复制改写

---

## 一、本文素材速览

| 素材 | 内容 | 适用位置 |
|------|------|---------|
| 会话总结 | 一次完整的「技能发现→评估→实装→沉淀」闭环 | 文章开头/README 摘要 |
| 技能分析报告 | 六项技能六维评估 + 自媒体运营技能检索结论 | 文章正文/评估文档 |
| 实装经验 | 6 个真实踩坑与解法（含命令） | 文章正文/FAQ/经验贴 |
| 新技能 | skill-discovery-ops（技能发现与实装运维） | 仓库 skill 包/发布物 |

---

## 二、会话总结（闭环全景）

**一句话**：用 find-skills 技能发现器，完成了「找技能 → 评估 → 排除冲突 → 实装 → 验证 → 沉淀」的完整闭环，并为自媒体运营补齐了跨平台热搜与发布前审核两项能力。

**过程脉络**：

1. **评估选型**：GitHub 上三个 find-skills 候选（官方 vercel-labs/skills ⭐28.7K MIT 活跃 / WhizZest ⭐1 无 License / find-skills-x ⭐7），核实后只有官方实现值得装；
2. **生态澄清**：OpenClaw 生态（ClawHub）也有 find-skills 且是核心发现工具，但两套生态独立（`npx skills` vs `npx clawhub`），不冲突；
3. **安装执行**：Node 22.16 实测不满足 skills CLI 的硬性要求（≥22.20）→ 升级 Node 24 LTS → 遇到 npm 缓存损坏坑 → 改全局安装 skills CLI → find-skills 装好并双保险同步；
4. **六项技能评估**：tavily-search / summarize / skill-creator / memory-setup / self-improving-agent / code-simplifier 逐一核实，结论「1 可选、5 不装」；
5. **运营技能配置**：检索公众号/小红书/抖音/B站/知乎/头条等 9 组关键词，与本机已有技能对照后补装 2 项增量技能（跨平台实时热搜 + 小红书发布前审核）；
6. **经验沉淀**：方法论固化为一键可用的新技能（skill-discovery-ops），并同步到 Wiki 技能库。

---

## 三、技能分析报告（GitHub 文章正文素材）

### 3.1 六项技能评估结论（2026-08-12 实测）

| 技能 | 生态规模 | 结论 | 理由 |
|------|---------|------|------|
| tavily-search（实时联网） | 28.4K，Tavily 官方 | 不装 | 与 Codex 内置联网检索高度重复，且需 API key |
| summarize（万物可总结） | 22.7K，OpenClaw 官方 | 不装 | 依赖 brew 仅 macOS；会话总结现有能力可覆盖 |
| skill-creator（技能创建） | **348.9K**，Anthropic 官方 | 可选 | 含评估闭环方法论；本机已有系统版 |
| memory-setup（记忆配置） | 1.6K，OpenClaw 社区 | 不装 | 针对 Clawdbot 配置，与 Codex 无关；本机记忆体系已健全 |
| self-improving-agent（自我进化） | 32.9K | 不装 | hooks 为 Claude 机制，Codex 无原生支持；理念已实践 |
| code-simplifier（代码精简） | 1.7K（索引已过期） | 不装 | 源码核实多实现已下线，仅存版本为 Claude 专用路径 |

**方法论**：安装前六维核实——来源与规模、功能、依赖、本机现状、重复/冲突、结论。核心原则：**与原生能力冲突的不装；未核实源码的不推荐**。

### 3.2 自媒体运营技能检索结论（平台 × 缺口）

| 平台 | 本机已配置 | 生态检索结论 |
|------|-----------|-------------|
| 公众号 | 自动创作+发布草稿箱+排版+爆款套件 | 生态安装量 <300，无需补 |
| 小红书 | 定位/标题/正文/封面/热点/诊断全套 | 补「发布前审核」（敏感词/限流风险） |
| 抖音/B站 | 视频创作全流程套件 + 浏览器自动化 | 生态安装量 <500 或需第三方 API，不补 |
| 知乎/头条 | 全域搜索 + 发布编排 | 生态无专用技能，不补 |
| 全平台 | — | 补「跨平台实时热搜」（微博/知乎/百度/抖音/头条/B站） |

---

## 四、实装经验（6 个真实踩坑与解法）

### 1. Node 版本硬性要求

skills CLI（vercel-labs/skills v1.5.22）要求 **Node ≥22.20.0**。Node 22.16 实测报 `Cannot find module './compose/composer.js'`（yaml 依赖兼容问题），engines 是硬性的。

```powershell
# 升级到最新 LTS（2026-08：v24.19.0）
msiexec /i node-v24.19.0-x64.msi /qn /norestart   # 需管理员
corepack enable                                   # 恢复 pnpm
```

### 2. npm _npx 缓存损坏坑

`npx` 首次下载损坏的 yaml 包后每次复现同一错误；`npm cache clean --force` **不影响 `_npx` 目录**，且递归删除可能被安全策略拦截。

**解法**：`npm install -g skills` 全局安装 CLI，绕开 npx 缓存，日常用 `skills` 命令。

### 3. GitHub 直连失败 → 镜像安装

`skills add` 内部 git clone 报 `Connection was reset`（本机 GitHub 直连不稳），raw 也超时。

```powershell
git clone https://ghfast.top/https://github.com/<owner>/<repo>.git <临时目录>
skills add <临时目录> --skill <技能名> -a codex -g -y
```

本地路径安装同样写入 lock，后续可 `skills update` 管理。

### 4. 双保险目录同步（关键）

skills CLI 把 Codex 全局技能装到 `~\.agents\skills\`，但 Codex 实际从 **`~/.codex/skills/`** 加载——**必须复制副本**，否则技能不生效。

```powershell
Copy-Item <技能目录> ~/.codex/skills/ -Recurse
```

### 5. 安全评估解读

安装器自带 Gen/Socket/Snyk 评估。Snyk Med 常见原因是「技能可执行 shell 命令」（所有 agent 技能通用），仍需人工复核技能实际外联对象（实测 find-skills 仅查询 skills.sh/GitHub API）。

### 6. 外部 API 稳定性

hot-topics（60s API）实测：百度 50 条/微博 50 条/抖音 49 条即时返回；知乎 429、B站 500 为服务端临时状态，重试即可，非技能缺陷。技能索引可能过期（code-simplifier 案例）——**以 GitHub 源码为准**。

---

## 五、沉淀技能：skill-discovery-ops

把上述方法论固化为可复用技能（已通过结构校验）：

- `SKILL.md`：七步工作流（理解需求→检索→三查→冲突排除→实装→验证→记录）
- `references/analysis-template.md`：六维评估框架 + GitHub 发布文案结构
- `references/practice-notes.md`：实装经验库（含本会话全部踩坑）

安装：`skills add <repo> --skill skill-discovery-ops -a codex -g -y`

---

*素材生成：2026-08-12 · 旺财（能工巧匠 EduOpenAI Core 团队）· 全部结论均经实测核实*
