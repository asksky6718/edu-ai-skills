# 变更记录 · vocational-training-school-setup

## [1.1.0] — 2026-10-08

### 新增
- **按技能骨架规范改造**：新增根路由入口（能力总览 ＋ 路由判定表 ＋ 通则 ＋ 执行前核对），业务正文下沉到 5 个子技能与 `references/`
- 5 个子技能六段封面：`scope-route`（口径与路线）、`gap-check`（推进表核对）、`deliverables`（交付物清单）、`compliance`（运行合规）、`evaluation`（评价资质）
- `references/application-package-recipe.md` —— 职业（工种）申报包配方（六大类、逐份要点、设置标准门槛表、装包自检）
- `references/case-shanghai-ai-trainer.md` —— 脱敏案例：一套实际报送的申报材料实录（49 份文件的组织方式、字段栏目、门槛阈值、6 条可复用经验）
- 发布要件：`README.md` / `CHANGELOG.md` / `VERSION` / `LICENSE` / `manifest.json` / `agents/interface.yaml`
- 路由判定表带**前置门禁**与「**明确不要做**」两列；「评价资质」标为**须点名**

### 变更
- `SKILL.md` 从「一页装下全部流程」改为路由入口；原六步工作流与九段摘要保留在 `references/playbook-9-stages.md`
- 「两条铁律」提到根入口显要位置（属地当期文件为准；办学许可 ≠ 社评组织备案）
- 缺口分档口径统一为**阻断 / 重要 / 建议 / 提示**四级

### 修复
- `scripts/gap_check.py`：报错提示去掉本机解释器绝对路径，补「在虚拟环境或已装依赖的解释器中运行」（对应安全审计 P1 项）
- 参考件与测试记录中的**地名绑定、主体名、工作区名、本机路径**全部脱敏
- 内部件（安全审计报告）**不进发布包**

### 脱敏
- 主体名 / 客户名 / 项目名 / 地名绑定 / 人名 / 证件号 / 第三方机构名 / 本机绝对路径 —— 全部替换为中性泛称或删除；案例中的市场数据不转发
