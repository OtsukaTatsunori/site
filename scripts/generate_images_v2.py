"""記事画像生成（モバイル最適化版）
幅800px / フォント32px以上 / 1カラム / 2xRetina
"""
from __future__ import annotations
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "articles" / "images"
OUT.mkdir(parents=True, exist_ok=True)

W = 800  # スマホ400px表示で2倍 = ちょうどRetina

def render(html: str, path: Path):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": W, "height": 2000}, device_scale_factor=2)
        page.set_content(html, wait_until="networkidle")
        page.locator("body").screenshot(path=str(path), type="png")
        browser.close()
    print(f"✅ {path.name}")

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700;900&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Noto Sans JP',sans-serif;-webkit-font-smoothing:antialiased;background:#fff;width:800px}
"""
BRAND = "#2563eb"
SITE = "大人の学びなおし比較"

def hd(title, sub=""):
    s = f'<p style="font-size:16px;opacity:.7;margin-top:4px">{sub}</p>' if sub else ""
    return f'<div style="background:{BRAND};color:#fff;padding:28px 36px"><div style="font-size:28px;font-weight:900">{title}</div>{s}</div>'

def ft():
    return f'<div style="padding:16px 36px;border-top:1px solid #eee;font-size:13px;color:#aaa;text-align:right">{SITE}</div>'


# === 1. アイキャッチ: 動画編集 未経験 ===
def eyecatch_beginner():
    html = f"""<!DOCTYPE html><html><head><style>{CSS}
    body{{height:420px;background:#fff;display:flex}}
    .l{{flex:1;padding:40px 36px;display:flex;flex-direction:column;justify-content:center}}
    .r{{width:200px;background:{BRAND};display:flex;align-items:center;justify-content:center}}
    .play{{width:80px;height:80px;border-radius:50%;background:rgba(255,255,255,.2);display:flex;align-items:center;justify-content:center}}
    .play::after{{content:'';border-left:24px solid #fff;border-top:14px solid transparent;border-bottom:14px solid transparent;margin-left:4px}}
    .tag{{display:inline-block;background:{BRAND};color:#fff;padding:4px 14px;border-radius:5px;font-size:14px;font-weight:700;margin-bottom:12px}}
    h1{{font-size:32px;font-weight:900;color:#1e293b;line-height:1.4}}
    h1 em{{font-style:normal;color:{BRAND}}}
    .sub{{font-size:16px;color:#64748b;margin-top:10px}}
    .ft{{position:absolute;bottom:10px;left:36px;font-size:12px;color:#aaa}}
    </style></head><body>
    <div class="l">
      <span class="tag">2026年版</span>
      <h1>動画編集は<br><em>未経験でも始められる？</em></h1>
      <p class="sub">失敗しない始め方とおすすめスクール</p>
    </div>
    <div class="r"><div class="play"></div></div>
    </body></html>"""
    render(html, OUT / "eyecatch-video-editing-beginner.png")


# === 2. アイキャッチ: 無料ソフト比較 ===
def eyecatch_free():
    items = "".join(f'<span style="display:inline-block;padding:6px 14px;border-radius:6px;background:#f1f5f9;font-size:14px;font-weight:700;color:#334155">{n}</span>' for n in ["CapCut","DaVinci Resolve","iMovie","Clipchamp","Canva","Shotcut","Filmora"])
    html = f"""<!DOCTYPE html><html><head><style>{CSS}
    body{{height:420px;padding:40px 36px;display:flex;flex-direction:column;justify-content:center}}
    .tags{{display:flex;gap:8px;margin-bottom:12px}}
    .tag{{padding:4px 14px;border-radius:5px;font-size:14px;font-weight:700;color:#fff}}
    h1{{font-size:32px;font-weight:900;color:#1e293b;line-height:1.4}}
    h1 em{{font-style:normal;color:{BRAND}}}
    .sub{{font-size:16px;color:#64748b;margin-top:8px}}
    .chips{{display:flex;flex-wrap:wrap;gap:8px;margin-top:20px}}
    .ft{{position:absolute;bottom:10px;left:36px;font-size:12px;color:#aaa}}
    </style></head><body>
    <div class="tags"><span class="tag" style="background:{BRAND}">2026年版</span><span class="tag" style="background:#ef4444">無料</span></div>
    <h1>無料の動画編集ソフト<br><em>おすすめ7選</em></h1>
    <p class="sub">用途別に徹底比較</p>
    <div class="chips">{items}</div>
    </body></html>"""
    render(html, OUT / "eyecatch-free-video-editing-software.png")


# === 3. 独学 vs スクール（1カラム・縦並び） ===
def comparison():
    rows = [
        ("費用", "月額〜数千円", "◎", "15万〜40万円", "△"),
        ("期間", "3〜6ヶ月", "○", "2〜6ヶ月", "◎"),
        ("挫折率", "高い（7〜8割）", "×", "低い（2〜3割）", "◎"),
        ("質問対応", "自力で調べる", "△", "講師が対応", "◎"),
        ("案件サポート", "なし", "×", "あり", "◎"),
        ("学習効率", "取捨選択に時間", "△", "最短ルート", "◎"),
    ]
    rc = {"◎":"#16a34a","○":"#2563eb","△":"#f59e0b","×":"#ef4444"}
    trs = ""
    for label, v1, r1, v2, r2 in rows:
        trs += f"""<div class="row">
          <div class="label">{label}</div>
          <div class="cell"><span class="rating" style="color:{rc[r1]}">{r1}</span><span class="val">{v1}</span></div>
          <div class="cell"><span class="rating" style="color:{rc[r2]}">{r2}</span><span class="val">{v2}</span></div>
        </div>"""

    html = f"""<!DOCTYPE html><html><head><style>{CSS}
    .hdr{{display:flex;padding:0 36px}}
    .hdr-blank{{width:100px}}
    .hdr-col{{flex:1;text-align:center;padding:16px 0;font-size:20px;font-weight:900}}
    .row{{display:flex;align-items:center;padding:16px 36px;border-bottom:1px solid #f1f5f9}}
    .label{{width:100px;font-size:15px;color:#94a3b8;font-weight:700}}
    .cell{{flex:1;display:flex;align-items:center;gap:10px}}
    .rating{{font-size:28px;font-weight:900;width:36px;text-align:center}}
    .val{{font-size:18px;font-weight:700;color:#334155}}
    </style></head><body>
    {hd("独学 vs スクール 比較","どちらが自分に合っている？")}
    <div class="hdr"><div class="hdr-blank"></div><div class="hdr-col" style="color:#2563eb">独学</div><div class="hdr-col" style="color:#ea580c">スクール</div></div>
    {trs}
    {ft()}
    </body></html>"""
    render(html, OUT / "comparison-self-vs-school.png")


# === 4. ロードマップ（縦フロー） ===
def roadmap():
    steps = [
        ("STEP 1","1週目","環境整備","ソフト契約・PC準備",BRAND),
        ("STEP 2","2〜8週目","基礎習得","カット・テロップ・BGM","#0891b2"),
        ("STEP 3","9〜12週目","作品制作","ポートフォリオ3本","#16a34a"),
        ("STEP 4","12週目〜","案件応募","CW・ランサーズで初受注","#ea580c"),
    ]
    cards = ""
    for i,(num,period,title,desc,color) in enumerate(steps):
        cards += f"""<div class="step">
          <div class="num" style="background:{color}">{num}</div>
          <div class="info">
            <div class="title">{title}<span class="period">{period}</span></div>
            <div class="desc">{desc}</div>
          </div>
        </div>"""
        if i < 3:
            cards += '<div class="arrow">↓</div>'

    html = f"""<!DOCTYPE html><html><head><style>{CSS}
    .step{{display:flex;align-items:center;gap:16px;padding:16px 36px}}
    .num{{padding:8px 16px;border-radius:8px;color:#fff;font-size:15px;font-weight:900;white-space:nowrap}}
    .title{{font-size:24px;font-weight:900;color:#1e293b}}
    .period{{font-size:14px;color:#94a3b8;margin-left:12px;font-weight:400}}
    .desc{{font-size:16px;color:#64748b;margin-top:2px}}
    .arrow{{text-align:center;font-size:20px;color:#d1d5db;padding:4px 0;margin-left:60px}}
    </style></head><body>
    {hd("未経験からの学習ロードマップ","4ステップで最初の案件獲得へ")}
    <div style="padding:20px 0">{cards}</div>
    {ft()}
    </body></html>"""
    render(html, OUT / "roadmap-4steps.png")


# === 5. 用途別おすすめ ===
def usage_matrix():
    data = [
        ("ショート動画","CapCut","#00b4d8"),
        ("YouTube本格運用","DaVinci Resolve","#ff6b35"),
        ("Mac・iPhoneで手軽に","iMovie","#a855f7"),
        ("Windowsで今すぐ","Clipchamp","#3b82f6"),
        ("SNSバナー動画","Canva","#06b6d4"),
        ("広告なし・制限なし","Shotcut","#84cc16"),
        ("操作感を試したい","Filmora","#f59e0b"),
    ]
    rows = ""
    for usage, soft, color in data:
        rows += f"""<div class="row">
          <div class="usage">{usage}</div>
          <div class="soft"><span class="dot" style="background:{color}"></span>{soft}</div>
        </div>"""

    html = f"""<!DOCTYPE html><html><head><style>{CSS}
    .row{{display:flex;align-items:center;padding:18px 36px;border-bottom:1px solid #f1f5f9}}
    .usage{{flex:1;font-size:18px;color:#64748b}}
    .soft{{font-size:20px;font-weight:900;color:#1e293b;display:flex;align-items:center;gap:10px}}
    .dot{{width:10px;height:10px;border-radius:50%;flex-shrink:0}}
    </style></head><body>
    {hd("用途別おすすめソフト早見表","やりたいことから選ぶ")}
    {rows}
    {ft()}
    </body></html>"""
    render(html, OUT / "usage-matrix.png")


# === 6. 収入イメージ ===
def income():
    stages = [
        ("0〜3ヶ月","学習期間","0円","8%","#93c5fd"),
        ("3〜6ヶ月","初案件期","月1〜3万円","25%","#86efac"),
        ("6ヶ月〜1年","成長期","月5〜15万円","55%","#fdba74"),
        ("1年以上","安定期","月20万円〜","90%","#fca5a5"),
    ]
    rows = ""
    for period,label,amount,width,color in stages:
        rows += f"""<div class="row">
          <div class="left"><div class="period">{period}</div><div class="label">{label}</div></div>
          <div class="right">
            <div class="amount">{amount}</div>
            <div class="bar-bg"><div class="bar" style="width:{width};background:{color}"></div></div>
          </div>
        </div>"""

    html = f"""<!DOCTYPE html><html><head><style>{CSS}
    .row{{display:flex;align-items:center;padding:20px 36px;border-bottom:1px solid #f1f5f9;gap:16px}}
    .left{{width:120px}}
    .period{{font-size:16px;font-weight:700;color:#1e293b}}
    .label{{font-size:13px;color:#94a3b8}}
    .right{{flex:1}}
    .amount{{font-size:24px;font-weight:900;color:#1e293b;margin-bottom:6px}}
    .bar-bg{{height:14px;background:#f1f5f9;border-radius:7px;overflow:hidden}}
    .bar{{height:100%;border-radius:7px}}
    </style></head><body>
    {hd("未経験からの収入イメージ","副業〜本業化までの目安")}
    {rows}
    {ft()}
    </body></html>"""
    render(html, OUT / "income-roadmap.png")


def main():
    print("画像生成中...\n")
    try:
        eyecatch_beginner()
        eyecatch_free()
        comparison()
        roadmap()
        usage_matrix()
        income()
    except Exception as e:
        print(f"\n❌ {e}", file=sys.stderr)
        return 1
    print(f"\n完了！ → {OUT}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
