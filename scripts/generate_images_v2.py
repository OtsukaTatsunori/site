"""
HTML/CSS + Playwright で記事画像を生成（v3: マイベスト風・引き算デザイン）

デザイン原則:
- 白背景 + 控えめな影
- 文字は黒/グレー中心。色はアクセントだけ
- 余白たっぷり
- 評価は◎○△×やバーで視覚化
- 全画像にブランド統一テンプレ

使い方:
  python scripts/generate_images_v2.py
"""
from __future__ import annotations

import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "articles" / "images"
OUT.mkdir(parents=True, exist_ok=True)

WIDTH = 1200
BRAND_COLOR = "#2563eb"
BRAND_NAME = "大人の学びなおし比較"


def render(html: str, path: Path):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": WIDTH, "height": 800}, device_scale_factor=2)
        page.set_content(html, wait_until="networkidle")
        page.screenshot(path=str(path), type="png", full_page=True)
        browser.close()
    print(f"✅ {path.name}")


RESET = """
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700;900&display=swap');
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Noto Sans JP', sans-serif; -webkit-font-smoothing: antialiased; background: #fff; }
"""

# 全画像共通のブランドヘッダー＋フッター
def wrap(title: str, body_html: str, subtitle: str = "") -> str:
    sub = f'<p class="hd-sub">{subtitle}</p>' if subtitle else ""
    return f"""<!DOCTYPE html><html><head><style>
    {RESET}
    body {{ width: {WIDTH}px; }}
    .hd {{
      background: {BRAND_COLOR}; color: #fff; padding: 36px 60px;
    }}
    .hd-title {{ font-size: 32px; font-weight: 900; }}
    .hd-sub {{ font-size: 18px; opacity: 0.8; margin-top: 8px; }}
    .content {{ padding: 40px 60px; }}
    .ft {{
      padding: 20px 60px; border-top: 1px solid #e5e7eb;
      font-size: 14px; color: #9ca3af; text-align: right;
    }}
    </style></head><body>
    <div class="hd"><div class="hd-title">{title}</div>{sub}</div>
    <div class="content">{body_html}</div>
    <div class="ft">{BRAND_NAME}</div>
    </body></html>"""


# ============================================================
# 1. アイキャッチ: 動画編集 未経験
# ============================================================
def eyecatch_beginner():
    html = f"""<!DOCTYPE html><html><head><style>
    {RESET}
    body {{
      width: {WIDTH}px; height: 630px;
      background: #fff;
      display: flex; position: relative; overflow: hidden;
    }}
    .left {{
      flex: 1; padding: 56px 60px; display: flex; flex-direction: column; justify-content: center;
    }}
    .right {{
      width: 400px; background: {BRAND_COLOR};
      display: flex; align-items: center; justify-content: center;
    }}
    .play {{
      width: 120px; height: 120px; border-radius: 50%; background: rgba(255,255,255,0.15);
      display: flex; align-items: center; justify-content: center;
    }}
    .play::after {{
      content: ''; border-left: 36px solid #fff; border-top: 22px solid transparent; border-bottom: 22px solid transparent;
      margin-left: 6px;
    }}
    .tag {{
      display: inline-block; background: {BRAND_COLOR}; color: #fff; padding: 6px 18px;
      border-radius: 6px; font-size: 16px; font-weight: 700; margin-bottom: 20px;
    }}
    h1 {{ font-size: 44px; font-weight: 900; color: #1e293b; line-height: 1.4; }}
    h1 em {{ font-style: normal; color: {BRAND_COLOR}; }}
    .sub {{ font-size: 20px; color: #64748b; margin-top: 16px; line-height: 1.6; }}
    .chips {{ display: flex; gap: 10px; margin-top: 24px; flex-wrap: wrap; }}
    .chip {{
      padding: 6px 16px; border-radius: 20px; font-size: 14px; font-weight: 500;
      background: #f1f5f9; color: #475569;
    }}
    .ft {{
      position: absolute; bottom: 16px; left: 60px; font-size: 14px; color: #94a3b8;
    }}
    </style></head><body>
    <div class="left">
      <span class="tag">2026年版</span>
      <h1>動画編集は<br><em>未経験でも始められる？</em></h1>
      <p class="sub">失敗しない始め方とおすすめスクール</p>
      <div class="chips">
        <span class="chip">独学 vs スクール</span>
        <span class="chip">4ステップロードマップ</span>
        <span class="chip">失敗パターン5選</span>
      </div>
      <div class="ft">{BRAND_NAME}</div>
    </div>
    <div class="right"><div class="play"></div></div>
    </body></html>"""
    render(html, OUT / "eyecatch-video-editing-beginner.png")


