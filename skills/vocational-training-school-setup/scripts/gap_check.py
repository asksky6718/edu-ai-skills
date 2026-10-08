#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""推进表机械核对：资质链 / 日期 / 状态 / 空值 / 顺序倒置。

用法：
    python gap_check.py --xlsx "项目推进表.xlsx" [--region 湖北] [--json-out out.json]

只做确定性检查并输出事实，不给主观评价。退出码：0=无阻断项，1=存在阻断项，2=文件/依赖问题。
"""
import argparse
import json
import re
import sys

try:
    import openpyxl
except ImportError:  # pragma: no cover
    print("ERROR[environment] 需要 openpyxl。请在虚拟环境或已装 openpyxl 的解释器中运行"
          "（脚本不会自动安装任何依赖，也不联网）")
    sys.exit(2)

DATE_RE = re.compile(r"(\d{4})\s*[-/年]\s*(\d{1,2})\s*[-/月]\s*(\d{1,2})")
CANDIDATE_DATE_RE = re.compile(r"\d{4}\s*[-/年]\s*\d{1,3}(?:\s*[-/月]\s*\d{1,3})?")

STATUS_OK = {"已完成", "进行中", "待确认", "待执行", "规划中"}

# 必备合规任务（关键词命中即视为"表内已覆盖"）
REQUIRED = [
    ("办学许可", ["办学许可", "办学许可证", "民办学校办学许可"], "资质链", True),
    ("法人登记", ["法人登记", "营业执照", "民办非企业", "登记证书"], "资质链", True),
    ("名称核准", ["名称核准", "核名", "名称自主申报", "名称预核准"], "资质链", True),
    ("立项/备案", ["立项", "备案", "决议", "批准书"], "资质链", True),
    ("场地产权/租赁", ["产权", "租赁", "场地合规", "场所", "面积"], "前置条件", True),
    ("消防", ["消防"], "前置条件", True),
    ("章程/管理制度", ["章程", "管理制度", "制度"], "前置条件", False),
    ("校长/教师资格", ["教师资格", "校长", "教师", "师资资格", "财会", "财务人员"], "前置条件", False),
    ("验资/注册资金", ["验资", "注册资金", "固定资产"], "前置条件", False),
    ("设施设备清单", ["设备清单", "设备采购", "设施设备"], "前置条件", False),
    ("收费公示", ["收费公示", "价格公示", "收费标准"], "运行合规", False),
    ("培训协议", ["培训协议", "合同模板"], "运行合规", False),
    ("实名制台账", ["台账", "实名制", "学员档案"], "运行合规", False),
    ("年检", ["年检", "检查评估"], "运行合规", False),
    ("评价资质", ["社评组织", "社会培训评价组织", "等级认定", "评价机构", "考核点"], "评价资质", False),
]

# 需要"资质先行"的任务：命中即要求其开始日期不早于办学许可办结日期
AFTER_LICENSE = ["招生", "宣传", "培训实施", "授课", "报名", "开课", "开班", "公示"]
TRIGGER_WORDS = ["招生", "宣传", "报名", "培训实施", "授课", "开课", "开班", "推广", "推广宣传"]


WANT = ["重点任务", "具体事项", "交付物", "负责人", "协同方", "当前状态", "验收标准", "时间节点", "备注"]


def cell_text(v):
    if v is None:
        return ""
    return str(v).strip()


def find_header_row(ws, min_hits=3):
    """表头行＝同时命中至少 min_hits 个标准列名的行（避免被正文里的说明文字误判）。"""
    for r in range(1, min(ws.max_row, 30) + 1):
        hits = sum(1 for c in range(1, ws.max_column + 1)
                   if cell_text(ws.cell(row=r, column=c).value) in WANT)
        if hits >= min_hits:
            return r
    return None


def collect_rows(ws, header_row):
    cols = {}
    for c in range(1, ws.max_column + 1):
        t = cell_text(ws.cell(row=header_row, column=c).value)
        if t:
            cols[t] = c
    want = WANT
    idx = {w: cols.get(w) for w in want}
    rows = []
    for r in range(header_row + 1, ws.max_row + 1):
        def g(name):
            c = idx.get(name)
            return cell_text(ws.cell(row=r, column=c).value) if c else ""
        item = {w: g(w) for w in want}
        item["_row"] = r
        # 跳过重复表头行与阶段标题行（无交付物、无状态、无时间节点）
        if not item["交付物"] and not item["时间节点"] and not item["当前状态"]:
            continue
        if any(item[k] == k for k in ("重点任务", "具体事项", "交付物", "时间节点")):
            continue
        if any(item[k] for k in ("重点任务", "具体事项", "交付物", "时间节点")):
            rows.append(item)
    return rows


def dates_in(text):
    """返回 (合法日期列表, 可疑片段列表)"""
    good, bad = [], []
    for m in DATE_RE.finditer(text):
        y, mo, d = (int(x) for x in m.groups())
        if 1 <= mo <= 12 and 1 <= d <= 31:
            good.append((y, mo, d))
        else:
            bad.append(m.group(0))
    for m in CANDIDATE_DATE_RE.finditer(text):
        frag = m.group(0)
        if not DATE_RE.fullmatch(frag):
            if any(ch.isdigit() for ch in frag) and frag not in bad:
                bad.append(frag)
    return good, bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--xlsx", required=True)
    ap.add_argument("--region", default="")
    ap.add_argument("--sheet", default="")
    ap.add_argument("--json-out", default="")
    args = ap.parse_args()

    wb = openpyxl.load_workbook(args.xlsx, data_only=True)
    sheets = [args.sheet] if args.sheet and args.sheet in wb.sheetnames else wb.sheetnames

    all_rows, findings = [], []
    for sn in sheets:
        ws = wb[sn]
        hr = find_header_row(ws)
        if hr is None:
            continue
        rows = collect_rows(ws, hr)
        for r in rows:
            r["_sheet"] = sn
        all_rows.extend(rows)

    if not all_rows:
        findings.append(("阻断", "结构", "未识别到任务表（找不到含「时间节点」的表头行）"))
    # 任务身份字段（只用这三列判断"表里有没有这件事"，避免被备注文字误命中）
    blob = "\n".join(" ".join([r["重点任务"], r["具体事项"], r["交付物"]]) for r in all_rows)

    # 1) 必备合规任务覆盖
    for label, kws, group, blocking in REQUIRED:
        if label == "评价资质":
            # 若全表未出现任何"发证/等级"表述，则不作为缺口，只提示
            if not any(k in blob for k in kws + ["证书"]):
                findings.append(("提示", "评价资质", "表内未涉及职业技能等级认定/发证事项；如计划对外发证，须补评价资质路线"))
                continue
        if not any(k in blob for k in kws):
            findings.append(("阻断" if blocking else "重要", group, "缺少「%s」相关任务（关键词：%s）" % (label, "/".join(kws))))

    # 2) 字段空值
    for r in all_rows:
        missing = [k for k in ("交付物", "负责人", "验收标准", "时间节点") if not r[k]]
        if missing:
            findings.append(("重要", "字段空值", "第%d行「%s」缺：%s" % (r["_row"], r["具体事项"][:24] or r["重点任务"][:24], "、".join(missing))))

    # 3) 日期格式
    bad_dates = {}
    for r in all_rows:
        good, bad = dates_in(r["时间节点"])
        if bad:
            for b in bad:
                bad_dates.setdefault(b, []).append(r["_row"])
        if r["时间节点"] and not good:
            findings.append(("重要", "日期", "第%d行时间节点无法解析：%s" % (r["_row"], r["时间节点"])))
    for b, rows_ in bad_dates.items():
        findings.append(("重要", "日期", "非法日期片段「%s」出现在第%s行" % (b, "、".join(map(str, rows_)))))

    # 4) 状态白名单
    for r in all_rows:
        st = r["当前状态"]
        if st and st not in STATUS_OK and not any(s in st for s in STATUS_OK):
            findings.append(("重要", "状态", "第%d行状态越界：「%s」（白名单：%s）" % (r["_row"], st, "/".join(sorted(STATUS_OK)))))
        if st == "已完成" and any(k in r["备注"] for k in ("待确认", "待核对", "需核对", "待核")):
            findings.append(("重要", "状态", "第%d行标「已完成」但备注含待核项：%s" % (r["_row"], r["备注"][:40])))

    # 5) 顺序：办学许可 / 立项 应在招生宣传之前
    license_rows = [r for r in all_rows if any(k in (r["重点任务"] + r["具体事项"] + r["交付物"]) for k in ("办学许可", "办学许可证"))]
    promo_rows = [r for r in all_rows if any(k in (r["重点任务"] + r["具体事项"] + r["交付物"]) for k in AFTER_LICENSE)]
    if not license_rows and promo_rows:
        findings.append(("阻断", "顺序", "表内存在招生/宣传/培训实施类任务（第%s行），但全表无「办学许可」任务 —— 资质未取不得招生办学"
                         % "、".join(str(r["_row"]) for r in promo_rows)))
    elif license_rows and promo_rows:
        lic_end = max((d for r in license_rows for d in dates_in(r["时间节点"])[0]), default=None)
        promo_start = min((d for r in promo_rows for d in dates_in(r["时间节点"])[0]), default=None)
        if lic_end and promo_start and promo_start < lic_end:
            findings.append(("阻断", "顺序", "招生/宣传类任务最早开始 %s 早于办学许可计划完成 %s"
                             % ("-".join(map(str, promo_start)), "-".join(map(str, lic_end)))))

    # 6) 责任人单点
    owners = {r["负责人"] for r in all_rows if r["负责人"]}
    if len(owners) == 1 and len(all_rows) > 8:
        findings.append(("建议", "分工", "全部 %d 项任务仅 1 位负责人（%s），无复核人；外部协同事项建议落到对方确认人"
                         % (len(all_rows), list(owners)[0])))

    # 7) 口径词
    for word, tip in (("补贴", "补贴口径须引当期文件原文，不写金额承诺"),
                      ("就业", "就业类表述一律写「协助推荐与对接」，不承诺结果与薪资"),
                      ("包就业", "禁止承诺就业")):
        if word in blob and tip not in [f[2] for f in findings]:
            findings.append(("提示", "口径", "表内出现「%s」：%s" % (word, tip)))

    order = {"阻断": 0, "重要": 1, "建议": 2, "提示": 3}
    findings.sort(key=lambda x: order.get(x[0], 9))

    lines = ["# 推进表机械核对报告", ""]
    lines.append("- 文件：`%s`" % args.xlsx)
    if args.region:
        lines.append("- 属地口径假设：%s（须以当地当期办事指南复核）" % args.region)
    lines.append("- 任务行数：%d（工作表：%s）" % (len(all_rows), "、".join(sheets)))
    counts = {}
    for lvl, _, _ in findings:
        counts[lvl] = counts.get(lvl, 0) + 1
    lines.append("- 结论：阻断 %d / 重要 %d / 建议 %d / 提示 %d" % (counts.get("阻断", 0), counts.get("重要", 0), counts.get("建议", 0), counts.get("提示", 0)))
    lines.append("")
    lines.append("| 级别 | 类别 | 事实 |")
    lines.append("|---|---|---|")
    for lvl, cat, msg in findings:
        lines.append("| %s | %s | %s |" % (lvl, cat, msg))
    report = "\n".join(lines)

    print(report)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump({"file": args.xlsx, "rows": len(all_rows), "findings": findings,
                       "counts": counts}, f, ensure_ascii=False, indent=2)
    sys.exit(1 if counts.get("阻断") else 0)


if __name__ == "__main__":
    main()
