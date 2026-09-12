# AGENTS.md — 98五笔资源库

## 仓库性质

纯数据/文档仓库：98五笔输入法的码表、拆分母表、学习资料与图片。**无代码、无构建、无测试、无包管理器**。生成码表的 Python 脚本在另一个仓库（github.com/yanhuacuo/98wubi-unicode），本仓库只存放产物。

## 主要文件与目录

- `README.md`：权威说明，改码表前必读。
- `Wubi98-Unicode15.1.txt`：拆分母表，Unicode 15.1 全部 99049 个汉字（已剔除 PUA 点位），格式为 `汉字<Tab>[拆分; 编码; 字符集]`，是生成一切其他码表的基础。
- `wubi98_U.dict.yaml`：RIME 码表。表头含 name/version/sort/columns/encoder 规则，正文为 `text<Tab>code<Tab>weight<Tab>stem`，weight 自 1098420 递减。
- `98五笔拆分映射表/`：OpenCC 纯文本词典（spelling1/2/3.txt），格式 `汉字<Tab>〔拆分〕`。
- `校正纪录-01..07.pdf`：历次码表校正记录，改动拆分数据前先查对应纪录。
- `字根图/`、`wiki-pic/`：README 与 wiki 引用的图片资源。
- `高频3500字详拆版.pdf`、`GB18030-27533.txt`（国标两万字全码，供反查/造词）。

## 码表格式约定（README 有完整定义）

- **单义表**（文件名含「单义」）：`词条<Tab>编码`，一行一词。
- **多义表**（文件名含「多义」）：`编码<空格>词条1<空格>词条2 …`，编码按英文字母序排列，间隔符只能是空格。

## 关键陷阱

1. **编码与行尾**：2026-09-12 起全库文本统一为 **UTF-8 无 BOM + LF**（`.gitattributes` 已固定，新增 `.txt/.md/.yaml` 提交时会被 git 自动规范化，勿提交 CRLF 或 UTF-16）。历史上为 UTF-16LE + BOM + CRLF；Windows 系输入法工具若仍需 UTF-16，须自行转回（转换无损，已实测往返字节一致：Python `decode('utf-16')` / `encode('utf-16-le')` 后补 BOM）。**勿用 macOS 自带 iconv 处理本仓库文件**——它误拒合法字符（如 U+44DD、增补平面 PUA U+F00D0，报 `Illegal byte sequence`），请用 Python strict 模式。
2. **PUA 私用区字符**：`Wubi98-Unicode15.1.txt` 与 `wubi98_U.dict.yaml` 的拆分列含 PUA 字符（表示无对应汉字的字根），**不要「清理」、规范化或替换它们**；完整显示需超集字体。
3. **文件名含中文与【】**，shell 中务必整体加引号。
4. **文件巨大**（最大约 6.4 MB / 约 11 万行）：不要整个读入上下文，用 `head` 取样或流式处理。
