"""
HTML/CSS + Playwright で高品質な記事画像を生成するスクリプト（v2: モバイル最適化版）

原則:
- 1画像1メッセージ
- スマホ（400px表示）で読めるフォントサイズ
- 縦長レイアウト優先
- 横並びは2列まで

使い方:
  python scripts/generate_images_v2.py

出力先: articles/images/
依存: pip install playwright && playwright install chromium
"""
from __future__ import annotations

import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "articles" / "images"
OUT.mkdir(parents=True, exist_ok=True)

# 幅は1200px固定。高さはコンテンツに合わせてauto。
WIDTH = 1200


def render(html: str, path: Path):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": WIDTH, "height": 800}, device_scale_factor=2)
        page.set_content(html, wait_until="networkidle")
        page.screenshot(path=str(path), type="png", full_page=True)
        browser.close()
    print(f"✅ {path.name}")


CSS = """
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700;900&display=swap');
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Noto Sans JP', sans-serif; -webkit-font-smoothing: antialiased; }
"""


# ============================================================
# 1. アイキャッチ: 動画編集 未経験
# ============================================================
def eyecatch_beginner():
    html = f"""<!DOCTYPE html><html><head><style>
    {CSS}
    body {{
      width: {WIDTH}px; height: 630px;
      background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
      display: flex; flex-direction: column; justify-content: center; padding: 60px 70px;
      position: relative; overflow: hidden;
    }}
    .bar-top {{ position: absolute; top: 0; left: 0; right: 0; height: 6px; background: linear-gradient(90deg, #e94560, #ff6b6b); }}
    .tag {{
      display: inline-block; background: #e94560; color: #fff; padding: 8px 24px;
      border-radius: 8px; font-size: 20px; font-weight: 700; margin-bottom: 28px;
    }}
    h1 {{ color: #fff; font-size: 56px; font-weight: 900; line-height: 1.35; }}
    h1 em {{ font-style: normal; color: #fbbf24; }}
    .sub {{ color: #94a3b8; font-size: 26px; margin-top: 20px; line-height: 1.5; }}
    .play {{
      position: absolute; right: 80px; top: 50%; transform: translateY(-50%);
      width: 150px; height: 150px; border-radius: 50%;
      background: linear-gradient(135deg, #e94560, #ff6b6b);
      box-shadow: 0 12px 40px rgba(233,69,96,0.35);
      display: flex; align-items: center; justify-content: center;
    }}
    .play::after {{ content:''; border-left: 40px solid #fff; border-top: 24px solid transparent; border-bottom: 24px solid transparent; margin-left: 8px; }}
    .foot {{ position: absolute; bottom: 28px; left: 70px; color: #475569; font-size: 17px; }}
    </style></head><body>
    <div class="bar-top"></div>
    <span class="tag">2026年版</span>
    <h1>動画編集は<br><em>未経験でも始められる？</em></h1>
    <p class="sub">失敗しない始め方とおすすめスクール</p>
    <div class="play"></div>
    <div class="foot">独学 vs スクール ／ 4ステップロードマップ ／ 失敗パターン5選　｜　大人の学びなおし比較</div>
    </body></html>"""
    render(html, OUT / "eyecatch-video-editing-beginner.png")


