---
description: 記事をWordPressに反映する。画像生成→アップロード→記事push までの全手順をWindows側のコマンドで提示。
---

# ship-article

記事を WordPress に公開する（下書きとして）スキル。

## 引数
`$ARGS` に記事のスラッグまたはファイルパスが入る（例: `video-editing-beginner`、`articles/drafts/free-video-editing-software.md`）。

指定がなければ、直近に作成・編集した記事を対象とする。

## 実行手順

### 1. 記事の存在確認

`articles/drafts/{slug}.md` が存在することを確認する。

### 2. 新規記事 or 既存記事の判定

Markdown の frontmatter に `wp_id` があるか確認する。
- あり → **既存記事の更新**（WAF OFF 必要）
- なし → **新規記事作成**

### 3. 画像の有無を確認

記事内に `UPLOAD_URL:` マーカーがあるか確認する。あれば画像生成＋アップロードが必要。

### 4. Windows側の手順を全て提示

以下のテンプレートから適切なものを選んで提示する。

#### パターンA: 画像なし・新規記事

```powershell
cd C:\Users\t1528\Documents\site\site
git pull origin claude/enable-cocoon-child-cd2DT
python scripts/wp_draft.py push articles/drafts/{slug}.md
```

#### パターンB: 画像あり・新規記事

```powershell
cd C:\Users\t1528\Documents\site\site
git pull origin claude/enable-cocoon-child-cd2DT
python scripts/generate_images_v2.py
del articles\images\uploaded_urls.txt
python scripts/wp_draft.py upload-images
python scripts/wp_draft.py push articles/drafts/{slug}.md
```

#### パターンC: 既存記事の更新（WAF OFF 必要）

> ⚠️ 次のコマンドを実行する前に、**ConoHa WING コントロールパネル → サイトセキュリティ → WAF を OFF** にしてください。

```powershell
cd C:\Users\t1528\Documents\site\site
git pull origin claude/enable-cocoon-child-cd2DT
python scripts/wp_draft.py push articles/drafts/{slug}.md
```

> ✅ push が成功したら、**WAF を ON に戻してください**。

### 5. push 後の手動作業の案内

WordPress 管理画面で以下を確認・実施する：
- アイキャッチ画像の設定
- カテゴリの確認
- 編集メモコメント（`<!-- 編集メモ -->`）の削除
- アフィリエイトリンクを ASP から取得して差し替え
- プレビュー確認

編集URL を表示して伝える：`https://ai-school-guide.com/wp-admin/post.php?post={wp_id}&action=edit`

## エラー対処

- `401 Unauthorized` → `.env` の `WP_USER` / `WP_APP_PASSWORD` を確認
- `403 Forbidden` on push → WAF を OFF にする（上記パターンC）
- `403 Forbidden` on upload-images → `upload_media()` を `multipart/form-data` で送信しているか確認
- `git pull` で conflict → `git stash` → `git pull` → `git stash pop` の順で実行
