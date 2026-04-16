"""
HTML/CSS + Playwright で高品質な記事画像を生成するスクリプト

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


def render_html_to_png(html: str, path: Path, width: int = 1200, height: int = 630):
    """HTML文字列をPNG画像に変換"""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=2)
        page.set_content(html, wait_until="networkidle")
        page.screenshot(path=str(path), type="png", full_page=True)
        browser.close()
    print(f"✅ {path.name} ({width}x auto)")


# ============================================================
# 共通CSS
# ============================================================
BASE_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700;900&display=swap');
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: 'Noto Sans JP', sans-serif;
  -webkit-font-smoothing: antialiased;
}
"""


# ============================================================
# 1. アイキャッチ: 動画編集 未経験
# ============================================================
def eyecatch_beginner():
    html = f"""<!DOCTYPE html><html><head><style>
    {BASE_CSS}
    body {{
      width: 1200px; height: 630px;
      background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
      display: flex; flex-direction: column; justify-content: center; padding: 60px;
      position: relative; overflow: hidden;
    }}
    .accent-top {{ position: absolute; top: 0; left: 0; right: 0; height: 6px; background: linear-gradient(90deg, #e94560, #ff6b6b); }}
    .accent-bottom {{ position: absolute; bottom: 0; left: 0; right: 0; height: 6px; background: linear-gradient(90deg, #e94560, #ff6b6b); }}
    .tag {{
      display: inline-block; background: #e94560; color: white; padding: 6px 20px;
      border-radius: 6px; font-size: 18px; font-weight: 700; margin-bottom: 24px;
    }}
    h1 {{ color: white; font-size: 52px; font-weight: 900; line-height: 1.3; margin-bottom: 16px; }}
    h1 .highlight {{ color: #ffc107; }}
    .subtitle {{ color: #b0b8c8; font-size: 24px; line-height: 1.6; }}
    .play-btn {{
      position: absolute; right: 80px; top: 50%; transform: translateY(-50%);
      width: 140px; height: 140px; border-radius: 50%;
      background: linear-gradient(135deg, #e94560, #ff6b6b);
      display: flex; align-items: center; justify-content: center;
      box-shadow: 0 8px 32px rgba(233,69,96,0.4);
    }}
    .play-btn::after {{
      content: ''; width: 0; height: 0;
      border-left: 36px solid white; border-top: 22px solid transparent; border-bottom: 22px solid transparent;
      margin-left: 8px;
    }}
    .footer {{ position: absolute; bottom: 30px; left: 60px; color: #5a6580; font-size: 16px; }}
    .circle1 {{ position: absolute; top: -60px; right: 200px; width: 200px; height: 200px; border-radius: 50%; background: rgba(233,69,96,0.08); }}
    .circle2 {{ position: absolute; bottom: -40px; right: 400px; width: 150px; height: 150px; border-radius: 50%; background: rgba(15,52,96,0.3); }}
    </style></head><body>
    <div class="accent-top"></div>
    <div class="accent-bottom"></div>
    <div class="circle1"></div>
    <div class="circle2"></div>
    <span class="tag">2026年版</span>
    <h1>動画編集は<br><span class="highlight">未経験でも始められる？</span></h1>
    <p class="subtitle">失敗しない始め方とおすすめスクール</p>
    <div class="play-btn"></div>
    <div class="footer">独学 vs スクール ／ 4ステップロードマップ ／ 失敗パターン5選　｜　大人の学びなおし比較</div>
    </body></html>"""
    render_html_to_png(html, OUT / "eyecatch-video-editing-beginner.png")


