"""
記事用の画像を自動生成するスクリプト

使い方:
  python scripts/generate_images.py

出力先: articles/images/
"""
from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "articles" / "images"
OUT.mkdir(parents=True, exist_ok=True)

# フォント設定
FONT_PATH = "/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf"
FONT_BOLD_PATH = FONT_PATH  # 太字がなければ同じフォントを使う


def get_font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_PATH, size)


# ============================================================
# カラーパレット
# ============================================================
WHITE = "#FFFFFF"
BG_DARK = "#1A1A2E"
BG_BLUE = "#16213E"
ACCENT_BLUE = "#0F3460"
ACCENT_ORANGE = "#E94560"
ACCENT_GREEN = "#4CAF50"
ACCENT_YELLOW = "#FFC107"
LIGHT_GRAY = "#F5F5F5"
DARK_TEXT = "#333333"
MID_GRAY = "#888888"
SOFT_BLUE = "#E8F0FE"
SOFT_GREEN = "#E8F5E9"
SOFT_ORANGE = "#FFF3E0"
SOFT_RED = "#FFEBEE"
BORDER_GRAY = "#DDDDDD"


# ============================================================
# 1. アイキャッチ: 動画編集 未経験
# ============================================================
def create_eyecatch_beginner():
    w, h = 1200, 630
    img = Image.new("RGB", (w, h), BG_DARK)
    draw = ImageDraw.Draw(img)

    # グラデーション風の帯
    for i in range(h):
        r = int(26 + (15 * i / h))
        g = int(26 + (33 * i / h))
        b = int(46 + (50 * i / h))
        draw.line([(0, i), (w, i)], fill=(r, g, b))

    # アクセントライン
    draw.rectangle([0, 0, w, 8], fill=ACCENT_ORANGE)
    draw.rectangle([0, h - 8, w, h], fill=ACCENT_ORANGE)

    # テキスト
    title_font = get_font(52)
    sub_font = get_font(28)
    tag_font = get_font(22)

    # タグ
    draw.rounded_rectangle([40, 40, 200, 80], radius=8, fill=ACCENT_ORANGE)
    draw.text((55, 45), "2026年版", font=tag_font, fill=WHITE)

    # メインタイトル
    draw.text((40, 120), "動画編集は", font=title_font, fill=WHITE)
    draw.text((40, 190), "未経験でも始められる？", font=title_font, fill=ACCENT_YELLOW)

    # サブタイトル
    draw.text((40, 300), "失敗しない始め方と", font=sub_font, fill="#CCCCCC")
    draw.text((40, 340), "おすすめスクール", font=sub_font, fill="#CCCCCC")

    # 右側にアイコン風の装飾
    # 再生ボタン風
    cx, cy = 950, 300
    draw.ellipse([cx - 80, cy - 80, cx + 80, cy + 80], fill=ACCENT_ORANGE)
    # 三角形（再生マーク）
    draw.polygon([(cx - 25, cy - 40), (cx - 25, cy + 40), (cx + 35, cy)], fill=WHITE)

    # フッターテキスト
    draw.text((40, 520), "独学 vs スクール / 4ステップロードマップ / 失敗パターン5選", font=tag_font, fill=MID_GRAY)
    draw.text((40, 560), "大人の学びなおし比較", font=tag_font, fill=MID_GRAY)

    path = OUT / "eyecatch-video-editing-beginner.png"
    img.save(path, "PNG")
    print(f"✅ {path.name}")
    return path


