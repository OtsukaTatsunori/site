# WordPress連携セットアップ手順

このリポジトリから WordPress（ai-school-guide.com）に**下書き投稿を直接アップロード**できる仕組みです。
Markdownで記事を書けば、そのまま下書きとしてWordPressに飛ばせます。

---

## 1. WordPress 側でアプリケーションパスワードを発行

1. WordPress管理画面 → ユーザー → プロフィール を開く
2. 一番下までスクロール → 「アプリケーションパスワード」セクション
3. 「新しいアプリケーションパスワード名」に `Claude Code` と入力
4. 「新しいアプリケーションパスワードを追加」をクリック
5. **表示されたパスワードをコピーする**（スペース込みのまま / 一度しか表示されない）

※ アプリケーションパスワードが表示されない場合：
- WordPressのバージョンが5.6以上か確認
- SiteGuard WP Pluginなどがブロックしていたら一時的に無効化するか例外設定

---

## 2. .env ファイルを作成

リポジトリのルート（`/home/user/site/`）で以下を実行：

```bash
cp .env.example .env
```

作成した `.env` を編集し、値を設定：

```
WP_URL=https://ai-school-guide.com
WP_USER=your_wordpress_username
WP_APP_PASSWORD=xxxx xxxx xxxx xxxx xxxx xxxx
```

- `WP_USER`: WordPressログイン時のユーザー名（またはメールアドレス）
- `WP_APP_PASSWORD`: 手順1でコピーしたパスワード（スペース込みのまま貼り付け）

**重要:** `.env` は `.gitignore` に入っているので、リポジトリには絶対にコミットされません。

---

## 3. Python依存パッケージのインストール

```bash
pip3 install -r scripts/requirements.txt
```

---

## 4. 接続テスト

```bash
python3 scripts/wp_draft.py ping
```

成功すると以下が表示されます：

```
✅ 接続成功: あなたの名前 (role: administrator)
   サイト: https://ai-school-guide.com
```

エラーが出る場合：
- `401 Unauthorized` → ユーザー名またはアプリケーションパスワードが間違っている
- `Connection error` → URLが間違っている、サイトがダウンしている
- それ以外 → エラーメッセージを教えてください

---

## 5. 記事の書き方

### 記事ファイルのフォーマット

`articles/drafts/` フォルダに `.md` ファイルを作成します。

先頭に frontmatter（YAML形式）でメタ情報を書き、その下に本文（Markdown）を書きます。

```markdown
---
title: 記事のタイトル
slug: article-slug
excerpt: 記事の抜粋（メタディスクリプション相当、任意）
categories:
  - english
  - programming
tags:
  - 初心者向け
---

## 見出し

ここから本文。Markdownで書けます。

- 箇条書き
- **太字**
- [リンク](https://example.com)

| 表 | もOK |
|---|---|
| A | B |
```

### categories の指定方法

カテゴリはスラッグまたは名前で指定できます。
例: `english`, `programming`, `qualification`, `online-learning`, `subject`, `subsidy`, `age-guide`

カテゴリ一覧はコマンドで確認できます：

```bash
python3 scripts/wp_draft.py categories
```

---

## 6. 下書きとしてアップロード

```bash
python3 scripts/wp_draft.py push articles/drafts/sample.md
```

成功すると以下のような出力になります：

```
✅ 下書き作成完了: id=123  title=記事のタイトル
   編集URL: https://ai-school-guide.com/wp-admin/post.php?post=123&action=edit
   プレビュー: https://ai-school-guide.com/?p=123
```

**自動で frontmatter に `wp_id: 123` が追記されます。**
同じコマンドをもう一度実行すれば、既存の下書きが更新されます。

---

## 7. 投稿一覧の確認

```bash
python3 scripts/wp_draft.py list
```

デフォルトでは下書き + 公開済みが表示されます。
下書きだけ見たい場合:

```bash
python3 scripts/wp_draft.py list --status draft
```

---

## 8. 運用フロー

```
1. articles/drafts/ に Markdownで記事を書く
   ↓
2. python3 scripts/wp_draft.py push articles/drafts/xxx.md
   ↓（WordPressに下書きとしてアップロード）
3. WordPress管理画面で開いて最終調整
   - Cocoon独自ブロック（比較表、吹き出し、ボタン等）を追加
   - アイキャッチ画像を設定
   - アフィリエイトリンクを挿入
   ↓
4. プレビューで確認 → 公開
```

**公開操作はあえて手動です。**最終チェックを必ず人の目で行うためです。

---

## ディレクトリ構成

```
site/
├── .env                      ← あなたの接続情報（git管理外）
├── .env.example              ← テンプレート
├── scripts/
│   ├── wp_client.py          ← WordPress APIクライアント
│   ├── wp_draft.py           ← 下書き投稿CLI
│   └── requirements.txt      ← Python依存
└── articles/
    └── drafts/
        └── xxx.md            ← 記事Markdownファイル
```

---

## トラブルシューティング

### `ModuleNotFoundError: No module named 'requests'`
→ `pip3 install -r scripts/requirements.txt` を実行

### `401 Unauthorized`
→ `.env` の WP_USER / WP_APP_PASSWORD を見直す
→ アプリケーションパスワードを再発行してみる

### `SiteGuard WP Plugin` のエラー
→ SiteGuard → WAFチューニングサポート で REST API を除外設定する
→ または SiteGuard を一時的に無効化してテスト

### カテゴリが見つからない
→ WordPressの管理画面でカテゴリを先に作成する必要あり
→ `python3 scripts/wp_draft.py categories` で現在のカテゴリ一覧を確認
