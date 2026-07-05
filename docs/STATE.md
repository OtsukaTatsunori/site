# プロジェクト状態（最終更新: 2026-07-05）

> このファイルは次のセッション（モデル問わず）が最初に読む申し送り。大きな区切りごとに更新すること。

## 今どこにいるか
- 記事113本（AI 46＋動画編集 67）をWordPressに登録済み・公開済み。全記事に運営者コメント欄（voice-box）挿入済み
- 診断LP `https://ai-school-guide.com/shindan/`（静的HTML）が本番稼働。広告出稿前の仕上げ段階
- 法務3ページ（privacy-policy / about / contact）作成済み・push済み
- Search Console 登録済み（URLプレフィックス）。サイトマップ送信・インデックス作業は進行中

## 主要な構成
- 記事: `articles/drafts/*.md` → `wp_draft.py push`（wp_idで更新判定）
- 固定ページ: `articles/pages/*.md`（frontmatter `type: page`、`body_class`対応）
- 診断LP: `static/shindan/index.html` — **WordPress外**。反映はConoHaファイルマネージャーで上書きアップロード
- CSS: `cocoon-child/style.css` → WordPressの「外観→カスタマイズ→追加CSS」に**全文貼り付け**運用（変更時は貼り直し依頼が必要）
- 便利コマンド: `wp_draft.py diff / push-missing / push-all / init-categories`（いずれも冪等）

## 進行中のタスク
- [ ] ASP登録（A8.net・もしも・afb）と各スクール提携申請 — ユーザー側の作業待ち
- [ ] 診断LPのアフィリURL差し替え — `static/shindan/index.html` の `AFF` オブジェクト（★コメントあり）に提携URLを入れる
- [ ] GA4＋広告コンバージョンタグ埋め込み — 広告媒体（Google/Meta）決定待ち
- [ ] 診断LPのプラン表記を正確な数字に更新 — ASP提携後に正式データで差し替え
- [ ] WordPressサイトアイコン設定 — `static/shindan/favicon-512.png`（ロボット版）を 外観→カスタマイズ→サイト基本情報 に

## 保留・確認事項
- DMM 生成AI CAMP: 2026年3月以降は補助金対象外・月額制に変更された情報あり → LP文面は補助金非対応として調整済みだが、提携時に最新条件を再確認
- Aidemy Premium: 2026年6月末サービス終了予定 → 記事内の記述は将来的に削除・更新が必要
- WordPress側の旧診断ページ（school-concierge-lp, id=512）: 不要。ゴミ箱へ移動推奨（ユーザー操作）

## 環境の落とし穴（詳細は docs/LESSONS.md）
- script入りコンテンツのAPI pushはWAFが403にする（WAF OFF→push→ON、または静的HTML）
- ユーザーはプログラミング初学者・Windows/PowerShell。手順は毎回 cd + pull から完全提示（CLAUDE.md参照）
- ユーザーローカルに未コミット変更が溜まりがち → pull失敗時は stash → pull → pop、コンフリクトは --ours 採用
