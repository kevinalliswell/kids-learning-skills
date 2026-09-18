---
name: make-handwriting-sheet
description: Create printable A4 Chinese handwriting practice worksheets with KaiTi-style sample text, alternating one demonstration row and one blank row. Use when the user asks for 小学中文/语文练字帖, 字帖, 楷书临摹, 作文格, 横线格, to convert an uploaded worksheet/photo/text into a clean printable PDF/PNG, or to adjust grid and ruled-line practice pages for children.
---

# Make Handwriting Sheet

## Workflow

1. Extract or confirm the source text.
   - If the user provides an image, read the visible Chinese text carefully and preserve punctuation.
   - If text is unclear, ask only for the missing sentence or paragraph.
   - Normalize obvious OCR/visual mistakes, but do not rewrite the passage unless asked.

2. Create an A4 printable worksheet.
   - Default to a green school-workbook style: outer border, centered title, name/grade blanks, section titles.
   - Use standard KaiTi/Kai-style fonts for sample characters. Prefer `C:\Windows\Fonts\simkai.ttf`, then `C:\Windows\Fonts\STKAITI.TTF`.
   - Use the bundled script `scripts/create_handwriting_sheet.py` for PDF/PNG generation when possible.

3. Follow the practice-row rule.
   - Every sample row must be followed immediately by one blank row.
   - Composition grid rows: one row of square cells with KaiTi sample characters, then one empty row of square cells.
   - Ruled-line rows: one line with KaiTi sample text, then one empty ruled line.

4. Keep child-friendly typography and line breaks.
   - Avoid orphan punctuation at the start of a row.
   - Keep each sample line comfortably inside its grid or ruled line.
   - Preserve Chinese punctuation such as `，。！？、；：`.
   - For copied textbook passages, keep wording exact unless the user asks for simplification.

5. Verify before delivering.
   - Render or open the preview PNG.
   - Check that text is not clipped, grid cells align, blank rows exist after every sample row, and the page has printable margins.
   - Deliver the PDF first and a PNG preview second.

## Script Usage

Use a JSON config with `scripts/create_handwriting_sheet.py`.

```powershell
python C:\Users\kevin\.codex\skills\make-handwriting-sheet\scripts\create_handwriting_sheet.py `
  --config work\handwriting_config.json `
  --output-pdf outputs\练字帖.pdf `
  --preview-png outputs\练字帖_预览.png
```

Minimal config:

```json
{
  "title": "三上一实用书写专项训练",
  "sections": [
    {
      "title": "一、作文格训练",
      "type": "composition_grid",
      "cols": 20,
      "text": "当雷云在天上轰响，六月的阵雨落下的时候，湿润的东风走过荒野。"
    },
    {
      "title": "二、横线格训练",
      "type": "ruled_lines",
      "text": "树枝在林中互相碰触着，绿叶在狂风里簌簌地响。"
    }
  ]
}
```

Use `text` for normal automatic wrapping. Use `lines` when manual line breaks are important; the script still protects against overflow unless `preserve_lines_exact` is set to `true`.

```json
{
  "title": "三上一实用书写专项训练",
  "sections": [
    {
      "title": "一、作文格训练",
      "type": "composition_grid",
      "cols": 20,
      "lines": ["当雷云在天上轰响，六月的阵雨落下的时", "候，湿润的东风走过荒野。"]
    }
  ]
}
```

## Output Defaults

- In a Codex workspace, put transient configs under `work/`.
- Put user-facing PDFs and previews under the current task's `outputs/` directory.
- Use descriptive Chinese filenames, for example `三上一实用书写专项训练_练字帖.pdf`.
