# 大人の学びなおし アフィリエイトサイト

Cocoon子テーマを管理するリポジトリです。

---

## このリポジトリについて

- `cocoon-child/` フォルダのみ管理しています
- WordPress本体・親テーマ・プラグインは含みません
- 親テーマ（Cocoon）は直接編集しない
- カスタマイズは必ず子テーマに書く

---

## ファイル構成

- `cocoon-child/style.css` ← テーマ宣言＋カスタムCSS
- `cocoon-child/functions.php` ← カスタム関数置き場
- `cocoon-child/screenshots/` ← 作業確認スクショ置き場（自分用）

---

## 必須プラグイン（3つのみ）

| プラグイン | 用途 |
|-----------|------|
| SiteGuard WP Plugin | セキュリティ |
| BackWPup | バックアップ |
| WP Multibyte Patch | 日本語対応 |

入れてはいけないプラグイン：
- All in One SEO / Yoast SEO / RankMath（Cocoonと重複してSEO逆効果）

---

## やってはいけないこと

1. 親テーマ（Cocoon）を直接編集しない
2. 本番環境に直接変更しない（Local WPで確認してから）
3. パスワード・APIキーをこのリポジトリに書かない
4. ユーザー名に `admin` を使わない
5. WordPress・Cocoon・プラグインの更新を放置しない

---

## セキュリティチェックリスト

- [ ] ユーザー名が `admin` ではない
- [ ] SiteGuard WP Plugin でログインURLを変更済み
- [ ] BackWPup で定期バックアップを設定済み
- [ ] SSL（https）が有効
- [ ] 強力なパスワードを使用