# ============================================================
# 2. アイキャッチ: 無料動画編集ソフト比較
# ============================================================
def eyecatch_free_software():
    html = f"""<!DOCTYPE html><html><head><style>
    {BASE_CSS}
    body {{
      width: 1200px; height: 630px;
      background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
      display: flex; padding: 60px; position: relative; overflow: hidden;
    }}
    .accent-top {{ position: absolute; top: 0; left: 0; right: 0; height: 6px; background: linear-gradient(90deg, #22c55e, #06b6d4); }}
    .left {{ flex: 1; display: flex; flex-direction: column; justify-content: center; }}
    .tags {{ margin-bottom: 24px; display: flex; gap: 12px; }}
    .tag {{ padding: 6px 20px; border-radius: 6px; font-size: 16px; font-weight: 700; color: white; }}
    .tag-green {{ background: #22c55e; }}
    .tag-red {{ background: #e94560; }}
    h1 {{ color: white; font-size: 48px; font-weight: 900; line-height: 1.3; margin-bottom: 16px; }}
    h1 .highlight {{ color: #fbbf24; }}
    .subtitle {{ color: #94a3b8; font-size: 22px; }}
    .right {{ width: 380px; display: flex; flex-direction: column; justify-content: center; gap: 12px; padding-left: 40px; }}
    .soft-badge {{
      padding: 12px 24px; border-radius: 10px; color: white; font-size: 18px; font-weight: 700;
      box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }}
    .footer {{ position: absolute; bottom: 24px; left: 60px; color: #475569; font-size: 15px; }}
    </style></head><body>
    <div class="accent-top"></div>
    <div class="left">
      <div class="tags"><span class="tag tag-green">2026年版</span><span class="tag tag-red">無料</span></div>
      <h1>無料の動画編集ソフト<br><span class="highlight">おすすめ7選</span></h1>
      <p class="subtitle">用途別に徹底比較</p>
    </div>
    <div class="right">
      <div class="soft-badge" style="background:linear-gradient(135deg,#00d1ff,#0891b2)">CapCut</div>
      <div class="soft-badge" style="background:linear-gradient(135deg,#ff6b35,#ea580c)">DaVinci Resolve</div>
      <div class="soft-badge" style="background:linear-gradient(135deg,#a855f7,#7c3aed)">iMovie</div>
      <div class="soft-badge" style="background:linear-gradient(135deg,#3b82f6,#2563eb)">Clipchamp</div>
      <div class="soft-badge" style="background:linear-gradient(135deg,#06b6d4,#0284c7)">Canva</div>
      <div class="soft-badge" style="background:linear-gradient(135deg,#84cc16,#65a30d)">Shotcut</div>
      <div class="soft-badge" style="background:linear-gradient(135deg,#f59e0b,#d97706)">Filmora</div>
    </div>
    <div class="footer">スマホ用 ／ PC用 ／ YouTube用 ／ SNS用　｜　大人の学びなおし比較</div>
    </body></html>"""
    render_html_to_png(html, OUT / "eyecatch-free-video-editing-software.png")


# ============================================================
# 3. 比較図: 独学 vs スクール
# ============================================================
def comparison_chart():
    html = f"""<!DOCTYPE html><html><head><style>
    {BASE_CSS}
    body {{ width: 1200px; height: 700px; background: #f8fafc; padding: 40px; }}
    h2 {{ text-align: center; font-size: 32px; color: #1e293b; margin-bottom: 32px; }}
    .container {{ display: flex; gap: 24px; height: 580px; }}
    .card {{
      flex: 1; border-radius: 20px; overflow: hidden;
      box-shadow: 0 4px 24px rgba(0,0,0,0.08);
    }}
    .card-header {{ padding: 20px; text-align: center; color: white; font-size: 26px; font-weight: 900; }}
    .card-body {{ padding: 24px; background: white; }}
    .row {{ padding: 16px 0; border-bottom: 1px solid #f1f5f9; }}
    .row:last-child {{ border-bottom: none; }}
    .label {{ font-size: 13px; color: #94a3b8; margin-bottom: 4px; font-weight: 700; }}
    .value {{ font-size: 20px; font-weight: 700; }}
    .blue .card-header {{ background: linear-gradient(135deg, #3b82f6, #2563eb); }}
    .orange .card-header {{ background: linear-gradient(135deg, #f97316, #ea580c); }}
    .vs {{
      display: flex; align-items: center; justify-content: center;
      width: 56px; height: 56px; border-radius: 50%;
      background: #1e293b; color: white; font-weight: 900; font-size: 18px;
      align-self: center; flex-shrink: 0;
      box-shadow: 0 4px 16px rgba(0,0,0,0.2);
    }}
    .good {{ color: #16a34a; }}
    .warn {{ color: #ea580c; }}
    .neutral {{ color: #475569; }}
    </style></head><body>
    <h2>独学 vs スクール 比較</h2>
    <div class="container">
      <div class="card blue">
        <div class="card-header">独学</div>
        <div class="card-body">
          <div class="row"><div class="label">費用</div><div class="value good">月額〜数千円</div></div>
          <div class="row"><div class="label">期間</div><div class="value neutral">3〜6ヶ月（個人差大）</div></div>
          <div class="row"><div class="label">挫折率</div><div class="value warn">高い（7〜8割）</div></div>
          <div class="row"><div class="label">質問対応</div><div class="value neutral">自力で調べる</div></div>
          <div class="row"><div class="label">案件サポート</div><div class="value warn">なし</div></div>
          <div class="row"><div class="label">学習効率</div><div class="value neutral">情報の取捨選択に時間</div></div>
        </div>
      </div>
      <div class="vs">VS</div>
      <div class="card orange">
        <div class="card-header">スクール</div>
        <div class="card-body">
          <div class="row"><div class="label">費用</div><div class="value warn">15万〜40万円</div></div>
          <div class="row"><div class="label">期間</div><div class="value good">2〜6ヶ月（カリキュラム化）</div></div>
          <div class="row"><div class="label">挫折率</div><div class="value good">低い（2〜3割）</div></div>
          <div class="row"><div class="label">質問対応</div><div class="value good">講師・メンター対応</div></div>
          <div class="row"><div class="label">案件サポート</div><div class="value good">あり（添削・紹介）</div></div>
          <div class="row"><div class="label">学習効率</div><div class="value good">カリキュラムで最短</div></div>
        </div>
      </div>
    </div>
    </body></html>"""
    render_html_to_png(html, OUT / "comparison-self-vs-school.png", 1200, 700)