# ============================================================
# 2. アイキャッチ: 無料動画編集ソフト比較
# ============================================================
def create_eyecatch_free_software():
    w, h = 1200, 630
    img = Image.new("RGB", (w, h), BG_BLUE)
    draw = ImageDraw.Draw(img)

    # グラデーション
    for i in range(h):
        r = int(22 + (10 * i / h))
        g = int(33 + (20 * i / h))
        b = int(62 + (30 * i / h))
        draw.line([(0, i), (w, i)], fill=(r, g, b))

    # アクセントライン
    draw.rectangle([0, 0, w, 8], fill=ACCENT_GREEN)
    draw.rectangle([0, h - 8, w, h], fill=ACCENT_GREEN)

    # タグ
    tag_font = get_font(22)
    draw.rounded_rectangle([40, 40, 200, 80], radius=8, fill=ACCENT_GREEN)
    draw.text((55, 45), "2026年版", font=tag_font, fill=WHITE)

    draw.rounded_rectangle([220, 40, 340, 80], radius=8, fill=ACCENT_ORANGE)
    draw.text((240, 45), "無料", font=tag_font, fill=WHITE)

    # メインタイトル
    title_font = get_font(52)
    sub_font = get_font(28)
    draw.text((40, 120), "無料の動画編集ソフト", font=title_font, fill=WHITE)
    draw.text((40, 190), "おすすめ7選", font=title_font, fill=ACCENT_YELLOW)

    draw.text((40, 300), "用途別に徹底比較", font=sub_font, fill="#CCCCCC")

    # 右側にソフト名を並べる
    soft_font = get_font(20)
    softwares = ["CapCut", "DaVinci Resolve", "iMovie", "Clipchamp", "Canva", "Shotcut", "Filmora"]
    colors = ["#00D1FF", "#FF6B35", "#A855F7", "#3B82F6", "#06B6D4", "#84CC16", "#F59E0B"]

    for i, (name, color) in enumerate(zip(softwares, colors)):
        y = 120 + i * 55
        x = 780
        draw.rounded_rectangle([x, y, x + 350, y + 42], radius=6, fill=color + "33", outline=color)
        draw.text((x + 15, y + 8), name, font=soft_font, fill=WHITE)

    # フッター
    draw.text((40, 520), "スマホ用 / PC用 / YouTube用 / SNS用", font=tag_font, fill=MID_GRAY)
    draw.text((40, 560), "大人の学びなおし比較", font=tag_font, fill=MID_GRAY)

    path = OUT / "eyecatch-free-video-editing-software.png"
    img.save(path, "PNG")
    print(f"✅ {path.name}")
    return path


