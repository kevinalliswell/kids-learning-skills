from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


GREEN = "#5F8B4B"
LINE_GREEN = "#98BE8F"
BLACK = "#111111"
PUNCTUATION = set("，。！？；：、,.!?;:）】》”’")

DEFAULT_COMPOSITION_CELL_MM = 9.0
DEFAULT_COMPOSITION_COLS = 20
DEFAULT_LARGE_GRID_CELL_MM = 14.0
DEFAULT_LARGE_GRID_COLS = 13
DEFAULT_RULED_LINE_GAP_MM = 10.0
DEFAULT_RULED_WIDTH_MM = 180.0
DEFAULT_RULED_TEXT_INDENT_MM = 10.0


FONT_CANDIDATES = [
    Path(r"C:\Windows\Fonts\simkai.ttf"),
    Path(r"C:\Windows\Fonts\STKAITI.TTF"),
    Path(r"C:\Windows\Fonts\simfang.ttf"),
    Path("/System/Library/Fonts/Supplemental/Kaiti.ttc"),
    Path("/System/Library/Fonts/STHeiti Light.ttc"),
    Path("/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc"),
    Path("/usr/share/fonts/truetype/arphic/ukai.ttc"),
]


def find_font() -> Path:
    for path in FONT_CANDIDATES:
        if path.exists():
            return path
    raise FileNotFoundError("No KaiTi-compatible Chinese font found.")


def register_fonts() -> None:
    font_path = find_font()
    pdfmetrics.registerFont(TTFont("HWKai", str(font_path)))
    pdfmetrics.registerFont(TTFont("HWTitle", str(font_path)))


def points_from_mm(value: float) -> float:
    return float(value) * mm


def dimension(section: dict, pt_key: str, mm_key: str, default_mm: float) -> float:
    if mm_key in section:
        return points_from_mm(float(section[mm_key]))
    if pt_key in section:
        return float(section[pt_key])
    return points_from_mm(default_mm)


def grid_style(section: dict, section_type: str) -> str:
    style = str(section.get("grid_style", "")).strip().lower().replace("-", "_")
    if style in {"large", "large_square", "big", "big_square", "大方格"}:
        return "large_square"
    if style in {"composition", "composition_grid", "作文格"}:
        return "composition"
    if section_type == "large_grid":
        return "large_square"
    return "composition"


def grid_defaults(section: dict, section_type: str) -> tuple[int, float]:
    style = grid_style(section, section_type)
    if style == "large_square":
        default_cols = DEFAULT_LARGE_GRID_COLS
        default_cell_mm = DEFAULT_LARGE_GRID_CELL_MM
    else:
        default_cols = DEFAULT_COMPOSITION_COLS
        default_cell_mm = DEFAULT_COMPOSITION_CELL_MM
    cols = int(section.get("cols", default_cols))
    cell = dimension(section, "cell", "cell_mm", default_cell_mm)
    return cols, cell


def draw_centered(c: canvas.Canvas, text: str, x: float, y: float, width: float, font: str, size: float, color: str) -> None:
    c.setFont(font, size)
    c.setFillColor(color)
    text_width = pdfmetrics.stringWidth(text, font, size)
    c.drawString(x + (width - text_width) / 2, y, text)


def draw_page_header(c: canvas.Canvas, cfg: dict, page_num: int) -> None:
    page_w, page_h = A4
    border = cfg.get("border", 24)
    c.setStrokeColor(cfg.get("line_color", LINE_GREEN))
    c.setLineWidth(1.8)
    c.rect(border, 22, page_w - border * 2, page_h - 44)

    title = cfg.get("title", "语文练字帖")
    draw_centered(c, title, 0, page_h - 78, page_w, "HWTitle", 24, cfg.get("title_color", GREEN))

    c.setFont("HWKai", 15)
    c.setFillColor(cfg.get("title_color", GREEN))
    c.drawString(232, page_h - 134, cfg.get("name_label", "姓名："))
    c.drawString(385, page_h - 134, cfg.get("grade_label", "年级："))
    c.setStrokeColor(cfg.get("line_color", LINE_GREEN))
    c.setLineWidth(1)
    c.line(280, page_h - 137, 360, page_h - 137)
    c.line(433, page_h - 137, 520, page_h - 137)

    if page_num > 1:
        c.setFont("HWKai", 9)
        c.setFillColor(cfg.get("title_color", GREEN))
        c.drawRightString(page_w - 42, 34, str(page_num))


def draw_section_title(c: canvas.Canvas, text: str, x: float, y: float, color: str) -> None:
    c.setFont("HWKai", 17)
    c.setFillColor(color)
    c.drawString(x, y, text)


