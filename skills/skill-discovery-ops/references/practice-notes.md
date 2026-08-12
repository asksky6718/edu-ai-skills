# 实装经验库（2026-08-12 实战沉淀）

> 来源：旺财本机实装 find-skills、hot-topics、xiaohongshu-note-analyzer 的完整过程。

## 1. Node 前置条件（skills CLI）

- skills CLI（vercel-labs/skills）engines 要求 **Node ≥22.20.0**；
- Node 22.16.0 实测不可用：报 `Cannot find module './compose/composer.js'`（yaml@2.8 兼容问题），**engines 为硬性要求**；
- 升级目标选**最新 LTS**（2026-08：v24.19.0 Krypton；Node 26 仍 current 未选用）；官方 MSI 静默安装：`msiexec /i <msi> /qn /norestart`（需管理员）；
- 升级后验证：`node --version` / `npm --version` / 全局包 `npm ls -g --depth=0` / pnpm（corepack 恢复：`corepack enable`）。

## 2. npm _npx 缓存损坏坑

- 现象：npx 首次下载损坏的 yaml 包后，之后每次复现同一错误（同一 hash 目录 `npm-cache\_npx\<hash>`）；
- `npm cache clean --force` **不影响 _npx 目录**；
- 递归删除 _npx 目录可能被本机安全策略拦截；
- **解法**：`npm install -g skills` 全局安装 CLI，彻底绕开 npx 缓存，日常用 `skills` 命令。

## 3. GitHub 直连失败 → 镜像安装

- 现象：`skills add` 内部 git clone 报 `Recv failure: Connection was reset`（本机 GitHub 直连不稳）；
- raw.githubusercontent 亦超时，但 ghfast.top 镜像可达；
- **解法**：`git clone https://ghfast.top/https://github.com/<owner>/<repo>.git` 到临时目录 → `skills add <本地路径> --skill <名> -a codex -g -y`（本地路径安装同样写入 lock，可管理）。

## 4. 双保险目录同步（关键）

- skills CLI 1.5.22 将 Codex 全局技能装到 **`~\.agents\skills\`**；
- Codex 桌面端实际从 **`~/.codex/skills/`** 加载（本机 67+ 技能均在此）；
- **每次安装后必须复制副本**：`Copy-Item <src> ~/.codex/skills/ -Recurse`，否则 Codex 不加载；
- `skills list -g` 能看到两处（.agents 来源=vercel-labs/本地，.codex 来源=local）。

## 5. 安装器安全评估解读

- 官方安装器输出：Gen（Safe/Risk）+ Socket（alerts 数）+ Snyk（Low/Med/High）；
- Snyk Med 常见原因为「技能可执行 shell 命令」（所有 agent 技能皆有此能力，属通用提示）；
- 仍需人工复核：技能实际外联对象（实测 find-skills 仅查询 skills.sh/GitHub API）。

## 6. 外部 API 实测（hot-topics 案例）

- 端点：`https://60s.viki.moe/v2/{weibo|zhihu|douyin|bili|toutiao}`、`/v2/baidu/hot`；
- 实测：百度 50 条/微博 50 条/抖音 49 条即时返回；知乎 429（限流）与 B站 500（服务端错误）属**外部服务临时状态**，重试即可，非技能缺陷；
- 技能索引可能过期（code-simplifier 案例：skills.sh 显示存在但源码已下线）→ **以 GitHub 源码为准**。

## 7. 冲突排除清单（Codex 原生不装）

| 类型 | 案例 | 判定 |
|------|------|------|
| 与内置工具重复 | tavily-search（vs 内置 search） | 不装 |
| 平台不兼容 | summarize（brew 仅 macOS） | 不装 |
| 非 Codex 配置对象 | memory-setup（Clawdbot） | 不装 |
| 其他 agent 专属机制 | self-improving-agent（hooks）/write-xiaohongshu（MCP） | 不装 |
| 生态索引过期 | code-simplifier（多实现已下线） | 不装 |
| 需付费第三方 API | social-publishing（国外平台） | 不装 |

## 8. 真实安装案例（2026-08-12）

- find-skills：vercel-labs/skills 官方，28.7K star，MIT；装后实测 `skills find` 检索正常；
- hot-topics：vikiboss/60s-skills，1.9K installs，MIT；跨平台实时热搜，API 实测可用；
- xiaohongshu-note-analyzer：softbread/xiaohongshu-doctor，2.9K installs；发布前审核（关键词/敏感词/限流风险），纯提示词无外部依赖。
