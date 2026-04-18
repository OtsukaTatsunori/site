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
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700;900&family=Noto+Serif+JP:wght@700;900&family=Zen+Maru+Gothic:wght@500;700&display=swap');
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Noto Sans JP',sans-serif;-webkit-font-smoothing:antialiased;background:#FAF8F3;width:800px;color:#2D3748}
"""
BRAND = "#C56B49"
SITE = "大人の学びなおし比較"

def hd(title, sub=""):
    s = f'<p class="hd-sub">{sub}</p>' if sub else ""
    return f"""<div style="background:{BRAND};color:#fff;padding:28px 36px;position:relative">
      <div style="font-family:'Noto Serif JP',serif;font-size:26px;font-weight:900">{title}</div>{s}
      <div style="position:absolute;bottom:-8px;left:36px;width:60px;height:4px;background:#FFE8A3;border-radius:2px"></div>
    </div>"""

def ft():
    return f'<div style="padding:16px 36px;border-top:2px dashed #E8DFD0;font-size:13px;color:#A89F91;text-align:right;font-family:\'Zen Maru Gothic\',sans-serif">{SITE}</div>'


# === 1. アイキャッチ: 動画編集 未経験 ===
def eyecatch_beginner():
    html = f"""<!DOCTYPE html><html><head><style>{CSS}
    body{{height:420px;background:#FAF8F3;position:relative;overflow:hidden}}
    .wrap{{padding:48px 44px;position:relative;height:100%;display:flex;flex-direction:column;justify-content:center}}
    .tag{{display:inline-block;background:{BRAND};color:#fff;padding:6px 16px;border-radius:6px;font-size:14px;font-weight:700;margin-bottom:16px;letter-spacing:0.05em;width:fit-content;font-family:'Zen Maru Gothic',sans-serif}}
    h1{{font-family:'Noto Serif JP',serif;font-size:38px;font-weight:900;color:#2D3748;line-height:1.4;letter-spacing:0.02em}}
    h1 .hl{{background:linear-gradient(transparent 60%,#FFE8A3 60%);padding:0 4px}}
    h1 em{{font-style:normal;color:{BRAND}}}
    .sub{{font-family:'Zen Maru Gothic',sans-serif;font-size:17px;color:#6B5B3E;margin-top:14px;line-height:1.6}}
    .chips{{display:flex;gap:8px;margin-top:20px;flex-wrap:wrap}}
    .chip{{background:#fff;border:1px solid #E8DFD0;padding:6px 14px;border-radius:20px;font-size:13px;color:#8B7E6A;font-family:'Zen Maru Gothic',sans-serif}}
    .deco{{position:absolute;right:-20px;top:50%;transform:translateY(-50%);width:200px;height:200px;background:{BRAND};border-radius:50%;opacity:0.08}}
    .play{{position:absolute;right:70px;top:50%;transform:translateY(-50%);width:90px;height:90px;border-radius:50%;background:{BRAND};display:flex;align-items:center;justify-content:center;box-shadow:0 8px 24px rgba(197,107,73,0.3)}}
    .play::after{{content:'';border-left:26px solid #fff;border-top:16px solid transparent;border-bottom:16px solid transparent;margin-left:6px}}
    .brand{{position:absolute;bottom:16px;left:44px;font-size:12px;color:#A89F91;font-family:'Zen Maru Gothic',sans-serif}}
    .tape{{position:absolute;top:24px;right:240px;width:80px;height:22px;background:rgba(255,232,163,0.6);transform:rotate(6deg)}}
    </style></head><body>
    <div class="deco"></div>
    <div class="tape"></div>
    <div class="play"></div>
    <div class="wrap">
      <span class="tag">2026年版</span>
      <h1>動画編集は<br><span class="hl"><em>未経験でも始められる？</em></span></h1>
      <p class="sub">失敗しない始め方と、おすすめスクール</p>
      <div class="chips">
        <span class="chip">独学 vs スクール</span>
        <span class="chip">4ステップロードマップ</span>
        <span class="chip">失敗パターン5選</span>
      </div>
      <div class="brand">{SITE}</div>
    </div>
    </body></html>"""
    render(html, OUT / "eyecatch-video-editing-beginner.png")


# === 2. アイキャッチ: 無料ソフト比較 ===
def eyecatch_free():
    softs = [("CapCut","#E8795C"),("DaVinci Resolve","#4A7FAD"),("iMovie","#8B6FBF"),("Clipchamp","#5A8EC5"),("Canva","#5EA5B8"),("Shotcut","#7A9C5E"),("Filmora","#C9943A")]
    items = "".join(f'<span class="chip" style="border-left:4px solid {c}">{n}</span>' for n, c in softs)
    html = f"""<!DOCTYPE html><html><head><style>{CSS}
    body{{height:420px;background:#FAF8F3;position:relative;overflow:hidden;padding:48px 44px;display:flex;flex-direction:column;justify-content:center}}
    .tags{{display:flex;gap:8px;margin-bottom:14px}}
    .tag{{padding:6px 16px;border-radius:6px;font-size:14px;font-weight:700;color:#fff;font-family:'Zen Maru Gothic',sans-serif;letter-spacing:0.05em}}
    h1{{font-family:'Noto Serif JP',serif;font-size:36px;font-weight:900;color:#2D3748;line-height:1.4}}
    h1 em{{font-style:normal;color:{BRAND}}}
    h1 .hl{{background:linear-gradient(transparent 60%,#FFE8A3 60%);padding:0 4px}}
    .sub{{font-family:'Zen Maru Gothic',sans-serif;font-size:17px;color:#6B5B3E;margin-top:14px}}
    .chips{{display:flex;flex-wrap:wrap;gap:8px;margin-top:22px;max-width:560px}}
    .chip{{background:#fff;padding:8px 14px;border-radius:6px;font-size:14px;font-weight:700;color:#2D3748;font-family:'Zen Maru Gothic',sans-serif;box-shadow:0 2px 6px rgba(0,0,0,0.04)}}
    .brand{{position:absolute;bottom:16px;left:44px;font-size:12px;color:#A89F91;font-family:'Zen Maru Gothic',sans-serif}}
    .tape{{position:absolute;top:28px;right:60px;width:110px;height:24px;background:rgba(255,232,163,0.7);transform:rotate(-4deg)}}
    .tape-label{{position:absolute;top:30px;right:72px;font-size:14px;font-weight:700;color:#8B7E3E;transform:rotate(-4deg);font-family:'Zen Maru Gothic',sans-serif;letter-spacing:0.1em}}
    </style></head><body>
    <div class="tape"></div>
    <div class="tape-label">7本を比較！</div>
    <div class="tags"><span class="tag" style="background:{BRAND}">2026年版</span><span class="tag" style="background:#5B8C3E">完全無料</span></div>
    <h1>無料の動画編集ソフト<br><span class="hl"><em>おすすめ7選</em></span></h1>
    <p class="sub">用途別に徹底比較</p>
    <div class="chips">{items}</div>
    <div class="brand">{SITE}</div>
    </body></html>"""
    render(html, OUT / "eyecatch-free-video-editing-software.png")


# === 3. 独学 vs スクール（1カラム・縦並び） ===
def comparison():
    rows = [
        ("💰", "費用", "月額〜数千円", "◎", "15万〜40万円", "△", True),
        ("⏱️", "期間", "3〜6ヶ月", "○", "2〜6ヶ月", "◎", False),
        ("🔥", "挫折率", "高い（7〜8割）", "×", "低い（2〜3割）", "◎", True),
        ("💬", "質問対応", "自力で調べる", "△", "講師が対応", "◎", False),
        ("🤝", "案件サポート", "なし", "×", "あり", "◎", True),
        ("📈", "学習効率", "取捨選択に時間", "△", "最短ルート", "◎", False),
    ]
    rc = {"◎":"#5B8C3E","○":"#4A7FAD","△":"#C9943A","×":"#C75450"}
    trs = ""
    for icon, label, v1, r1, v2, r2, highlight in rows:
        hl = "background:rgba(255,232,163,0.4);" if highlight else ""
        trs += f"""<div class="row" style="{hl}">
          <div class="icon">{icon}</div>
          <div class="label">{label}</div>
          <div class="cell">
            <span class="rating" style="color:{rc[r1]}">{r1}</span>
            <span class="val">{v1}</span>
          </div>
          <div class="cell">
            <span class="rating" style="color:{rc[r2]}">{r2}</span>
            <span class="val">{v2}</span>
          </div>
        </div>"""

    html = f"""<!DOCTYPE html><html><head><style>{CSS}
    .hdr{{display:flex;padding:0 36px;align-items:center}}
    .hdr-blank{{width:140px}}
    .hdr-col{{flex:1;text-align:center;padding:20px 0;font-size:22px;font-weight:900;font-family:'Noto Serif JP',serif}}
    .row{{display:flex;align-items:center;padding:18px 36px;border-bottom:2px dashed #E8DFD0}}
    .row:last-child{{border-bottom:none}}
    .icon{{width:32px;font-size:22px;flex-shrink:0}}
    .label{{width:108px;font-size:15px;color:#8B7E6A;font-weight:700;font-family:'Zen Maru Gothic',sans-serif}}
    .cell{{flex:1;display:flex;align-items:center;gap:10px}}
    .rating{{font-size:26px;font-weight:900;width:32px;text-align:center}}
    .val{{font-size:18px;font-weight:700;color:#2D3748}}
    .note{{
      margin:0 36px 0;padding:16px 20px;
      background:#FFF8E7;border-left:4px solid #C9943A;border-radius:0 8px 8px 0;
      font-size:15px;color:#6B5B3E;line-height:1.6;
      font-family:'Zen Maru Gothic',sans-serif;
    }}
    .note strong{{color:#C56B49}}
    </style></head><body>
    {hd("独学 vs スクール 比較","〜 正直なところ、どちらが合う？ 〜")}
    <div class="hdr">
      <div class="hdr-blank"></div>
      <div class="hdr-col" style="color:#4A7FAD">独学</div>
      <div class="hdr-col" style="color:#C56B49">スクール</div>
    </div>
    {trs}
    <div class="note">
      📝 <strong>迷ったときの判断基準：</strong>「3ヶ月以内に案件を取りたい」ならスクール、「まず向き不向きを確認したい」なら独学からがおすすめです。
    </div>
    {ft()}
    </body></html>"""
    render(html, OUT / "comparison-self-vs-school.png")


# === 4. ロードマップ（縦フロー） ===
def roadmap():
    steps = [
        ("01","1週目","🛠","環境整備","ソフト契約・PC準備","#C56B49"),
        ("02","2〜8週目","📚","基礎習得","カット・テロップ・BGM","#4A7FAD"),
        ("03","9〜12週目","🎬","作品制作","ポートフォリオ3本","#5B8C3E"),
        ("04","12週目〜","💼","案件応募","CW・ランサーズで初受注","#C9943A"),
    ]
    cards = ""
    for i,(num,period,icon,title,desc,color) in enumerate(steps):
        cards += f"""<div class="step">
          <div class="num-wrap">
            <div class="num" style="color:{color};border-color:{color}">{num}</div>
          </div>
          <div class="info">
            <div class="meta"><span class="icon">{icon}</span><span class="period">{period}</span></div>
            <div class="title">{title}</div>
            <div class="desc">{desc}</div>
          </div>
        </div>"""
        if i < 3:
            cards += '<div class="connector"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div>'

    html = f"""<!DOCTYPE html><html><head><style>{CSS}
    .step{{display:flex;align-items:center;gap:20px;padding:20px 36px}}
    .num-wrap{{flex-shrink:0}}
    .num{{width:64px;height:64px;border-radius:50%;border:3px solid;display:flex;align-items:center;justify-content:center;font-family:'Noto Serif JP',serif;font-size:24px;font-weight:900;background:#fff}}
    .info{{flex:1}}
    .meta{{display:flex;align-items:center;gap:10px;margin-bottom:4px}}
    .icon{{font-size:18px}}
    .period{{font-size:13px;color:#8B7E6A;font-family:'Zen Maru Gothic',sans-serif;background:#FFF8E7;padding:2px 10px;border-radius:10px}}
    .title{{font-family:'Noto Serif JP',serif;font-size:24px;font-weight:900;color:#2D3748}}
    .desc{{font-size:15px;color:#6B5B3E;margin-top:4px;font-family:'Zen Maru Gothic',sans-serif}}
    .connector{{display:flex;flex-direction:column;gap:4px;margin-left:66px;padding:6px 0}}
    .connector .dot{{width:4px;height:4px;border-radius:50%;background:#E8DFD0}}
    </style></head><body>
    {hd("未経験からの学習ロードマップ","〜 4ステップで最初の案件獲得へ 〜")}
    <div style="padding:24px 0">{cards}</div>
    {ft()}
    </body></html>"""
    render(html, OUT / "roadmap-4steps.png")


# === 5. 用途別おすすめ ===
def usage_matrix():
    data = [
        ("📱","ショート動画","CapCut","#E8795C"),
        ("🎥","YouTube本格運用","DaVinci Resolve","#4A7FAD"),
        ("🍎","Mac・iPhoneで手軽に","iMovie","#8B6FBF"),
        ("🪟","Windowsで今すぐ","Clipchamp","#5A8EC5"),
        ("🎨","SNSバナー動画","Canva","#5EA5B8"),
        ("🔧","広告なし・制限なし","Shotcut","#7A9C5E"),
        ("🎓","操作感を試したい","Filmora","#C9943A"),
    ]
    rows = ""
    for icon, usage, soft, color in data:
        rows += f"""<div class="row">
          <div class="icon">{icon}</div>
          <div class="usage">{usage}</div>
          <div class="soft" style="color:{color}">{soft}</div>
        </div>"""

    html = f"""<!DOCTYPE html><html><head><style>{CSS}
    .row{{display:flex;align-items:center;padding:18px 36px;border-bottom:2px dashed #E8DFD0;gap:14px}}
    .row:last-child{{border-bottom:none}}
    .icon{{font-size:24px;width:32px;flex-shrink:0}}
    .usage{{flex:1;font-size:17px;color:#6B5B3E;font-family:'Zen Maru Gothic',sans-serif}}
    .soft{{font-family:'Noto Serif JP',serif;font-size:20px;font-weight:900}}
    </style></head><body>
    {hd("用途別おすすめソフト早見表","〜 やりたいことから選ぶ 〜")}
    {rows}
    {ft()}
    </body></html>"""
    render(html, OUT / "usage-matrix.png")


# === 6. 収入イメージ ===
def income():
    stages = [
        ("🌱","0〜3ヶ月","学習期間","0円","10%","#A8C5A0","#C1D8B9"),
        ("🌿","3〜6ヶ月","初案件期","月1〜3万円","28%","#7DAA8E","#9DC2AE"),
        ("🌳","6ヶ月〜1年","成長期","月5〜15万円","58%","#D9A25F","#E8BA82"),
        ("🏆","1年以上","安定期","月20万円〜","92%","#C56B49","#D98866"),
    ]
    rows = ""
    for icon,period,label,amount,width,color,light in stages:
        rows += f"""<div class="row">
          <div class="left">
            <div class="icon">{icon}</div>
            <div class="period">{period}</div>
            <div class="label">{label}</div>
          </div>
          <div class="right">
            <div class="amount" style="color:{color}">{amount}</div>
            <div class="bar-bg"><div class="bar" style="width:{width};background:linear-gradient(90deg,{light},{color})"></div></div>
          </div>
        </div>"""

    html = f"""<!DOCTYPE html><html><head><style>{CSS}
    .row{{display:flex;align-items:center;padding:22px 36px;border-bottom:2px dashed #E8DFD0;gap:20px}}
    .row:last-child{{border-bottom:none}}
    .left{{width:130px;text-align:center}}
    .icon{{font-size:28px;margin-bottom:4px}}
    .period{{font-size:14px;font-weight:700;color:#2D3748;font-family:'Zen Maru Gothic',sans-serif}}
    .label{{font-size:12px;color:#8B7E6A;font-family:'Zen Maru Gothic',sans-serif}}
    .right{{flex:1}}
    .amount{{font-family:'Noto Serif JP',serif;font-size:26px;font-weight:900;margin-bottom:8px}}
    .bar-bg{{height:12px;background:#F0E9DB;border-radius:6px;overflow:hidden;box-shadow:inset 0 1px 2px rgba(0,0,0,0.06)}}
    .bar{{height:100%;border-radius:6px}}
    .note{{margin:0 36px 0;padding:14px 18px;background:#FFF8E7;border-left:4px solid #C9943A;border-radius:0 8px 8px 0;font-size:14px;color:#6B5B3E;line-height:1.6;font-family:'Zen Maru Gothic',sans-serif}}
    </style></head><body>
    {hd("未経験からの収入イメージ","〜 副業〜本業化までの目安 〜")}
    {rows}
    <div class="note">
      📝 <strong style="color:#C56B49">目安の数字です。</strong>週にかけられる時間とスキル習得の速さで個人差があります。
    </div>
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