# ============================================================
# 4. ロードマップ: 4ステップ
# ============================================================
def roadmap():
    html = f"""<!DOCTYPE html><html><head><style>
    {BASE_CSS}
    body {{ width: 1200px; height: 480px; background: #f8fafc; padding: 40px; }}
    h2 {{ font-size: 28px; color: #1e293b; margin-bottom: 32px; }}
    .steps {{ display: flex; gap: 16px; align-items: stretch; }}
    .step {{
      flex: 1; border-radius: 16px; padding: 28px; color: white; position: relative;
      display: flex; flex-direction: column;
      box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    }}
    .step-num {{ font-size: 14px; font-weight: 700; opacity: 0.8; margin-bottom: 4px; }}
    .step-period {{ font-size: 12px; opacity: 0.7; margin-bottom: 16px; }}
    .step-title {{ font-size: 24px; font-weight: 900; margin-bottom: 12px; }}
    .step-desc {{ font-size: 15px; line-height: 1.6; opacity: 0.9; }}
    .s1 {{ background: linear-gradient(135deg, #1e3a5f, #2c3e7b); }}
    .s2 {{ background: linear-gradient(135deg, #1976d2, #42a5f5); }}
    .s3 {{ background: linear-gradient(135deg, #2e7d32, #66bb6a); }}
    .s4 {{ background: linear-gradient(135deg, #c62828, #ef5350); }}
    .arrow {{
      display: flex; align-items: center; justify-content: center; flex-shrink: 0;
      font-size: 28px; color: #94a3b8; width: 24px;
    }}
    </style></head><body>
    <h2>未経験からの学習ロードマップ（4ステップ）</h2>
    <div class="steps">
      <div class="step s1">
        <div class="step-num">STEP 1</div><div class="step-period">1週目</div>
        <div class="step-title">環境整備</div>
        <div class="step-desc">ソフト契約<br>PC準備</div>
      </div>
      <div class="arrow">▶</div>
      <div class="step s2">
        <div class="step-num">STEP 2</div><div class="step-period">2〜8週目</div>
        <div class="step-title">基礎習得</div>
        <div class="step-desc">カット・テロップ<br>BGM・補正</div>
      </div>
      <div class="arrow">▶</div>
      <div class="step s3">
        <div class="step-num">STEP 3</div><div class="step-period">9〜12週目</div>
        <div class="step-title">作品制作</div>
        <div class="step-desc">ポートフォリオ<br>3本作る</div>
      </div>
      <div class="arrow">▶</div>
      <div class="step s4">
        <div class="step-num">STEP 4</div><div class="step-period">12週目〜</div>
        <div class="step-title">案件応募</div>
        <div class="step-desc">CW・ランサーズ<br>初受注を目指す</div>
      </div>
    </div>
    </body></html>"""
    render_html_to_png(html, OUT / "roadmap-4steps.png", 1200, 480)


