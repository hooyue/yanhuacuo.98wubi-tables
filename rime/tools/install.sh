#!/bin/bash
# 五笔98繁体 → 鼠须管安装脚本
# 将 rime/dist 下的三个成品文件拷入 ~/Library/Rime 并重新部署。
# 无需清空 ~/Library/Rime：已有用户数据（拼音个人词典、界面设置等）均会保留；
# 若目标已有同名文件，先备份为 *.bak.时间戳 再覆盖。
set -euo pipefail

SRC="$(cd "$(dirname "$0")/../dist" && pwd)"
DST="$HOME/Library/Rime"
SQUIRREL="/Library/Input Methods/Squirrel.app/Contents/MacOS/Squirrel"

FILES=(
  wubi98_traditional.dict.yaml
  wubi98_traditional.schema.yaml
  default.custom.yaml
)

echo "源目录: $SRC"
echo "目标目录: $DST"
echo

for f in "${FILES[@]}"; do
  if [ -e "$DST/$f" ]; then
    bak="$DST/$f.bak.$(date +%Y%m%d%H%M%S)"
    cp "$DST/$f" "$bak"
    echo "已备份: $f → $(basename "$bak")"
  fi
  cp "$SRC/$f" "$DST/$f"
  echo "已拷贝: $f"
done

echo
echo "触发鼠须管重新部署…"
"$SQUIRREL" --reload

echo
echo "完成。按 Ctrl+\` 或 F4 选择「五笔98繁体」即可使用；敲 z 后接拼音可反查。"
