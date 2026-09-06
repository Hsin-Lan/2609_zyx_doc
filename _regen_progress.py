#!/usr/bin/env python3
# 根据磁盘上 proof 文件的存在与否 + _inprogress.txt 重新生成 progress.md
import os, sys

BASE = "/Users/xinlan/202609-朱-校对"
os.chdir(BASE)

target = list(range(151, 992)) + list(range(993, 1263))  # 992 无此页

inprog_file = os.path.join(BASE, "_inprogress.txt")
inprog = set()
if os.path.exists(inprog_file):
    with open(inprog_file, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.isdigit():
                inprog.add(int(line))

def status(n):
    if os.path.exists(os.path.join(BASE, f"{n}-proof")):
        return "已完成"
    if n in inprog:
        return "处理中"
    return "待处理"

# build status per page
from collections import OrderedDict
st = {n: status(n) for n in target}
st[150] = "已完成"  # 试校样例，单独列出

counts = {"已完成": 0, "处理中": 0, "待处理": 0}
for n in target:
    counts[st[n]] += 1

# collapse contiguous runs of same status (over the ordered target list)
runs = []
if target:
    prev = st[target[0]]
    start = target[0]
    for n in target[1:]:
        if st[n] != prev:
            runs.append((start, prev))
            start = n
            prev = st[n]
    runs.append((start, prev))
# compress: consecutive runs with same status separated only by the 992 gap can stay separate for clarity

lines = []
lines.append("# 校对进度记录")
lines.append("")
lines.append("> 目标范围：印刷页 151–991、993–1262（**992 无此页**，卷间分隔页无页码不处理）。第 150 页为试校样例（已完成）。")
lines.append("")
lines.append(f"- 已完成：{counts['已完成']} 页")
lines.append(f"- 处理中：{counts['处理中']} 页")
lines.append(f"- 待处理：{counts['待处理']} 页")
lines.append("")
lines.append("## 状态明细（连续同状态合并显示）")
lines.append("")
lines.append("| 页码范围 | 状态 |")
lines.append("|------|------|")
lines.append("| 150 | 已完成（试校样例） |")
for start, s in runs:
    if start == target[-1]:
        rng = str(start)
    else:
        # find run end
        pass
# rebuild runs with end
runs2 = []
if target:
    prev = st[target[0]]
    start = target[0]
    for i, n in enumerate(target):
        if st[n] != prev:
            runs2.append((start, target[i-1], prev))
            start = n
            prev = st[n]
    runs2.append((start, target[-1], prev))
for start, end, s in runs2:
    if start == end:
        rng = str(start)
    else:
        rng = f"{start}–{end}"
    lines.append(f"| {rng} | {s} |")

with open("progress.md", "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

print(f"progress.md 已更新：已完成{counts['已完成']} / 处理中{counts['处理中']} / 待处理{counts['待处理']}")