# SNS 自動投稿ツール — 大人の学びなおし

X（Twitter）と Instagram への投稿を自動化するツールです。

## セットアップ

### 1. Python パッケージのインストール

```bash
cd social-automation
pip install -r requirements.txt
```

### 2. API キーの取得

#### X (Twitter) API

1. [X Developer Portal](https://developer.x.com/en/portal/dashboard) にアクセス
2. プロジェクト・アプリを作成
3. 「User authentication settings」で OAuth 1.0a を有効にする
4. 以下の 4 つのキーを取得:
   - API Key
   - API Secret
   - Access Token
   - Access Token Secret

#### Instagram Graph API

1. [Facebook Developers](https://developers.facebook.com/) にアクセス
2. アプリを作成し、Instagram Graph API を追加
3. Instagram ビジネスアカウントを Facebook ページに接続
4. 以下を取得:
   - Instagram ビジネスアカウント ID
   - ページアクセストークン（長期トークン推奨）

### 3. 環境変数の設定

```bash
cp .env.example .env
```

`.env` ファイルを開き、取得したキーを記入してください。

**重要: `.env` ファイルは絶対に Git にコミットしないでください。**

## 使い方

### ブログ記事をシェア

```bash
python main.py blog \
  --title "英語の学び直しに最適な3つの方法" \
  --summary "大人になってからでも遅くない！効率的な英語学習法を紹介" \
  --url "https://your-site.com/english-learning" \
  --image "https://your-site.com/wp-content/uploads/image.jpg"
```

### ワンポイント知識を投稿

```bash
python main.py tip \
  --category "英語" \
  --tip "「I look forward to」の後は動名詞（-ing）！「I look forward to seeing you」が正解です" \
  --image "/path/to/local/image.jpg"
```

### 自由テキストで投稿

```bash
python main.py custom \
  --text "今日から新しいシリーズを始めます！" \
  --ig-text "今日から新しいシリーズを始めます！\n\n詳しくはプロフィールのリンクから👆"
```

### オプション

| オプション | 説明 |
|-----------|------|
| `--image` | 画像パス（X用）または画像URL（Instagram用） |
| `--hashtags` | 追加ハッシュタグ（カンマ区切り、例: `英語学習,TOEIC`） |
| `--x-only` | X のみに投稿 |
| `--ig-only` | Instagram のみに投稿 |
| `--dry-run` | 投稿せずにプレビューだけ表示 |

### プレビュー（ドライラン）

実際に投稿せず内容を確認できます:

```bash
python main.py blog \
  --title "テスト記事" \
  --summary "テスト要約" \
  --url "https://example.com" \
  --dry-run
```

## ファイル構成

| ファイル | 役割 |
|---------|------|
| `main.py` | CLI エントリーポイント |
| `content_creator.py` | 投稿テンプレート・コンテンツ作成 |
| `x_poster.py` | X (Twitter) API 連携 |
| `instagram_poster.py` | Instagram Graph API 連携 |
| `config.py` | 環境変数の読み込み |
| `.env.example` | 環境変数テンプレート |

## 注意事項

- Instagram Graph API はローカル画像を直接アップロードできません。画像は公開 URL で指定してください（WordPress のメディアライブラリ URL が使えます）。
- X は画像なしでもテキストのみで投稿できます。
- X の文字数制限は 280 文字、Instagram のキャプションは 2,200 文字です。
- API キー（`.env` ファイル）は絶対に Git にコミットしないでください。
