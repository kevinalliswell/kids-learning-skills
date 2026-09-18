# make-handwriting-sheet

生成适合小朋友临摹的 A4 中文练字帖，默认使用楷体风格，支持作文格和横线格，并遵循“一行示范、一行空白”的练习规则。

## 适合触发的请求

```text
帮小朋友做一份练字帖，作文格和横线格都要，一行楷书字一行空白。
```

```text
用 $make-handwriting-sheet 根据这张图片做成可打印字帖。
```

## 功能

- A4 PDF 输出，适合直接打印。
- 生成 PNG 预览图，方便交付前检查。
- 作文格：一行楷书示范，一行空白格。
- 横线格：一行楷书示范，一行空白横线。
- 自动避开行首孤立标点。
- 自动分页，避免长文本挤出页面。

## 依赖

```powershell
pip install -r ..\..\requirements.txt
```

Windows 上优先使用系统字体：

- `C:\Windows\Fonts\simkai.ttf`
- `C:\Windows\Fonts\STKAITI.TTF`

## 示例命令

在仓库根目录运行：

```powershell
python .\skills\make-handwriting-sheet\scripts\create_handwriting_sheet.py `
  --config .\skills\make-handwriting-sheet\examples\basic.json `
  --output-pdf .\work\handwriting-sheet.pdf `
  --preview-png .\work\handwriting-sheet-preview.png
```

## 配置格式

见 [`examples/basic.json`](examples/basic.json)。

常用 section 类型：

- `composition_grid`：作文格。
- `ruled_lines`：横线格。

每个 section 可以用 `text` 自动换行，也可以用 `lines` 手动指定示范行。即使用 `lines`，脚本默认也会保护文本不要溢出横线；如果确实要完全保留手动断行，可设置 `preserve_lines_exact: true`。

## 扩展方向

- 增加田字格。
- 增加拼音格。
- 增加多页批量生成。
- 增加不同年级的默认字号和格子尺寸。
