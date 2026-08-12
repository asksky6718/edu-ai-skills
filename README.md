# EduOpenAI Core · 职业教育 AI Skills 仓库

面向职业教育场景的 AI 工具技能包合集：备课、出题、考证辅导、课程运营、机构效率工具等。

> 品牌：对外统一使用 **EduOpenAI Core**；上游开源基座标识仅限技术文档与版权声明。

## 已发布 Skills

| Skill | 说明 | 适用 |
|-------|------|------|
| [edu-course-outline-generator](skills/edu-course-outline-generator/) | 职业教育课程大纲生成器：输入主题/人群/考试要求 → 模块化大纲+课时规划+配套练习 | 职教机构、教师、培训机构 |
| [skill-discovery-ops](skills/skill-discovery-ops/) | AI 智能体技能发现与实装运维：检索/评估/冲突排除/镜像安装/双保险同步/经验沉淀 | Codex 用户、Agent 开发者、AI 运营者 |

## 文章与经验

- [AI 智能体技能发现与实装实战（2026-08-12）](docs/ai-skill-discovery-practice_20260812.md)——一次完整闭环：技能检索→六维评估→冲突排除→实装→验证→沉淀；含平台×技能缺口表与 6 个真实踩坑解法（含命令）

## 路线图（计划中）

- AI 训练师三级备考助手（题库拆解/刷题计划）
- 职教考证攻略生成器（政策/报考/备考一键成文）
- AI 伴学督学提示词包（学情提醒/错题推送）
- 职教机构运营 SOP 生成器（课程上架/服务闭环）

## 目录规划

```
skills/
  <skill-name>/
    SKILL.md        # 技能说明（人设/触发词/工作流）
    references/     # 参考与模板
    assets/         # 素材
```

## 安装方式

```bash
# 将 skills/ 下的任意 skill 目录复制到 Codex 技能目录
cp -r skills/edu-course-outline-generator ~/.codex/skills/
```

## 维护

- 每个技能包遵循 Codex Skill 规范（frontmatter：name/description）
- 发布前过合规与品牌检查
- 版本随内容迭代，README 更新记录

## License

MIT