# ============================================================
# 2. アイキャッチ: 無料動画編集ソフト比較
# ============================================================
def eyecatch_free_software():
    badges = "".join(
        f'<span class="b" style="border-left: 4px solid {c}">{n}</span>'
        for n, c in [
            ("CapCut", "#00d1ff"), ("DaVinci Resolve", "#ff6b35"), ("iMovie", "#a855f7"),
            ("Clipchamp", "#3b82f6"), ("Canva", "#06b6d4"), ("Shotcut", "#84cc16"), ("Filmora", "#f59e0b"),
        ]
    )
    html = f"""<!DOCTYPE html><html><head><style>
    {RESET}
    body {{
      width: {WIDTH}px; height: 630px;
      background: #fff; display: flex; position: relative; overflow: hidden;
    }}
    .left {{ flex: 1; padding: 56px 60px; display: flex; flex-direction: column; justify-content: center; }}
    .tags {{ display: flex; gap: 10px; margin-bottom: 20px; }}
    .tag {{ padding: 6px 18px; border-radius: 6px; font-size: 16px; font-weight: 700; color: #fff; }}
    .tag-b {{ background: {BRAND_COLOR}; }}
    .tag-r {{ background: #ef4444; }}
    h1 {{ font-size: 44px; font-weight: 900; color: #1e293b; line-height: 1.4; }}
    h1 em {{ font-style: normal; color: {BRAND_COLOR}; }}
    .sub {{ font-size: 20px; color: #64748b; margin-top: 12px; }}
    .right {{ width: 420px; background: #f8fafc; display: flex; flex-direction: column; justify-content: center; padding: 40px 36px; gap: 8px; }}
    .b {{
      display: block; padding: 14px 20px; background: #fff; font-size: 18px; font-weight: 700;
      color: #1e293b; border-radius: 8px;
    }}
    .ft {{ position: absolute; bottom: 16px; left: 60px; font-size: 14px; color: #94a3b8; }}
    </style></head><body>
    <div class="left">
      <div class="tags"><span class="tag tag-b">2026年版</span><span class="tag tag-r">無料</span></div>
      <h1>無料の動画編集ソフト<br><em>おすすめ7選</em></h1>
      <p class="sub">用途別に徹底比較</p>
      <div class="ft">{BRAND_NAME}</div>
    </div>
    <div class="right">{badges}</div>
    </body></html>"""
    render(html, OUT / "eyecatch-free-video-editing-software.png")


# ============================================================
# 3. 比較図: 独学 vs スクール
# ============================================================
def comparison_chart():
    def rating(symbol):
        colors = {"◎": "#16a34a", "○": "#2563eb", "△": "#f59e0b", "×": "#ef4444"}
        return f'<span style="color:{colors.get(symbol, "#333")}; font-weight:900">{symbol}</span>'

    rows = [
        ("費用", "月額〜数千円", rating("◎"), "15万〜40万円", rating("△")),
        ("期間", "3〜6ヶ月", rating("○"), "2〜6ヶ月", rating("◎")),
        ("挫折率", "高い（7〜8割）", rating("×"), "低い（2〜3割）", rating("◎")),
        ("質問対応", "自力で調べる", rating("△"), "講師・メンター対応", rating("◎")),
        ("案件サポート", "なし", rating("×"), "あり（添削・紹介）", rating("◎")),
        ("学習効率", "取捨選択に時間", rating("△"), "カリキュラムで最短", rating("◎")),
    ]
    trs = ""
    for label, v1, r1, v2, r2 in rows:
        trs += f"""<tr>
          <td class="lbl">{label}</td>
          <td class="val">{v1}</td><td class="rt">{r1}</td>
          <td class="val">{v2}</td><td class="rt">{r2}</td>
        </tr>"""

    body = f"""<style>
    table {{ width: 100%; border-collapse: collapse; }}
    thead th {{
      padding: 16px 12px; font-size: 18px; font-weight: 900; text-align: center;
      border-bottom: 3px solid #e5e7eb;
    }}
    .th-self {{ color: #2563eb; }}
    .th-school {{ color: #ea580c; }}
    td {{ padding: 20px 12px; border-bottom: 1px solid #f1f5f9; font-size: 20px; }}
    .lbl {{ font-size: 16px; color: #94a3b8; font-weight: 700; width: 100px; }}
    .val {{ font-weight: 500; color: #334155; }}
    .rt {{ width: 48px; font-size: 28px; text-align: center; }}
    </style>
    <table>
      <thead>
        <tr>
          <th></th>
          <th class="th-self" colspan="2">独学</th>
          <th class="th-school" colspan="2">スクール</th>
        </tr>
      </thead>
      <tbody>{trs}</tbody>
    </table>"""
    render(wrap("独学 vs スクール 比較", body, "どちらが自分に合っている？"), OUT / "comparison-self-vs-school.png")