# ============================================================
# 5. 用途別おすすめマトリクス
# ============================================================
def usage_matrix():
    html = f"""<!DOCTYPE html><html><head><style>
    {BASE_CSS}
    body {{ width: 1200px; height: 600px; background: #f8fafc; padding: 40px; }}
    h2 {{ font-size: 28px; color: #1e293b; margin-bottom: 24px; }}
    table {{ width: 100%; border-collapse: separate; border-spacing: 0; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 12px rgba(0,0,0,0.06); }}
    th {{ background: #1e293b; color: white; padding: 16px 24px; text-align: left; font-size: 16px; }}
    td {{ padding: 16px 24px; font-size: 17px; border-bottom: 1px solid #e2e8f0; background: white; }}
    tr:last-child td {{ border-bottom: none; }}
    tr:nth-child(even) td {{ background: #f8fafc; }}
    .badge {{
      display: inline-block; padding: 8px 24px; border-radius: 8px;
      color: white; font-weight: 700; font-size: 16px;
    }}
    </style></head><body>
    <h2>用途別おすすめソフト早見表</h2>
    <table>
      <tr><th>やりたいこと</th><th>おすすめソフト</th><th>理由</th></tr>
      <tr><td>ショート動画（TikTok・Reels）</td><td><span class="badge" style="background:linear-gradient(135deg,#00d1ff,#0891b2)">CapCut</span></td><td>テンプレ＋自動字幕でスマホ完結</td></tr>
      <tr><td>YouTube（長尺・本格）</td><td><span class="badge" style="background:linear-gradient(135deg,#ff6b35,#ea580c)">DaVinci Resolve</span></td><td>無料でプロ仕様。4K書き出し可</td></tr>
      <tr><td>Mac・iPhoneで手軽に</td><td><span class="badge" style="background:linear-gradient(135deg,#a855f7,#7c3aed)">iMovie</span></td><td>標準搭載。学習コスト最小</td></tr>
      <tr><td>Windowsで今すぐ</td><td><span class="badge" style="background:linear-gradient(135deg,#3b82f6,#2563eb)">Clipchamp</span></td><td>インストール不要。即起動</td></tr>
      <tr><td>SNSバナー動画・広告</td><td><span class="badge" style="background:linear-gradient(135deg,#06b6d4,#0284c7)">Canva</span></td><td>テンプレ最強。デザインごと作れる</td></tr>
      <tr><td>広告なし・制限なし</td><td><span class="badge" style="background:linear-gradient(135deg,#84cc16,#65a30d)">Shotcut</span></td><td>完全無料のオープンソース</td></tr>
      <tr><td>操作感を試したい</td><td><span class="badge" style="background:linear-gradient(135deg,#f59e0b,#d97706)">Filmora（無料版）</span></td><td>UIが親切（ただし透かしあり）</td></tr>
    </table>
    </body></html>"""
    render_html_to_png(html, OUT / "usage-matrix.png", 1200, 600)


# ============================================================
# 6. 収入ロードマップ
# ============================================================
def income_chart():
    html = f"""<!DOCTYPE html><html><head><style>
    {BASE_CSS}
    body {{ width: 1200px; height: 480px; background: #f8fafc; padding: 40px; display: flex; flex-direction: column; }}
    h2 {{ font-size: 28px; color: #1e293b; margin-bottom: 32px; }}
    .chart {{ display: flex; align-items: flex-end; gap: 32px; flex: 1; padding-bottom: 60px; position: relative; }}
    .bar-group {{ flex: 1; display: flex; flex-direction: column; align-items: center; }}
    .bar {{
      width: 100%; border-radius: 12px 12px 0 0; display: flex; flex-direction: column;
      justify-content: flex-start; padding: 20px; color: white; min-height: 40px;
      box-shadow: 0 4px 16px rgba(0,0,0,0.1);
    }}
    .bar-amount {{ font-size: 26px; font-weight: 900; }}
    .bar-label {{ font-size: 14px; opacity: 0.8; margin-top: 4px; }}
    .bar-period {{ margin-top: 12px; font-size: 17px; color: #475569; font-weight: 700; text-align: center; }}
    .b1 {{ height: 60px; background: linear-gradient(180deg, #93c5fd, #3b82f6); }}
    .b2 {{ height: 130px; background: linear-gradient(180deg, #86efac, #22c55e); }}
    .b3 {{ height: 240px; background: linear-gradient(180deg, #fdba74, #f97316); }}
    .b4 {{ height: 340px; background: linear-gradient(180deg, #fca5a5, #ef4444); }}
    </style></head><body>
    <h2>未経験からの収入イメージ</h2>
    <div class="chart">
      <div class="bar-group"><div class="bar b1"><div class="bar-amount">0円</div><div class="bar-label">学習期間</div></div><div class="bar-period">0〜3ヶ月</div></div>
      <div class="bar-group"><div class="bar b2"><div class="bar-amount">月1〜3万円</div><div class="bar-label">初案件期</div></div><div class="bar-period">3〜6ヶ月</div></div>
      <div class="bar-group"><div class="bar b3"><div class="bar-amount">月5〜15万円</div><div class="bar-label">成長期</div></div><div class="bar-period">6ヶ月〜1年</div></div>
      <div class="bar-group"><div class="bar b4"><div class="bar-amount">月20万円〜</div><div class="bar-label">安定期</div></div><div class="bar-period">1年以上</div></div>
    </div>
    </body></html>"""
    render_html_to_png(html, OUT / "income-roadmap.png", 1200, 480)


# ============================================================
# メイン
# ============================================================
def main():
    print("HTML/CSS → PNG 高品質画像を生成中...\n")
    try:
        eyecatch_beginner()
        eyecatch_free_software()
        comparison_chart()
        roadmap()
        usage_matrix()
        income_chart()
    except Exception as e:
        print(f"\n❌ エラー: {e}", file=sys.stderr)
        print("Playwrightが未インストールの場合:", file=sys.stderr)
        print("  pip install playwright && playwright install chromium", file=sys.stderr)
        return 1

    print(f"\n完了！出力先: {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