def normalize_text(text: str) -> str:
    return text.replace("\r", "").replace("\n", "").replace("\t", "　")


def wrap_grid_text(text: str, cols: int) -> tuple[list[str], dict[int, str]]:
    rows: list[str] = []
    trailing: dict[int, str] = {}
    current: list[str] = []
    for ch in normalize_text(text):
        if len(current) >= cols:
            rows.append("".join(current))
            current = []
        if not current and rows and ch in PUNCTUATION:
            trailing[len(rows) - 1] = trailing.get(len(rows) - 1, "") + ch
            continue
        current.append(ch)
    if current:
        rows.append("".join(current))
    return rows, trailing


def prepare_grid_lines(section: dict) -> tuple[list[str], dict[int, str]]:
    cols = int(section.get("cols", 20))
    lines = section.get("lines")
    if lines:
        rows: list[str] = []
        trailing: dict[int, str] = {}
        for raw in lines:
            wrapped, marks = wrap_grid_text(str(raw), cols)
            offset = len(rows)
            rows.extend(wrapped)
            for idx, mark in marks.items():
                trailing[offset + idx] = mark
        for key, value in section.get("trailing_marks", {}).items():
            trailing[int(key)] = str(value)
        return rows, trailing
    return wrap_grid_text(str(section.get("text", "")), cols)


def draw_composition_grid(
    c: canvas.Canvas,
    x: float,
    top_y: float,
    cols: int,
    cell: float,
    sample_lines: list[str],
    trailing_marks: dict[int, str],
    line_color: str,
) -> float:
    rows = len(sample_lines) * 2
    width = cols * cell
    height = rows * cell
    bottom_y = top_y - height

    c.setStrokeColor(line_color)
    c.setLineWidth(0.85)
    for i in range(cols + 1):
        px = x + i * cell
        c.line(px, top_y, px, bottom_y)
    for j in range(rows + 1):
        py = top_y - j * cell
        c.line(x, py, x + width, py)

    font_size = min(16.2, cell * 0.74)
    c.setFont("HWKai", font_size)
    c.setFillColor(BLACK)
    for line_idx, line in enumerate(sample_lines):
        row = line_idx * 2
        row_bottom = top_y - (row + 1) * cell
        for col_idx, ch in enumerate(list(line)[:cols]):
            if ch in {" ", "　"}:
                continue
            char_width = pdfmetrics.stringWidth(ch, "HWKai", font_size)
            cx = x + col_idx * cell + (cell - char_width) / 2
            cy = row_bottom + cell * 0.19
            c.drawString(cx, cy, ch)
        if line_idx in trailing_marks:
            c.setFont("HWKai", max(7, font_size * 0.52))
            c.drawString(x + cols * cell - cell * 0.35, row_bottom + cell * 0.12, trailing_marks[line_idx])
            c.setFont("HWKai", font_size)
    return bottom_y


def wrap_ruled_text(text: str, font: str, size: float, max_width: float) -> list[str]:
    lines: list[str] = []
    current = ""
    for ch in normalize_text(text):
        trial = current + ch
        if pdfmetrics.stringWidth(trial, font, size) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = ch
    if current:
        lines.append(current)

    for idx in range(1, len(lines)):
        while lines[idx] and lines[idx][0] in PUNCTUATION and lines[idx - 1]:
            lines[idx - 1] += lines[idx][0]
            lines[idx] = lines[idx][1:]
        while 0 < len(lines[idx]) < 3 and len(lines[idx - 1]) > 3:
            lines[idx] = lines[idx - 1][-1] + lines[idx]
            lines[idx - 1] = lines[idx - 1][:-1]
    return [line for line in lines if line]


def draw_ruled_pair(c: canvas.Canvas, x: float, line_y: float, width: float, sample: str, row_gap: float, font_size: float, line_color: str) -> float:
    c.setStrokeColor(line_color)
    c.setLineWidth(0.9)
    c.line(x, line_y, x + width, line_y)
    c.setFont("HWKai", font_size)
    c.setFillColor(BLACK)
    c.drawString(x + points_from_mm(DEFAULT_RULED_TEXT_INDENT_MM), line_y + 5.2, sample)

    blank_y = line_y - row_gap
    c.setStrokeColor(line_color)
    c.line(x, blank_y, x + width, blank_y)
    return line_y - row_gap * 2


def new_page(c: canvas.Canvas, cfg: dict, page_num: int) -> tuple[int, float]:
    if page_num > 0:
        c.showPage()
    page_num += 1
    draw_page_header(c, cfg, page_num)
    return page_num, A4[1] - 171