# ============================================================
# 4. ロードマップ: 4ステップ（縦フロー）
# ============================================================
def roadmap():
    steps = [
        ("STEP 1", "1週目", "環境整備", "ソフト契約・PC準備", BRAND_COLOR),
        ("STEP 2", "2〜8週目", "基礎習得", "カット・テロップ・BGM・補正", "#0891b2"),
        ("STEP 3", "9〜12週目", "作品制作", "ポートフォリオを3本作る", "#16a34a"),
        ("STEP 4", "12週目〜", "案件応募", "CW・ランサーズで初受注を目指す", "#ea580c"),
    ]
    cards = ""
    for i, (num, period, title, desc, color) in enumerate(steps):
        cards += f"""
        <div class="step">
          <div class="num" style="background:{color}">{num}</div>
          <div class="body">
            <div class="meta"><span class="period">{period}</span></div>
            <div class="title">{title}</div>
            <div class="desc">{desc}</div>
          </div>
        </div>"""
        if i < len(steps) - 1:
            cards += '<div class="arrow">↓</div>'

    body = f"""<style>
    .step {{ display: flex; align-items: center; gap: 24px; }}
    .num {{
      width: 100px; height: 44px; border-radius: 8px; color: #fff;
      font-size: 16px; font-weight: 900; display: flex; align-items: center; justify-content: center;
      flex-shrink: 0;
    }}
    .body {{ flex: 1; }}
    .period {{ font-size: 15px; color: #94a3b8; }}
    .title {{ font-size: 28px; font-weight: 900; color: #1e293b; margin: 4px 0; }}
    .desc {{ font-size: 18px; color: #64748b; }}
    .arrow {{ text-align: center; font-size: 24px; color: #d1d5db; padding: 8px 0; margin-left: 38px; }}
    </style>
    {cards}"""
    render(wrap("未経験からの学習ロードマップ", body, "4ステップで最初の案件獲得へ"), OUT / "roadmap-4steps.png")


# ============================================================
# 5. 用途別おすすめマトリクス
# ============================================================
def usage_matrix():
    data = [
        ("ショート動画（TikTok・Reels）", "CapCut", "#00d1ff"),
        ("YouTube（長尺・本格）", "DaVinci Resolve", "#ff6b35"),
        ("Mac・iPhoneで手軽に", "iMovie", "#a855f7"),
        ("Windowsで今すぐ", "Clipchamp", "#3b82f6"),
        ("SNSバナー動画・広告", "Canva", "#06b6d4"),
        ("広告なし・制限なし", "Shotcut", "#84cc16"),
        ("操作感を試したい", "Filmora（無料版）", "#f59e0b"),
    ]
    rows = ""
    for usage, soft, color in data:
        rows += f"""
        <div class="row">
          <div class="dot" style="background:{color}"></div>
          <div class="usage">{usage}</div>
          <div class="soft">{soft}</div>
        </div>"""

    body = f"""<style>
    .row {{
      display: flex; align-items: center; padding: 20px 0;
      border-bottom: 1px solid #f1f5f9; gap: 16px;
    }}
    .row:last-child {{ border: none; }}
    .dot {{ width: 12px; height: 12px; border-radius: 50%; flex-shrink: 0; }}
    .usage {{ flex: 1; font-size: 22px; color: #334155; }}
    .soft {{ font-size: 22px; font-weight: 900; color: #1e293b; text-align: right; }}
    </style>
    {rows}"""
    render(wrap("用途別おすすめソフト早見表", body, "やりたいことから選ぶ"), OUT / "usage-matrix.png")


# ============================================================
# 6. 収入ロードマップ
# ============================================================
def income_chart():
    stages = [
        ("0〜3ヶ月", "学習期間", "0円", "10%", "#93c5fd"),
        ("3〜6ヶ月", "初案件期", "月1〜3万円", "30%", "#86efac"),
        ("6ヶ月〜1年", "成長期", "月5〜15万円", "60%", "#fdba74"),
        ("1年以上", "安定期", "月20万円〜", "90%", "#fca5a5"),
    ]
    rows = ""
    for period, label, amount, width, color in stages:
        rows += f"""
        <div class="stage">
          <div class="left">
            <div class="period">{period}</div>
            <div class="label">{label}</div>
          </div>
          <div class="right">
            <div class="amount">{amount}</div>
            <div class="bar-bg"><div class="bar" style="width:{width}; background:{color}"></div></div>
          </div>
        </div>"""

    body = f"""<style>
    .stage {{ display: flex; align-items: center; padding: 24px 0; border-bottom: 1px solid #f1f5f9; gap: 24px; }}
    .stage:last-child {{ border: none; }}
    .left {{ width: 160px; flex-shrink: 0; }}
    .period {{ font-size: 18px; font-weight: 700; color: #1e293b; }}
    .label {{ font-size: 15px; color: #94a3b8; }}
    .right {{ flex: 1; }}
    .amount {{ font-size: 28px; font-weight: 900; color: #1e293b; margin-bottom: 8px; }}
    .bar-bg {{ height: 20px; background: #f1f5f9; border-radius: 10px; overflow: hidden; }}
    .bar {{ height: 100%; border-radius: 10px; }}
    </style>
    {rows}"""
    render(wrap("未経験からの収入イメージ", body, "副業〜本業化までの目安"), OUT / "income-roadmap.png")


# ============================================================
def main():
    print("画像を生成中（マイベスト風デザイン）...\n")
    try:
        eyecatch_beginner()
        eyecatch_free_software()
        comparison_chart()
        roadmap()
        usage_matrix()
        income_chart()
    except Exception as e:
        print(f"\n❌ エラー: {e}", file=sys.stderr)
        print("  pip install playwright && playwright install chromium", file=sys.stderr)
        return 1
    print(f"\n完了！出力先: {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
