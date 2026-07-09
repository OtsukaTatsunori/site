"""全記事画像をデータ駆動で一括生成"""
from __future__ import annotations
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
from image_data import IMAGES

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "articles" / "images"
OUT.mkdir(parents=True, exist_ok=True)
W = 800
BRAND = "#C56B49"
SITE = "大人の学びなおし比較"

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700;900&family=Noto+Serif+JP:wght@700;900&family=Zen+Maru+Gothic:wght@500;700&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Noto Sans JP',sans-serif;-webkit-font-smoothing:antialiased;background:#FAF8F3;width:800px;color:#2D3748}
"""

RC = {"◎": "#5B8C3E", "○": "#4A7FAD", "△": "#C9943A", "×": "#C75450",
      "◎ ": "#5B8C3E", "良い": "#5B8C3E", "良い点": "#5B8C3E",
      "注意": "#C75450", "注意点": "#C75450", "できる": "#5B8C3E",
      "不可": "#C75450", "必須": "#C56B49", "最重要": "#C56B49",
      "覚悟": "#C9943A"}


def render_table_image(data: dict):
    rows_html = ""
    for icon, label, value, extra in data["rows"]:
        ec = RC.get(extra, "#8B7E6A")
        extra_html = f'<span style="color:{ec};font-weight:700;font-size:14px">{extra}</span>' if extra else ""
        rows_html += f"""<div style="display:flex;align-items:center;padding:16px 36px;border-bottom:2px dashed #E8DFD0;gap:12px">
          <span style="font-size:22px;width:32px;flex-shrink:0">{icon}</span>
          <span style="width:110px;font-size:15px;color:#8B7E6A;font-weight:700;font-family:'Zen Maru Gothic',sans-serif;flex-shrink:0">{label}</span>
          <span style="flex:1;font-size:17px;font-weight:700;color:#2D3748">{value}</span>
          {extra_html}
        </div>"""

    title = data["title"]
    sub = data.get("sub", "")
    sub_html = f'<p style="font-size:16px;opacity:.7;margin-top:4px">{sub}</p>' if sub else ""

    html = f"""<!DOCTYPE html><html><head><style>{CSS}</style></head><body>
    <div style="background:{BRAND};color:#fff;padding:28px 36px;position:relative">
      <div style="font-family:'Noto Serif JP',serif;font-size:24px;font-weight:900">{title}</div>
      {sub_html}
      <div style="position:absolute;bottom:-8px;left:36px;width:60px;height:4px;background:#FFE8A3;border-radius:2px"></div>
    </div>
    {rows_html}
    <div style="padding:16px 36px;border-top:2px dashed #E8DFD0;font-size:13px;color:#A89F91;text-align:right;font-family:'Zen Maru Gothic',sans-serif">{SITE}</div>
    </body></html>"""

    path = OUT / data["file"]
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": W, "height": 2000}, device_scale_factor=2)
        page.set_content(html, wait_until="networkidle")
        page.locator("body").screenshot(path=str(path), type="png")
        browser.close()
    print(f"✅ {data['file']}")


def main():
    print(f"画像を生成中... ({len(IMAGES)}枚)\n")
    ok = 0
    ng = 0
    for img in IMAGES:
        try:
            render_table_image(img)
            ok += 1
        except Exception as e:
            print(f"❌ {img['file']}: {e}", file=sys.stderr)
            ng += 1
    print(f"\n完了！ 成功:{ok} 失敗:{ng} → {OUT}")
    return 0 if ng == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