# ============================================================
# 3. 比較図: 独学 vs スクール
# ============================================================
def create_comparison_chart():
    w, h = 1200, 700
    img = Image.new("RGB", (w, h), WHITE)
    draw = ImageDraw.Draw(img)

    title_font = get_font(36)
    header_font = get_font(26)
    body_font = get_font(20)
    small_font = get_font(16)

    # タイトル
    draw.text((w // 2 - 200, 20), "独学 vs スクール 比較", font=title_font, fill=DARK_TEXT, anchor=None)

    # 左: 独学
    lx, ly = 30, 90
    lw = 560
    draw.rounded_rectangle([lx, ly, lx + lw, ly + 560], radius=16, fill=SOFT_BLUE, outline="#90CAF9", width=2)
    draw.rounded_rectangle([lx, ly, lx + lw, ly + 60], radius=16, fill="#2196F3")
    draw.rectangle([lx, ly + 40, lx + lw, ly + 60], fill="#2196F3")
    draw.text((lx + lw // 2 - 40, ly + 15), "独学", font=header_font, fill=WHITE)

    items_l = [
        ("費用", "月額〜数千円", ACCENT_GREEN),
        ("期間", "3〜6ヶ月（個人差大）", MID_GRAY),
        ("挫折率", "高い（7〜8割）", ACCENT_ORANGE),
        ("質問対応", "自力で調べる", MID_GRAY),
        ("案件サポート", "なし", ACCENT_ORANGE),
        ("学習効率", "情報の取捨選択に時間", MID_GRAY),
    ]
    for i, (label, val, color) in enumerate(items_l):
        y = ly + 80 + i * 75
        draw.text((lx + 30, y), label, font=body_font, fill=MID_GRAY)
        draw.text((lx + 30, y + 30), val, font=header_font, fill=color)

    # 右: スクール
    rx = 630
    draw.rounded_rectangle([rx, ly, rx + lw, ly + 560], radius=16, fill=SOFT_ORANGE, outline="#FFAB91", width=2)
    draw.rounded_rectangle([rx, ly, rx + lw, ly + 60], radius=16, fill=ACCENT_ORANGE)
    draw.rectangle([rx, ly + 40, rx + lw, ly + 60], fill=ACCENT_ORANGE)
    draw.text((rx + lw // 2 - 60, ly + 15), "スクール", font=header_font, fill=WHITE)

    items_r = [
        ("費用", "15万〜40万円", ACCENT_ORANGE),
        ("期間", "2〜6ヶ月（カリキュラム化）", ACCENT_GREEN),
        ("挫折率", "低い（2〜3割）", ACCENT_GREEN),
        ("質問対応", "講師・メンター対応", ACCENT_GREEN),
        ("案件サポート", "あり（添削・紹介）", ACCENT_GREEN),
        ("学習効率", "カリキュラムで最短", ACCENT_GREEN),
    ]
    for i, (label, val, color) in enumerate(items_r):
        y = ly + 80 + i * 75
        draw.text((rx + 30, y), label, font=body_font, fill=MID_GRAY)
        draw.text((rx + 30, y + 30), val, font=header_font, fill=color)

    # VS
    draw.ellipse([w // 2 - 30, ly + 260, w // 2 + 30, ly + 320], fill=DARK_TEXT)
    draw.text((w // 2 - 18, ly + 272), "VS", font=body_font, fill=WHITE)

    path = OUT / "comparison-self-vs-school.png"
    img.save(path, "PNG")
    print(f"✅ {path.name}")
    return path


# ============================================================
# 4. ロードマップ: 4ステップ
# ============================================================
def create_roadmap():
    w, h = 1200, 500
    img = Image.new("RGB", (w, h), WHITE)
    draw = ImageDraw.Draw(img)

    title_font = get_font(32)
    step_font = get_font(22)
    body_font = get_font(18)
    small_font = get_font(14)

    draw.text((30, 20), "未経験からの学習ロードマップ（4ステップ）", font=title_font, fill=DARK_TEXT)

    steps = [
        ("STEP 1", "環境整備", "1週目", "ソフト契約\nPC準備", "#2C3E7B"),
        ("STEP 2", "基礎習得", "2〜8週目", "カット・テロップ\nBGM・補正", "#1976D2"),
        ("STEP 3", "作品制作", "9〜12週目", "ポートフォリオ\n3本作る", "#2E7D32"),
        ("STEP 4", "案件応募", "12週目〜", "CW・ランサーズ\n初受注を目指す", "#C62828"),
    ]

    box_w = 240
    gap = 40
    start_x = 40
    y = 100

    for i, (step, title, period, desc, color) in enumerate(steps):
        x = start_x + i * (box_w + gap)

        # ボックス（背景を濃くして文字を白で出す）
        draw.rounded_rectangle([x, y, x + box_w, y + 340], radius=16, fill=color, outline=color, width=2)

        # ステップラベル
        draw.rounded_rectangle([x + 10, y + 10, x + 110, y + 45], radius=8, fill=color)
        draw.text((x + 20, y + 14), step, font=small_font, fill=WHITE)

        # 期間
        draw.text((x + 120, y + 18), period, font=small_font, fill=MID_GRAY)

        # タイトル
        draw.text((x + 20, y + 65), title, font=step_font, fill=WHITE)

        # 説明
        lines = desc.split("\n")
        for j, line in enumerate(lines):
            draw.text((x + 20, y + 110 + j * 28), line, font=body_font, fill=WHITE)

        # 矢印（最後以外）
        if i < len(steps) - 1:
            ax = x + box_w + 5
            ay = y + 170
            draw.polygon([(ax, ay - 12), (ax, ay + 12), (ax + 25, ay)], fill=color)

    path = OUT / "roadmap-4steps.png"
    img.save(path, "PNG")
    print(f"✅ {path.name}")
    return path


# ============================================================
# 5. 用途別おすすめマトリクス
# ============================================================
def create_usage_matrix():
    w, h = 1200, 580
    img = Image.new("RGB", (w, h), WHITE)
    draw = ImageDraw.Draw(img)

    title_font = get_font(30)
    header_font = get_font(18)
    body_font = get_font(20)
    small_font = get_font(16)

    draw.text((30, 15), "用途別おすすめソフト早見表", font=title_font, fill=DARK_TEXT)

    rows = [
        ("ショート動画\n(TikTok/Reels)", "CapCut", "#00D1FF"),
        ("YouTube本格運用", "DaVinci Resolve", "#FF6B35"),
        ("Mac/iPhoneで手軽に", "iMovie", "#A855F7"),
        ("Windowsで今すぐ", "Clipchamp", "#3B82F6"),
        ("SNSバナー動画", "Canva", "#06B6D4"),
        ("広告なし・制限なし", "Shotcut", "#84CC16"),
        ("操作感を試したい", "Filmora(無料版)", "#F59E0B"),
    ]

    y_start = 70
    row_h = 68
    col1_w = 400
    col2_x = 440

    # ヘッダー
    draw.rectangle([20, y_start, w - 20, y_start + 45], fill=DARK_TEXT)
    draw.text((40, y_start + 10), "やりたいこと", font=header_font, fill=WHITE)
    draw.text((col2_x + 20, y_start + 10), "おすすめソフト", font=header_font, fill=WHITE)

    for i, (usage, soft, color) in enumerate(rows):
        y = y_start + 50 + i * row_h
        bg = LIGHT_GRAY if i % 2 == 0 else WHITE
        draw.rectangle([20, y, w - 20, y + row_h], fill=bg, outline=BORDER_GRAY)

        # 用途（改行対応）
        lines = usage.split("\n")
        for j, line in enumerate(lines):
            draw.text((40, y + 10 + j * 26), line, font=body_font, fill=DARK_TEXT)

        # ソフト名バッジ
        draw.rounded_rectangle([col2_x, y + 15, col2_x + 320, y + 53], radius=8, fill=color, outline=color)
        draw.text((col2_x + 15, y + 20), soft, font=body_font, fill=WHITE)

    path = OUT / "usage-matrix.png"
    img.save(path, "PNG")
    print(f"✅ {path.name}")
    return path


# ============================================================
# 6. 収入ロードマップ（未経験→月収推移）
# ============================================================
def create_income_chart():
    w, h = 1200, 500
    img = Image.new("RGB", (w, h), WHITE)
    draw = ImageDraw.Draw(img)

    title_font = get_font(30)
    label_font = get_font(20)
    small_font = get_font(16)
    num_font = get_font(24)

    draw.text((30, 15), "未経験からの収入イメージ", font=title_font, fill=DARK_TEXT)

    stages = [
        ("0〜3ヶ月", "学習期間", "0円", SOFT_BLUE, "#2196F3"),
        ("3〜6ヶ月", "初案件期", "月1〜3万円", SOFT_GREEN, ACCENT_GREEN),
        ("6ヶ月〜1年", "成長期", "月5〜15万円", SOFT_ORANGE, "#FF9800"),
        ("1年以上", "安定期", "月20万円〜", "#FFF9C4", ACCENT_ORANGE),
    ]

    bar_heights = [60, 140, 280, 380]
    bar_w = 220
    gap = 50
    base_y = 440
    start_x = 80

    for i, (period, label, income, bg, color) in enumerate(stages):
        x = start_x + i * (bar_w + gap)
        bh = bar_heights[i]

        # バー
        draw.rounded_rectangle([x, base_y - bh, x + bar_w, base_y], radius=12, fill=bg, outline=color, width=2)

        # 金額
        draw.text((x + 20, base_y - bh + 15), income, font=num_font, fill=color)

        # ラベル
        draw.text((x + 20, base_y - bh + 50), label, font=small_font, fill=MID_GRAY)

        # 期間（バーの下）
        draw.text((x + bar_w // 2 - 40, base_y + 10), period, font=label_font, fill=DARK_TEXT)

    path = OUT / "income-roadmap.png"
    img.save(path, "PNG")
    print(f"✅ {path.name}")
    return path


# ============================================================
# メイン
# ============================================================
def main():
    print("画像を生成中...\n")

    create_eyecatch_beginner()
    create_eyecatch_free_software()
    create_comparison_chart()
    create_roadmap()
    create_usage_matrix()
    create_income_chart()

    print(f"\n完了！出力先: {OUT}")
    print(f"生成ファイル数: {len(list(OUT.glob('*.png')))}")


if __name__ == "__main__":
    main()
