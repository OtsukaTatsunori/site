---
title: 【2026年】AI画像生成プロンプト完全ガイド｜Midjourney・DALL-Eで思い通りの画像を作るコツ
slug: ai-image-prompt-guide
excerpt: AI画像生成のプロンプト（呪文）の書き方を完全解説。Midjourney、DALL-E、Stable Diffusionで使える基本構文、画風指定、品質向上のテクニックとテンプレート付き。
categories:
  - ai
tags:
  - AI画像生成
  - プロンプト
  - Midjourney
  - DALL-E
---

AI画像生成は**プロンプト（指示文）の書き方**で出力品質が10倍変わります。この記事では、思い通りの画像を作るためのプロンプトの書き方とテンプレートを紹介します。

**この記事でわかること：**
- AI画像生成プロンプトの5要素と基本テンプレート
- Midjourney・DALL-E・SDのツール別コツ
- 画風指定キーワード一覧と品質向上テクニック


## プロンプトの基本構文

![AI画像生成プロンプトの5要素](UPLOAD_URL:ai-image-prompt-structure.png)

| 要素 | 内容 | 例 |
|---|---|---|
| **①被写体** | 何が映っているか | a woman, a cat, a cityscape |
| **②スタイル** | 画風・アートスタイル | photo realistic, watercolor, anime |
| **③構図** | カメラアングル・フレーミング | close-up, bird's eye view, wide angle |
| **④照明** | 光の種類・方向 | golden hour, studio lighting, neon |
| **⑤品質指定** | 解像度・クオリティ | high quality, 4K, detailed |

### 基本テンプレート

```
[被写体], [スタイル], [構図], [照明], [品質指定]
```

**例**：
```
a japanese woman reading a book in a cafe,
photo realistic, soft natural lighting,
medium shot, shallow depth of field,
high quality, 4K, detailed
```

> 💬 **現場の本音**：プロのAIクリエイターは「5要素を全部入れた基本プロンプト」をテンプレとして保存しています。毎回ゼロから書くのではなく、テンプレの被写体だけ変える方が安定した品質が出ます。

## ツール別のコツ

### Midjourney のコツ

| テクニック | プロンプト例 |
|---|---|
| **アスペクト比** | `--ar 16:9`（横長）、`--ar 9:16`（縦長） |
| **スタイル強度** | `--stylize 100`（控えめ）〜`--stylize 1000`（強い） |
| **バージョン指定** | `--v 7`（最新版を使用） |
| **ネガティブ** | `--no text, watermark`（文字やウォーターマークを除外） |

### DALL-E（ChatGPT）のコツ

| テクニック | 詳細 |
|---|---|
| **日本語OK** | 日本語プロンプトの精度が高い。そのまま日本語で書ける |
| **対話で修正** | 「もう少し明るく」「背景を変えて」と対話形式で調整可能 |
| **サイズ指定** | 「横長で」「正方形で」と指定 |

### Stable Diffusion のコツ

| テクニック | 詳細 |
|---|---|
| **ネガティブプロンプト** | `Negative prompt: low quality, blurry, deformed hands` |
| **重み付け** | `(beautiful face:1.3)` で特定要素を強調 |
| **モデル選択** | SDXL、Animagine等、目的に合ったモデルを選ぶ |

## 画風・スタイルの指定一覧

| カテゴリ | キーワード | 効果 |
|---|---|---|
| **写真風** | photo realistic, cinematic, editorial | 本物の写真のような画像 |
| **イラスト** | illustration, digital art, concept art | デジタルイラスト風 |
| **アニメ** | anime style, manga style | 日本のアニメ・漫画風 |
| **水彩画** | watercolor painting | 水彩画風の柔らかいタッチ |
| **油絵** | oil painting | 油絵風の重厚な質感 |
| **ミニマル** | minimalist, flat design | シンプルでモダン |
| **レトロ** | vintage, retro, 80s style | レトロな雰囲気 |

## 用途別テンプレート集

### ビジネス用（プレゼン・資料の挿絵）

```
a modern office workspace with laptop and coffee,
clean minimalist style, bright natural lighting,
top-down view, soft shadows,
professional, high quality, white background
```

サムネイル画像の作り方は[AIでYouTubeサムネイルを自動作成する方法](/ai-thumbnail-creation/)も参考にしてください。

### YouTube サムネイル用の背景

```
abstract colorful gradient background,
vibrant blue and orange tones,
dynamic lighting, bokeh effect,
high resolution, suitable for text overlay
```

### SNS投稿用（おしゃれな雰囲気）

```
aesthetic flat lay of stationery and plants,
soft pastel colors, instagram style,
overhead view, natural daylight,
clean composition, 4K
```

### ブログのアイキャッチ

```
conceptual image of AI and technology,
futuristic digital art style, blue and white tones,
clean composition with space for text,
professional, modern, high quality
```

## 品質を上げるキーワード集

| 目的 | キーワード |
|---|---|
| **高解像度** | 4K, 8K, high resolution, ultra detailed |
| **映画品質** | cinematic, film grain, color grading |
| **プロ写真** | professional photography, shot on Canon EOS R5 |
| **照明の質** | studio lighting, golden hour, rim lighting |
| **構図の良さ** | rule of thirds, leading lines, symmetry |

## 避けるべきNG

| NG | 理由 |
|---|---|
| **実在の人物名** | 肖像権・パブリシティ権の問題 |
| **長すぎるプロンプト** | キーワードの羅列が効果的。文章は不要 |
| **矛盾する指示** | 「明るい暗い夜景」のような矛盾は破綻する |
| **テキストの生成** | AI画像内の文字は崩れやすい。後から画像編集ソフトで追加 |

> 💡 **よくある失敗**：「beautiful, amazing, stunning」のような形容詞を大量に並べても品質は上がりません。それよりも**構図・照明・カメラの種類**を具体的に指定する方が効果的です。

## こんな人におすすめ / おすすめしない人

| 向いている人 | 向いていない人 |
|---|---|
| AI画像のクオリティを上げたい人 | すでにプロンプトエンジニアとして活動している人 |
| プロンプトの書き方がわからない初心者 | 写真撮影で実写画像を使いたい人 |
| 用途別テンプレートをコピペで使いたい人 | 日本語のみでプロンプトを書きたい人（英語推奨） |


## よくある質問

### Q. 英語と日本語、どっちがいい？

**英語が推奨**です（特にMidjourney・Stable Diffusion）。DALL-E（ChatGPT内）は日本語でも高精度。ChatGPTに「以下を英語のAI画像生成プロンプトに変換して」と頼む方法が効率的です。

### Q. 思い通りの画像が出ないときは？

1回で完璧を目指さない。**5〜10回生成して、ベストを選ぶ**のが基本です。その上で「もう少し◯◯に」と修正指示を出して絞り込みます。

## まとめ

| ステップ | やること |
|---|---|
| 1 | 5要素（被写体・スタイル・構図・照明・品質）で構成 |
| 2 | キーワードを英語で羅列（文章不要） |
| 3 | 5〜10回生成してベストを選ぶ |
| 4 | 修正指示で微調整 |

ツールの選び方 → [AI画像生成ツール比較6選](/ai-image-generation-tools/)

動画のプロンプトも学ぶ → [AI動画生成プロンプトの書き方](/ai-video-prompt-guide/)

副業での活用 → [AI画像生成で副業する方法](/ai-image-side-job/)

AIスキル全体 → [AIスキルの始め方 完全ロードマップ](/ai-skill-roadmap/)
