# プロジェクト固有の指示

このファイルは Claude が毎回の会話で参照する永続的な指示です。

---

## 🔁 セッション開始時の必須プロトコル

**どのモデルで動いていても、大きめのタスクを始める前に必ず以下を実行する：**

1. `.claude/skills/kaizen-loop.md` を読む（働き方のOS。検証ループ・失敗プロトコル・セルフチェック5問）
2. `docs/STATE.md` を読む（プロジェクトの現在地と進行中タスク）
3. `docs/LESSONS.md` の「一般化」行を流し読みする（過去の罠を踏まない）

**セッション終了時・大きな区切りで：** STATE.md を更新し、新しい教訓があれば LESSONS.md に追記する。

## ユーザープロフィール

- **プログラミング初学者**
- 主な作業環境: Windows PC（PowerShell）
- リポジトリのローカルパス: `C:\Users\t1528\Documents\site\site`
- 作業ブランチ: `claude/enable-cocoon-child-cd2DT`
- WordPress: `https://ai-school-guide.com`

## 回答のルール

### 1. 完全な手順を常に提示する

Windows側で実行してもらうコマンドは、以下を**毎回**すべて含める（省略禁止）：

```powershell
cd C:\Users\t1528\Documents\site\site
git pull origin claude/enable-cocoon-child-cd2DT
（メインのコマンド）
```

※ `git pull` でコンフリクトが予想される場合は `git stash` → `git pull` → `git stash pop` の流れを示す。

### 2. ユーザーの知識を仮定しない

以下を**解説なしに使わない**：
- `cd` / `ls` / `explorer` / `start` 等のコマンド
- ファイルパスの意味
- git の操作（stash, checkout, pull, push）
- Python / pip の使い方

初出時は一言で説明を添える。例：「`explorer フォルダ名`でそのフォルダを開きます」

### 3. ファイルを開く方法を具体的に示す

画像やファイルの確認を促すときは、必ず開き方を書く。例：
- `explorer articles\images` でフォルダを開く
- `start ファイル名.png` で画像を直接開く
- ダブルクリックで開く
- スクリーンショットは **Win + Shift + S** で撮影、**Ctrl + V** で貼り付け

### 4. マルチステップのタスクは一括で提示

途中まで書いて「ここまで実行して」と区切らない。全手順を1つのコードブロックで出す。ただし **WAF OFF** のような手動操作が挟まる場合は、その直前でコードブロックを分割し、手動操作を明記する。

### 5. エラーが出たときの原因の可能性を併記

コマンドが失敗する可能性が高い箇所は、先回りで「もしXXエラーが出たら△△してください」と書く。

### 6. 日本語の語尾は「〜です・ます」調

雑談調にせず、丁寧な案内役の口調を維持する。

---

## このプロジェクトの約束事

### ディレクトリ構成

```
site/
├── articles/
│   ├── drafts/         ← 記事Markdown（frontmatter付き）
│   └── images/         ← 記事用画像（自動生成＋アップロード）
├── cocoon-child/       ← WordPress子テーマ
├── docs/
│   ├── editorial-policy.md            ← 編集方針・18原則
│   ├── article-writing-guide.md       ← 記事の書き方（How）
│   ├── site-structure.md              ← カテゴリ構成
│   ├── keyword-research.md            ← KW調査
│   └── video-production-content-plan.md ← 動画制作カテゴリ記事マップ
├── scripts/
│   ├── wp_client.py                   ← WordPress REST APIクライアント
│   ├── wp_draft.py                    ← Markdown→WP下書きCLI
│   └── generate_images_v2.py          ← Playwright画像生成
└── .claude/
    └── skills/                        ← プロジェクト固有のスキル
```

### 記事作成のフロー

1. KW選定 → `docs/video-production-content-plan.md` でカニバリ確認
2. 構成案を立てる（18原則に照らす）
3. `articles/drafts/{slug}.md` に Markdown で執筆
4. `generate_images_v2.py` で画像生成
5. `wp_draft.py upload-images` で画像アップロード
6. `wp_draft.py push` で記事アップロード
7. 記事1（既存投稿の更新）は WAF OFF → push → WAF ON の手順が必要

### WAF（ConoHa WING）

記事push時に 403 になったら、**ConoHa WING コントロールパネル → サイトセキュリティ → WAF** を OFF にする。push 成功後に ON に戻す。

### 編集方針

- **18原則**（`docs/editorial-policy.md` 参照）に沿って記事を書く
- カニバリ回避：ピラー記事「動画編集 未経験」との役割分担を明確にする
- 文字数：比較・情報系は 7,000〜8,000字目安

### 画像生成

- **モバイル最適化**（幅800px、フォント最小18px、1カラム）
- **マイベスト風**（白背景、◎○△× 評価、統一ブランドヘッダー）
- 画像ファイル名は英語（WordPress URLに使われる）
- alt属性は日本語でメインキーワードを含める
- **ツールのスクリーンショットが必須な記事は作らない**（自動生成できないため）
- 図解・比較表・フロー図など、データ駆動で生成できる画像のみ使用する
- **スクショ必須で飛ばした記事は、作業完了時に「スクショ必須のため今回スキップした記事」として必ず一覧で報告する**（忘れ防止）

### セキュリティルール

- `.env` にシークレットを書く。ソースコードに直書き禁止
- `.env` は `.gitignore` で除外済み。**絶対にコミットしない**
- WordPress API は **HTTPS のみ**（`wp_client.py` で強制チェック済み）
- ユーザー入力を `exec()` / `eval()` / `os.system()` に渡さない
- `push` コマンドは `articles/drafts/` 内のファイルのみ受け付ける（パストラバーサル防止）
- 依存パッケージはバージョンを固定（`requirements.txt`）
- 新しいパッケージを追加したら `pip audit` でチェック
- `--dangerously-skip-permissions` は使わない
- 他人のリポジトリを Claude Code で安易に開かない

### コミット＆プッシュ

コードや記事を変更したら、自動でコミット＆プッシュする。コミットメッセージは変更意図を1〜3行で記載。

---

## よくある質問への定型応答

### 「画像を確認したい」

```powershell
explorer articles\images
```
でフォルダを開き、ダブルクリックで画像を開く。スクショは **Win + Shift + S**。

### 「WordPressに記事をあげたい」

画像生成済みの場合：
```powershell
cd C:\Users\t1528\Documents\site\site
git pull origin claude/enable-cocoon-child-cd2DT
python scripts/wp_draft.py push articles/drafts/{ファイル名}.md
```

新規記事＋画像の場合：
```powershell
cd C:\Users\t1528\Documents\site\site
git pull origin claude/enable-cocoon-child-cd2DT
python scripts/generate_images_v2.py
del articles\images\uploaded_urls.txt
python scripts/wp_draft.py upload-images
python scripts/wp_draft.py push articles/drafts/{ファイル名}.md
```

既存記事の更新は WAF OFF → push → WAF ON が必要。

### 「画像を再生成したい」

```powershell
cd C:\Users\t1528\Documents\site\site
git pull origin claude/enable-cocoon-child-cd2DT
python scripts/generate_images_v2.py
```

サムネイルが古いまま見える場合は、**画像を右クリック → プログラムから開く → フォト**で直接開く。
