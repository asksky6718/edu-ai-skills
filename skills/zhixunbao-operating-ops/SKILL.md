---
name: zhixunbao-operating-ops
description: 网校管理后台“运营”栏目操作技能。覆盖网站装修、导航/区块/页面、文章/公告/证书、文档中心、商业模式案例、Skill资源、格物圈、AIOSTA认证等运营管理。当需要操作网校后台运营栏目、内容发布、Skill、格物圈、AIOSTA认证时触发。
---

# 网校后台-运营

## 范围

网站装修、导航/区块/页面、文章/公告/证书、文档中心、商业模式案例、Skill 资源、格物圈、AIOSTA 认证等运营管理。

## 公共前置

1. 按 `zhixunbao-admin-core` 完成登录并保持会话。
2. 内容发布前先做内容合规/脱敏检查。
3. 涉及状态流转（草稿→发布、待开考→进行中等）先确认当前状态。

## 常用操作速览

| 操作 | 后台入口 | 注意事项 |
|---|---|---|
| 导航管理 | `/admin/v2/navigation` | 修改后清缓存/验证前台 |
| 区块装修 | `/admin/v2/block` | 注意草稿/发布状态 |
| 文章/公告 | `/admin/v2/article`、`/announcement` | 发布后前台可见 |
| Skill 资源 | `/admin/v2/skill-resource` | 支持分类/状态/来源筛选 |
| 格物圈内容 | `/admin/v2/gewu-entry` | 支持 CSV 导入 |
| AIOSTA 认证项目 | `/admin/v2/aiosta/cert-project` | 状态机 draft→published→closed |
| AIOSTA 考试批次 | `/admin/v2/aiosta/exam-batch` | pending→in_progress→finished |
| AIOSTA 成绩/发证 | `/admin/v2/aiosta/cert-result` | 先公布成绩再发证 |

## 结果验证

- 前台页面/导航/区块渲染验证。
- 文章/公告发布后 URL 可访问、内容正确。
- 状态流转后在列表与详情核对。