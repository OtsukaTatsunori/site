---
title: 【2026年】AI動画生成プロンプトの書き方｜Runway・Kling・Pikaで使えるテンプレート集
slug: ai-video-prompt-guide
excerpt: AI動画生成ツールで思い通りの動画を作るためのプロンプトの書き方を解説。Runway、Kling、Pikaで使えるテンプレートと、カメラワーク・動き・雰囲気の指定方法を紹介します。
categories:
  - ai
tags:
  - AI動画生成
  - プロンプト
  - Runway
  - テンプレート
---

AI動画生成は**プロンプトの書き方**で結果が大きく変わります。画像生成と違い、**動き・カメラワーク・時間の流れ**を指示する必要があるのが特徴です。

## 動画プロンプトの基本構文

![AI動画生成プロンプトの6要素](UPLOAD_URL:ai-video-prompt-structure.png)

| 要素 | 内容 | 例 |
|---|---|---|
| **①被写体** | 何が映っているか | a woman walking, ocean waves |
| **②動きの指示** | 被写体がどう動くか | slowly turning, running toward camera |
| **③カメラワーク** | カメラの動き | dolly in, pan left, tracking shot |
| **④スピード** | 動きの速さ | slow motion, timelapse, normal speed |
| **⑤雰囲気** | 色調・ムード | cinematic, warm tones, dramatic |
| **⑥品質** | 解像度・フレームレート | 4K, 24fps, high quality |

### 基本テンプレート

```
[被写体] + [動きの指示],
[カメラワーク], [スピード],
[雰囲気], [品質]
```

## カメラワークのキーワード一覧

| キーワード | 効果 | 使いどころ |
|---|---|---|
| **dolly in** | カメラが被写体に近づく | 注目させたいとき |
| **dolly out** | カメラが引いていく | 全体像を見せたいとき |
| **pan left / right** | カメラが左右に振る | 風景を広く見せる |
| **tilt up / down** | カメラが上下に振る | 建物を見上げる等 |
| **tracking shot** | 被写体を追いかける | 歩く人を追う等 |
| **aerial shot** | 空撮 | 風景のダイナミックさ |
| **static shot** | カメラ固定 | 安定感を出す |
| **handheld** | 手持ち風の揺れ | ドキュメンタリー感 |

## 用途別テンプレート集

### YouTube動画のオープニング

```
cinematic aerial shot of a modern city at sunset,
golden hour lighting, warm color grading,
slow dolly forward over skyscrapers,
dramatic orchestral mood,
4K, high quality, smooth motion
```

### 商品紹介の背景映像

```
abstract particles floating in dark space,
soft blue and purple neon glow,
slow motion, gentle camera rotation,
clean and modern technology feel,
4K, seamless loop
```

### 旅行・Vlog風

```
woman walking through narrow streets of a european town,
handheld tracking shot from behind,
natural daylight, film grain,
casual documentary style,
warm tones, 24fps cinematic
```

### リラックス・ASMR系

```
close-up of rain drops falling on green leaves,
macro lens, extreme shallow depth of field,
slow motion 120fps,
soft natural lighting, calm mood,
4K, high detail
```

### ビジネスプレゼン用

```
modern office with people collaborating around a table,
smooth dolly in, professional studio lighting,
clean and bright atmosphere,
corporate style, 4K
```

## 失敗しやすいポイントと対策

| 失敗 | 原因 | 対策 |
|---|---|---|
| 動きが不自然 | 指示が曖昧 | 「slowly」「gently」等でスピードを明示 |
| 顔が崩れる | 人物の顔のクローズアップ | 引きの構図にするか、顔を背ける指示 |
| 長すぎて破綻 | 10秒以上の動画 | 5〜10秒で区切り、編集ソフトでつなぐ |
| 文字が崩れる | テキストを入れようとした | テロップは動画編集ソフトで後付け |

## 英語プロンプトに変換するコツ

日本語で考えた内容をChatGPTで英語プロンプトに変換するのが効率的です。

```
以下の日本語を、AI動画生成ツール用の英語プロンプトに変換してください。
カメラワーク、動きの指示、雰囲気を具体的に含めてください。

「夕暮れの海辺で女性が振り返る。スローモーション。映画のような雰囲気。」
```

## まとめ

| ステップ | やること |
|---|---|
| 1 | 6要素（被写体・動き・カメラ・速度・雰囲気・品質）で構成 |
| 2 | 英語で書く（ChatGPTで変換OK） |
| 3 | 5〜10回生成してベストを選ぶ |
| 4 | 動画編集ソフトで複数クリップを組み合わせる |

ツールの選び方 → [AI動画生成ツール比較5選](/ai-video-generation-tools/)

動画編集との組み合わせ → [動画編集ソフトの選び方](/video-editing-software-guide/)