def build_pdf(config: dict, output_pdf: Path) -> None:
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    register_fonts()
    c = canvas.Canvas(str(output_pdf), pagesize=A4)
    c.setTitle(config.get("title", "语文练字帖"))

    page_w, _ = A4
    left = float(config.get("left_margin", 62))
    bottom_limit = float(config.get("bottom_margin", 60))
    title_color = config.get("title_color", GREEN)
    line_color = config.get("line_color", LINE_GREEN)

    page_num, y = new_page(c, config, 0)
    for section in config.get("sections", []):
        section_type = section.get("type", "ruled_lines")
        title = section.get("title", "")
        if y < bottom_limit + 90:
            page_num, y = new_page(c, config, page_num)

        draw_section_title(c, title, left, y, title_color)

        if section_type in {"composition_grid", "large_grid"}:
            cols, cell = grid_defaults(section, section_type)
            rows, trailing = prepare_grid_lines(section)
            width = cols * cell
            x = float(section.get("x", (page_w - width) / 2))
            y -= float(section.get("title_gap", 27))
            max_sample_rows = max(1, math.floor((y - bottom_limit) / (cell * 2)))
            start = 0
            while start < len(rows):
                chunk = rows[start : start + max_sample_rows]
                chunk_marks = {
                    idx - start: mark
                    for idx, mark in trailing.items()
                    if start <= idx < start + len(chunk)
                }
                bottom_y = draw_composition_grid(c, x, y, cols, cell, chunk, chunk_marks, line_color)
                start += len(chunk)
                y = bottom_y - float(section.get("section_gap", 42))
                if start < len(rows):
                    page_num, y = new_page(c, config, page_num)
                    draw_section_title(c, f"{title}（续）", left, y, title_color)
                    y -= float(section.get("title_gap", 27))
                    max_sample_rows = max(1, math.floor((y - bottom_limit) / (cell * 2)))

        else:
            font_size = float(section.get("font_size", 17))
            row_gap = dimension(section, "row_gap", "row_gap_mm", DEFAULT_RULED_LINE_GAP_MM)
            width = dimension(section, "width", "width_mm", DEFAULT_RULED_WIDTH_MM)
            x = float(section.get("x", (page_w - width) / 2))
            y -= float(section.get("title_gap", 44))
            lines = []
            raw_lines = [str(line) for line in section.get("lines", [])]
            if raw_lines and section.get("preserve_lines_exact"):
                lines = raw_lines
            elif raw_lines:
                for raw_line in raw_lines:
                    lines.extend(wrap_ruled_text(raw_line, "HWKai", font_size, width - points_from_mm(DEFAULT_RULED_TEXT_INDENT_MM + 3)))
            else:
                lines = wrap_ruled_text(str(section.get("text", "")), "HWKai", font_size, width - points_from_mm(DEFAULT_RULED_TEXT_INDENT_MM + 3))

            for sample in lines:
                if y - row_gap < bottom_limit:
                    page_num, y = new_page(c, config, page_num)
                    draw_section_title(c, f"{title}（续）", left, y, title_color)
                    y -= float(section.get("title_gap", 44))
                y = draw_ruled_pair(c, x, y, width, sample, row_gap, font_size, line_color)
            y -= float(section.get("section_gap", 34))

    c.showPage()
    c.save()


def render_preview(output_pdf: Path, preview_png: Path) -> None:
    import pypdfium2 as pdfium

    preview_png.parent.mkdir(parents=True, exist_ok=True)
    doc = pdfium.PdfDocument(str(output_pdf))
    try:
        page = doc[0]
        bitmap = page.render(scale=2.0).to_pil()
        bitmap.save(preview_png)
    finally:
        doc.close()


def default_config() -> dict:
    return {
        "title": "语文练字帖",
        "sections": [
            {
                "title": "一、作文格训练",
                "type": "composition_grid",
                "cols": 20,
                "text": "当雷云在天上轰响，六月的阵雨落下的时候，湿润的东风走过荒野，在竹林中吹着口笛。",
            },
            {
                "title": "二、横线格训练",
                "type": "ruled_lines",
                "text": "树枝在林中互相碰触着，绿叶在狂风里簌簌地响，雷云拍着大手。",
            },
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Create an A4 Chinese handwriting practice sheet PDF.")
    parser.add_argument("--config", type=Path, help="JSON worksheet configuration.")
    parser.add_argument("--output-pdf", type=Path, required=True, help="Output PDF path.")
    parser.add_argument("--preview-png", type=Path, help="Optional first-page PNG preview path.")
    args = parser.parse_args()

    if args.config:
        config = json.loads(args.config.read_text(encoding="utf-8"))
    else:
        config = default_config()

    build_pdf(config, args.output_pdf)
    if args.preview_png:
        render_preview(args.output_pdf, args.preview_png)


if __name__ == "__main__":
    main()