# ============================================================
# 2. アイキャッチ: 無料動画編集ソフト比較
# ============================================================
def eyecatch_free_software():
    badges = "".join(
        f'<span class="b" style="background:linear-gradient(135deg,{c1},{c2})">{name}</span>'
        for name, c1, c2 in [
            ("CapCut", "#00d1ff", "#0891b2"), ("DaVinci Resolve", "#ff6b35", "#ea580c"),
            ("iMovie", "#a855f7", "#7c3aed"), ("Clipchamp", "#3b82f6", "#2563eb"),
            ("Canva", "#06b6d4", "#0284c7"), ("Shotcut", "#84cc16", "#65a30d"),
            ("Filmora", "#f59e0b", "#d97706"),
        ]
    )
    html = f"""<!DOCTYPE html><html><head><style>
    {CSS}
    body {{
      width: {WIDTH}px; height: 630px;
      background: linear-gradient(135deg, #0f172a, #1e293b);
      display: flex; padding: 60px 70px; position: relative; overflow: hidden;
    }}
    .bar-top {{ position: absolute; top: 0; left: 0; right: 0; height: 6px; background: linear-gradient(90deg, #22c55e, #06b6d4); }}
    .left {{ flex: 1; display: flex; flex-direction: column; justify-content: center; }}
    .tags {{ display: flex; gap: 12px; margin-bottom: 28px; }}
    .tag {{ padding: 8px 24px; border-radius: 8px; font-size: 18px; font-weight: 700; color: #fff; }}
    .tg {{ background: #22c55e; }}
    .tr {{ background: #e94560; }}
    h1 {{ color: #fff; font-size: 52px; font-weight: 900; line-height: 1.35; }}
    h1 em {{ font-style: normal; color: #fbbf24; }}
    .sub {{ color: #94a3b8; font-size: 24px; margin-top: 16px; }}
    .right {{ width: 400px; display: flex; flex-direction: column; justify-content: center; gap: 10px; padding-left: 40px; }}
    .b {{ display: block; padding: 14px 24px; border-radius: 10px; color: #fff; font-size: 20px; font-weight: 700; }}
    .foot {{ position: absolute; bottom: 24px; left: 70px; color: #475569; font-size: 16px; }}
    </style></head><body>
    <div class="bar-top"></div>
    <div class="left">
      <div class="tags"><span class="tag tg">2026年版</span><span class="tag tr">無料</span></div>
      <h1>無料の動画編集ソフト<br><em>おすすめ7選</em></h1>
      <p class="sub">用途別に徹底比較</p>
    </div>
    <div class="right">{badges}</div>
    <div class="foot">スマホ用 ／ PC用 ／ YouTube用 ／ SNS用　｜　大人の学びなおし比較</div>
    </body></html>"""
    render(html, OUT / "eyecatch-free-video-editing-software.png")


# ============================================================
# 3. 比較図: 独学 vs スクール（縦積み・大文字）
# ============================================================
def comparison_chart():
    def card(title, color, items):
        rows = "".join(f'<div class="row"><span class="lbl">{l}</span><span class="val" style="color:{c}">{v}</span></div>' for l, v, c in items)
        return f'<div class="card"><div class="hd" style="background:linear-gradient(135deg,{color[0]},{color[1]})">{title}</div><div class="bd">{rows}</div></div>'

    left = card("独学", ("#3b82f6", "#2563eb"), [
        ("費用", "月額〜数千円", "#16a34a"),
        ("期間", "3〜6ヶ月（個人差大）", "#475569"),
        ("挫折率", "高い（7〜8割）", "#ea580c"),
        ("質問", "自力で調べる", "#475569"),
        ("案件サポート", "なし", "#ea580c"),
        ("学習効率", "情報の取捨選択に時間", "#475569"),
    ])
    right = card("スクール", ("#f97316", "#ea580c"), [
        ("費用", "15万〜40万円", "#ea580c"),
        ("期間", "2〜6ヶ月（カリキュラム化）", "#16a34a"),
        ("挫折率", "低い（2〜3割）", "#16a34a"),
        ("質問", "講師・メンター対応", "#16a34a"),
        ("案件サポート", "あり（添削・紹介）", "#16a34a"),
        ("学習効率", "カリキュラムで最短", "#16a34a"),
    ])

    html = f"""<!DOCTYPE html><html><head><style>
    {CSS}
    body {{ width: {WIDTH}px; background: #f8fafc; padding: 48px 60px; }}
    h2 {{ text-align: center; font-size: 36px; color: #1e293b; margin-bottom: 36px; }}
    .wrap {{ display: flex; gap: 32px; }}
    .card {{ flex: 1; border-radius: 20px; overflow: hidden; box-shadow: 0 4px 24px rgba(0,0,0,0.08); }}
    .hd {{ padding: 24px; text-align: center; color: #fff; font-size: 32px; font-weight: 900; }}
    .bd {{ background: #fff; padding: 8px 28px; }}
    .row {{ display: flex; justify-content: space-between; align-items: center; padding: 20px 0; border-bottom: 1px solid #f1f5f9; }}
    .row:last-child {{ border: none; }}
    .lbl {{ font-size: 18px; color: #94a3b8; font-weight: 700; min-width: 120px; }}
    .val {{ font-size: 24px; font-weight: 900; text-align: right; }}
    .vs {{
      display: flex; align-items: center; justify-content: center; align-self: center;
      width: 64px; height: 64px; border-radius: 50%; flex-shrink: 0;
      background: #1e293b; color: #fff; font-weight: 900; font-size: 22px;
      box-shadow: 0 4px 16px rgba(0,0,0,0.2);
    }}
    </style></head><body>
    <h2>独学 vs スクール 比較</h2>
    <div class="wrap">{left}<div class="vs">VS</div>{right}</div>
    </body></html>"""
    render(html, OUT / "comparison-self-vs-school.png")


