---
description: 記事用の画像を生成する。画像の種類（比較図・ロードマップ・アイキャッチ等）を指定するとHTML/CSS/Playwrightで作成。
---

# gen-image

記事用の画像を HTML/CSS + Playwright で生成するスキル。

## 引数
`$ARGS` に画像の種類・テーマが入る（例: `プログラミングスクール比較図`、`Premiere Pro vs DaVinci Resolve比較`）。

## 実行手順

### 1. デザイン原則の確認

`scripts/generate_images_v2.py` を基準とし、以下を守る：

- **幅: 800px**（スマホ400px表示で2倍のRetina）
- **フォント最小: 18px**（スマホ表示で9px相当、読める範囲）
- **1カラム縦並び**（横並びは最大2列まで）
- **白背景ベース**（カラフルな背景は避ける）
- **評価は◎○△×** で視覚化
- **ブランドヘッダー**（青 `#2563eb`）とフッター（サイト名）で統一
- **余白ルール**: padding 16px / 24px / 36px のグリッド

### 2. スクリプトに関数を追加

`scripts/generate_images_v2.py` に新しい関数を追加する：

```python
def {function_name}():
    html = f\"\"\"<!DOCTYPE html><html><head><style>{CSS}
    ...
    </style></head><body>
    {hd("画像タイトル", "サブタイトル")}
    ...
    {ft()}
    </body></html>\"\"\"
    render(html, OUT / "{slug}.png")
```

`main()` 関数の try ブロックに追加呼び出し。

### 3. 生成確認

可能ならローカルで試し打ち（この環境で Playwright が動かないので Windows 側で確認してもらう）。

### 4. 記事への埋め込み案内

該当記事の Markdown に `![{alt}](UPLOAD_URL:{filename}.png)` で埋め込む位置を提案する。alt テキストはメインキーワードを含む具体的な説明にする。

### 5. コミット＆プッシュ

### 6. Windows側の手順

```powershell
cd C:\Users\t1528\Documents\site\site
git pull origin claude/enable-cocoon-child-cd2DT
python scripts/generate_images_v2.py
explorer articles\images
```

## 画像タイプ別のテンプレート

### 比較表
- `hd()` で青ヘッダー → 行ごとに label / value-A / rating-A / value-B / rating-B
- 最上段に列見出し（独学 / スクール等）

### ロードマップ
- 縦並びステップ。ステップ番号バッジ（色付き）+ タイトル + 説明
- ステップ間に矢印 `↓`

### 早見表（用途→おすすめ）
- 1行 = 1用途。左に用途、右にソフト名＋カラードット

### 収入グラフ（段階推移）
- 縦並び。期間 / ラベル / 金額 / プログレスバー

### アイキャッチ
- 高さ 420px 固定。左にタイトル＋タグ、右にアクセント色ブロック
