#!/usr/bin/env python3
"""单行多义表 → RIME 码表（.dict.yaml）转换器

输入格式（98五笔单字表-【多义】.txt）：
    编码<空格>字1<空格>字2<空格>…
    编码仅 a-y，长度 1~4（1~3 码为简码行，4 码为全码行）；
    行内字的顺序即候选顺序。

输出（RIME 字典，sort: by_weight）：
    字<Tab>编码<Tab>权重
    权重自 --start-weight 起，按行序与行内字序全局递减，
    保证同编码下候选顺序与多义表行内顺序一致。

用法：
    python3 duoyi2rime.py 输入.txt 输出.dict.yaml
"""

import argparse
import re
import sys

CODE_RE = re.compile(r"^[a-y]{1,4}$")


def convert(src: str, dst: str, name: str, version: str, start_weight: int) -> int:
    errors = []
    entries = []          # (text, code, weight)
    code_count = 0
    weight = start_weight

    with open(src, encoding="utf-8") as f:
        for lineno, raw in enumerate(f, 1):
            line = raw.rstrip("\n")
            if not line:
                errors.append(f"第 {lineno} 行为空行")
                continue
            parts = line.split(" ")
            code, chars = parts[0], parts[1:]
            if not CODE_RE.match(code):
                errors.append(f"第 {lineno} 行编码非法: {code!r}")
                continue
            if not chars or any(c == "" for c in chars):
                errors.append(f"第 {lineno} 行候选缺失或含连续空格: {line!r}")
                continue
            dup = [c for c in set(chars) if chars.count(c) > 1]
            if dup:
                errors.append(f"第 {lineno} 行行内重复字: {' '.join(dup)}")
            for ch in chars:
                if len(ch) != 1:
                    errors.append(f"第 {lineno} 行词条非单字: {ch!r}")
                    continue
                entries.append((ch, code, weight))
                weight -= 1
            code_count += 1

    if errors:
        for e in errors[:50]:
            print(f"[错误] {e}", file=sys.stderr)
        print(f"共 {len(errors)} 处错误，未写出文件", file=sys.stderr)
        return 1

    with open(dst, "w", encoding="utf-8", newline="\n") as f:
        f.write("# Rime dictionary\n")
        f.write("# encoding: utf-8\n")
        f.write(f"# 由「单行多义表」转换生成，候选顺序 = 表内行内顺序\n\n")
        f.write("---\n")
        f.write(f"name: {name}\n")
        f.write(f'version: "{version}"\n')
        f.write("sort: by_weight\n")
        f.write("columns:\n")
        f.write("  - text\n")
        f.write("  - code\n")
        f.write("  - weight\n")
        f.write("...\n\n")
        for text, code, w in entries:
            f.write(f"{text}\t{code}\t{w}\n")

    # ---- 自检输出 ----
    char2codes = {}
    for text, code, _ in entries:
        char2codes.setdefault(text, []).append(code)
    print(f"编码行数: {code_count}")
    print(f"词条总数: {len(entries)}")
    print(f"单字去重: {len(char2codes)}")
    print(f"权重区间: {weight + 1} ~ {start_weight}")
    for sample in ("的", "一", "式"):
        codes = char2codes.get(sample)
        print(f"抽样「{sample}」编码: {' '.join(codes) if codes else '缺失!'}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="单行多义表 → RIME 码表转换器")
    ap.add_argument("input", help="多义表路径（编码 字1 字2 …）")
    ap.add_argument("output", help="输出 .dict.yaml 路径")
    ap.add_argument("--name", default="wubi98_traditional", help="码表名（须与文件名一致）")
    ap.add_argument("--version", default="1.0")
    ap.add_argument("--start-weight", type=int, default=1_000_000)
    args = ap.parse_args()
    return convert(args.input, args.output, args.name, args.version, args.start_weight)


if __name__ == "__main__":
    sys.exit(main())
