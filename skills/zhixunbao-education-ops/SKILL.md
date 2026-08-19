---
name: zhixunbao-education-ops
description: 网校管理后台“教务”栏目操作技能。覆盖班课、产品库、教师、助教、教务参数等后台管理。当需要操作网校后台教务栏目、班课、教师、助教或教务设置时触发。
---

# 网校后台-教务

## 范围

班课、班课产品库、教师、助教、教务参数等教务管理。

## 公共前置

1. 按 `zhixunbao-admin-core` 完成登录并保持会话。
2. 先确认目标环境（dev/prod）与操作对象状态。
3. 写操作遵循“先查询 → 预检 → 执行 → 验证”。

## 常用操作速览

| 操作 | 后台入口 | 注意事项 |
|---|---|---|
| 查看班课列表 | `/admin/v2/multi_class/index` | 支持按状态/关键词过滤 |
| 班课巡检 | `/admin/v2/multi_class/inspection` | 用于检查异常班课 |
| 创建/编辑班课产品 | `/admin/v2/multi_class_product/index` | 产品库维护 |
| 教师管理 | `/admin/v2/teacher/index` | 设置教师可见性/推荐 |
| 助教管理 | `/admin/v2/assistant/index` | 配置班级助教 |
| 教务参数 | `/admin/v2/multi_class/setting` | 谨慎修改全局参数 |

## 结果验证

- 列表页刷新后检查目标对象是否出现在预期状态。
- 详情页核对字段、状态、关联关系。
- 只读接口/查询复核（如适用）。