# ============================================================
# 4. ロードマップ: 4ステップ（縦フロー）
# ============================================================
def roadmap():
    steps = [
        ("STEP 1", "1週目", "環境整備", "ソフト契約・PC準備", "#2c3e7b", "#3b5998"),
        ("STEP 2", "2〜8週目", "基礎習得", "カット・テロップ・BGM・補正", "#1976d2", "#42a5f5"),
        ("STEP 3", "9〜12週目", "作品制作", "ポートフォリオを3本作る", "#2e7d32", "#66bb6a"),
        ("STEP 4", "12週目〜", "案件応募", "CW・ランサーズで初受注を目指す", "#c62828", "#ef5350"),
    ]
    cards = ""
    for i, (num, period, title, desc, c1, c2) in enumerate(steps):
        cards += f"""
        <div class="step" style="background:linear-gradient(135deg,{c1},{c2})">
          <div class="step-head">
            <span class="num">{num}</span>
            <span class="period">{period}</span>
          </div>
          <div class="step-title">{title}</div>
          <div class="step-desc">{desc}</div>
        </div>
        """
        if i < len(steps) - 1:
            cards += '<div class="arrow">▼</div>'

    html = f"""<!DOCTYPE html><html><head><style>
    {CSS}
    body {{ width: {WIDTH}px; background: #f8fafc; padding: 48px 200px; }}
    h2 {{ font-size: 32px; color: #1e293b; margin-bottom: 36px; text-align: center; }}
    .steps {{ display: flex; flex-direction: column; align-items: stretch; }}
    .step {{
      border-radius: 16px; padding: 32px 36px; color: #fff;
      box-shadow: 0 4px 20px rgba(0,0,0,0.12);
    }}
    .step-head {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }}
    .num {{ font-size: 18px; font-weight: 700; opacity: 0.85; }}
    .period {{ font-size: 16px; opacity: 0.7; }}
    .step-title {{ font-size: 36px; font-weight: 900; margin-bottom: 8px; }}
    .step-desc {{ font-size: 22px; opacity: 0.9; }}
    .arrow {{ text-align: center; font-size: 32px; color: #94a3b8; padding: 8px 0; }}
    </style></head><body>
    <h2>未経験からの学習ロードマップ</h2>
    <div class="steps">{cards}</div>
    </body></html>"""
    render(html, OUT / "roadmap-4steps.png")


# ============================================================
# 5. 用途別おすすめマトリクス（2列・大フォント）
# ============================================================
def usage_matrix():
    rows_data = [
        ("ショート動画\n（TikTok・Reels）", "CapCut", "#00d1ff", "#0891b2"),
        ("YouTube\n（長尺・本格）", "DaVinci Resolve", "#ff6b35", "#ea580c"),
        ("Mac・iPhoneで\n手軽に", "iMovie", "#a855f7", "#7c3aed"),
        ("Windowsで\n今すぐ", "Clipchamp", "#3b82f6", "#2563eb"),
        ("SNSバナー\n動画・広告", "Canva", "#06b6d4", "#0284c7"),
        ("広告なし\n制限なし", "Shotcut", "#84cc16", "#65a30d"),
        ("操作感を\n試したい", "Filmora（無料版）", "#f59e0b", "#d97706"),
    ]
    rows = ""
    for usage, soft, c1, c2 in rows_data:
        usage_html = usage.replace("\n", "<br>")
        rows += f"""
        <div class="row">
          <div class="usage">{usage_html}</div>
          <div class="soft" style="background:linear-gradient(135deg,{c1},{c2})">{soft}</div>
        </div>"""

    html = f"""<!DOCTYPE html><html><head><style>
    {CSS}
    body {{ width: {WIDTH}px; background: #f8fafc; padding: 48px 60px; }}
    h2 {{ font-size: 32px; color: #1e293b; margin-bottom: 32px; text-align: center; }}
    .row {{
      display: flex; align-items: center; background: #fff; border-radius: 14px;
      margin-bottom: 12px; padding: 20px 32px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }}
    .usage {{ flex: 1; font-size: 24px; font-weight: 700; color: #334155; line-height: 1.4; }}
    .soft {{
      padding: 16px 36px; border-radius: 12px; color: #fff;
      font-size: 24px; font-weight: 900; white-space: nowrap;
      box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }}
    </style></head><body>
    <h2>用途別おすすめソフト早見表</h2>
    {rows}
    </body></html>"""
    render(html, OUT / "usage-matrix.png")


# ============================================================
# 6. 収入ロードマップ（縦ステップ）
# ============================================================
def income_chart():
    stages = [
        ("0〜3ヶ月", "学習期間", "0円", "#3b82f6", "#93c5fd"),
        ("3〜6ヶ月", "初案件期", "月1〜3万円", "#22c55e", "#86efac"),
        ("6ヶ月〜1年", "成長期", "月5〜15万円", "#f97316", "#fdba74"),
        ("1年以上", "安定期", "月20万円〜", "#ef4444", "#fca5a5"),
    ]
    cards = ""
    for period, label, amount, c1, c2 in stages:
        cards += f"""
        <div class="stage">
          <div class="period">{period}</div>
          <div class="body" style="background:linear-gradient(135deg,{c1},{c2})">
            <div class="amount">{amount}</div>
            <div class="label">{label}</div>
          </div>
        </div>"""

    html = f"""<!DOCTYPE html><html><head><style>
    {CSS}
    body {{ width: {WIDTH}px; background: #f8fafc; padding: 48px 120px; }}
    h2 {{ font-size: 32px; color: #1e293b; margin-bottom: 36px; text-align: center; }}
    .stages {{ display: flex; flex-direction: column; gap: 16px; }}
    .stage {{ display: flex; align-items: center; gap: 24px; }}
    .period {{ width: 160px; font-size: 20px; font-weight: 700; color: #64748b; text-align: right; }}
    .body {{
      flex: 1; border-radius: 14px; padding: 24px 32px; color: #fff;
      box-shadow: 0 4px 16px rgba(0,0,0,0.1);
    }}
    .amount {{ font-size: 36px; font-weight: 900; }}
    .label {{ font-size: 18px; opacity: 0.85; margin-top: 4px; }}
    </style></head><body>
    <h2>未経験からの収入イメージ</h2>
    <div class="stages">{cards}</div>
    </body></html>"""
    render(html, OUT / "income-roadmap.png")


# ============================================================
def main():
    print("高品質画像を生成中（モバイル最適化版）...\n")
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
