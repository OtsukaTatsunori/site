"""
Markdownファイルから WordPress 下書き（draft）を作成・更新するCLI

使い方:
  # 接続確認
  python scripts/wp_draft.py ping

  # 下書きの新規作成
  python scripts/wp_draft.py push articles/drafts/sample.md

  # 既存の下書きを更新（frontmatter の wp_id を使って自動判定）
  python scripts/wp_draft.py push articles/drafts/sample.md

  # 下書き一覧
  python scripts/wp_draft.py list

  # カテゴリ一覧
  python scripts/wp_draft.py categories


Markdownの形式:
  ---
  title: 記事タイトル
  slug: article-slug
  excerpt: 記事の抜粋（任意）
  categories:
    - english
    - programming
  tags:
    - 初心者向け
  # 作成済みの下書きには wp_id が追記される（自動更新用）
  ---

  ここから本文（Markdown / HTML 混在可）
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import frontmatter
import markdown as md

from wp_client import WPClient


def md_to_html(text: str) -> str:
    """Markdown → HTML 変換。
    WordPress Gutenberg はHTMLをそのまま受け付けるのでシンプル変換で十分。
    拡張: 表、フェンスコード、見出しID、改行保持"""
    return md.markdown(
        text,
        extensions=[
            "tables",
            "fenced_code",
            "sane_lists",
            "nl2br",
        ],
    )


def extract_faq_jsonld(markdown_text: str) -> str:
    """Markdownから「### Q. 〜」パターンのFAQを抽出し、JSON-LD構造化データを生成。
    FAQが見つからなければ空文字列を返す。"""
    faq_items: list[dict] = []
    lines = markdown_text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # ### Q. で始まる行を質問として検出
        q_match = re.match(r"^###\s+Q\.\s*(.+)$", line)
        if q_match:
            question = q_match.group(1).strip()
            # 次の行以降から回答を収集（次の###か##まで）
            answer_lines: list[str] = []
            i += 1
            while i < len(lines):
                next_line = lines[i].strip()
                if next_line.startswith("### ") or next_line.startswith("## "):
                    break
                # 空行・引用ブロック・テーブルなどもテキストとして収集
                if next_line:
                    # Markdownの装飾を除去して平文に
                    clean = re.sub(r"\*\*(.+?)\*\*", r"\1", next_line)
                    clean = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", clean)
                    clean = re.sub(r"^>\s*", "", clean)
                    clean = re.sub(r"^[|>]+\s*", "", clean)
                    if clean and not clean.startswith("---"):
                        answer_lines.append(clean)
                i += 1
            if answer_lines:
                answer = " ".join(answer_lines)
                faq_items.append({
                    "@type": "Question",
                    "name": question,
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": answer,
                    },
                })
            continue
        i += 1

    if not faq_items:
        return ""

    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": faq_items,
    }
    script_tag = (
        '\n<script type="application/ld+json">\n'
        + json.dumps(schema, ensure_ascii=False, indent=2)
        + "\n</script>\n"
    )
    return script_tag


def cmd_ping(_args: argparse.Namespace) -> int:
    wp = WPClient()
    me = wp.ping()
    print(f"✅ 接続成功: {me.get('name')} (role: {', '.join(me.get('roles', []))})")
    print(f"   サイト: {wp.url}")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    wp = WPClient()
    posts = wp.list_posts(status=args.status)
    if not posts:
        print("投稿はありません。")
        return 0
    print(f"合計 {len(posts)} 件")
    for p in posts:
        title = p["title"]["rendered"] or "(無題)"
        slug = p.get("slug", "")
        print(f"[{p['status']:>7}] id={p['id']:>3}  slug={slug}  title={title}")
    return 0


def _find_missing_files() -> list[Path]:
    """未push記事のPathリストを返す（WordPressと照合）"""
    wp = WPClient()
    posts = wp.list_posts(status="draft,publish")
    wp_slugs = {p.get("slug", "") for p in posts}

    drafts_dir = Path("articles/drafts")
    missing_files: list[Path] = []
    for f in sorted(drafts_dir.glob("*.md")):
        if f.name.startswith("_"):
            continue
        post = frontmatter.load(f)
        slug = post.metadata.get("slug", f.stem)
        if slug not in wp_slugs:
            missing_files.append(f)
    return missing_files


def cmd_diff(args: argparse.Namespace) -> int:
    """ローカルのMD一覧とWordPressの投稿を照合し、未pushの記事を表示"""
    wp = WPClient()
    posts = wp.list_posts(status="draft,publish")
    wp_slugs = {p.get("slug", "") for p in posts}

    drafts_dir = Path("articles/drafts")
    local_files: list[tuple[str, str]] = []
    missing_files: list[Path] = []
    for f in sorted(drafts_dir.glob("*.md")):
        if f.name.startswith("_"):
            continue
        post = frontmatter.load(f)
        slug = post.metadata.get("slug", f.stem)
        local_files.append((slug, f.name))
        if slug not in wp_slugs:
            missing_files.append(f)

    print(f"ローカル記事: {len(local_files)} 件")
    print(f"WordPress登録済み: {len(wp_slugs)} 件")
    print(f"未push: {len(missing_files)} 件\n")
    if missing_files:
        print("=== 未pushの記事 ===")
        for f in missing_files:
            print(f"  {f}")
    return 0


def cmd_push_missing(args: argparse.Namespace) -> int:
    """未pushの記事をまとめてpush（WordPressと照合して差分だけ）"""
    import time

    missing = _find_missing_files()
    if not missing:
        print("✅ 未pushの記事はありません。")
        return 0

    print(f"📋 未push {len(missing)} 件をpushします。")
    if not args.yes:
        ans = input("続けますか？ [y/N]: ").strip().lower()
        if ans != "y":
            print("中止しました。")
            return 0

    success = 0
    failed: list[str] = []
    for i, f in enumerate(missing, 1):
        print(f"\n--- [{i}/{len(missing)}] {f.name} ---")
        try:
            # 既存のcmd_pushを再利用するため、argsを疑似作成
            fake_args = argparse.Namespace(file=str(f))
            rc = cmd_push(fake_args)
            if rc == 0:
                success += 1
            else:
                failed.append(f.name)
        except Exception as e:
            print(f"❌ エラー: {e}", file=sys.stderr)
            failed.append(f.name)
        # WAF対策: 連続リクエスト間に少し待つ
        if i < len(missing):
            time.sleep(1.5)

    print(f"\n===== 完了 =====")
    print(f"成功: {success} 件")
    print(f"失敗: {len(failed)} 件")
    if failed:
        print("失敗したファイル:")
        for name in failed:
            print(f"  {name}")
    return 0 if not failed else 1


def cmd_categories(_args: argparse.Namespace) -> int:
    wp = WPClient()
    cats = wp.list_categories()
    for c in sorted(cats, key=lambda x: x["id"]):
        print(f"id={c['id']:>3}  slug={c['slug']:<20} name={c['name']}")
    return 0


# サイト構造設計書（docs/site-structure.md）で定義したカテゴリ一覧
DEFAULT_CATEGORIES = [
    {
        "name": "英語・語学",
        "slug": "english",
        "description": "大人・社会人の英語学び直しや語学学習サービスを比較",
    },
    {
        "name": "プログラミング・IT",
        "slug": "programming",
        "description": "社会人向けプログラミングスクールやIT資格の比較",
    },
    {
        "name": "資格・検定",
        "slug": "qualification",
        "description": "社会人におすすめの資格・通信講座の比較",
    },
    {
        "name": "オンライン学習",
        "slug": "online-learning",
        "description": "Udemy、Schoo、グロービス学び放題などのオンライン学習サービス",
    },
    {
        "name": "教科別やり直し",
        "slug": "subject",
        "description": "英語、数学、歴史などの教科別学び直しガイド",
    },
    {
        "name": "補助金・制度",
        "slug": "subsidy",
        "description": "教育訓練給付金やリスキリング補助金の活用方法",
    },
    {
        "name": "年代別ガイド",
        "slug": "age-guide",
        "description": "20代・30代・40代・50代の年代別学び直しガイド",
    },
    {
        "name": "動画制作",
        "slug": "video-production",
        "description": "動画編集スクールやYouTube運営、動画制作スキルに関する比較・情報",
    },
]


def cmd_init_categories(_args: argparse.Namespace) -> int:
    """サイト構造設計書のカテゴリを一括作成（既存はスキップ）"""
    wp = WPClient()
    existing = {c["slug"]: c for c in wp.list_categories()}

    # まず「Uncategorized」を「お知らせ」にリネーム
    uncategorized = existing.get("uncategorized")
    if uncategorized:
        if uncategorized["name"].lower() == "uncategorized":
            wp.update_category(
                uncategorized["id"],
                name="お知らせ",
                slug="news",
                description="サイト運営からのお知らせ",
            )
            print("🔄 Uncategorized → お知らせ (news) にリネーム")
        else:
            print(f"ℹ️  uncategorized はすでに「{uncategorized['name']}」に変更済み")

    # 7カテゴリを作成
    for cat in DEFAULT_CATEGORIES:
        if cat["slug"] in existing:
            print(f"⏭️  既存: {cat['slug']:<20} ({cat['name']})")
            continue
        result = wp.create_category(
            name=cat["name"],
            slug=cat["slug"],
            description=cat["description"],
        )
        print(f"✅ 作成: id={result['id']:>3} slug={cat['slug']:<20} name={cat['name']}")

    print("\n完了しました。確認するには:")
    print("  python scripts/wp_draft.py categories")
    return 0


def cmd_push(args: argparse.Namespace) -> int:
    path = Path(args.file)
    if not path.exists():
        print(f"エラー: ファイルが見つかりません: {path}", file=sys.stderr)
        return 1

    allowed_dirs = [Path("articles/drafts").resolve(), Path("articles/pages").resolve()]
    if not any(path.resolve().is_relative_to(d) for d in allowed_dirs):
        print("エラー: articles/drafts/ または articles/pages/ 内のファイルのみ指定できます。", file=sys.stderr)
        return 1

    post = frontmatter.load(path)
    meta = post.metadata
    body_md = post.content

    title = meta.get("title")
    if not title:
        print("エラー: frontmatter に title がありません。", file=sys.stderr)
        return 1

    # UPLOAD_URL:filename.png を実際のURLに置換
    url_map_path = Path("articles/images/uploaded_urls.txt")
    if url_map_path.exists():
        url_map: dict[str, str] = {}
        for line in url_map_path.read_text(encoding="utf-8").strip().splitlines():
            parts = line.split("\t", 1)
            if len(parts) == 2:
                url_map[parts[0]] = parts[1]
        for filename, url in url_map.items():
            body_md = body_md.replace(f"UPLOAD_URL:{filename}", url)

    content_html = md_to_html(body_md)

    # FAQ構造化データ（JSON-LD）を自動挿入
    faq_jsonld = extract_faq_jsonld(body_md)
    if faq_jsonld:
        content_html += faq_jsonld
        faq_count = faq_jsonld.count('"@type": "Question"')
        print(f"📋 FAQ構造化データ: {faq_count}件のQ&Aを検出・挿入")

    slug = meta.get("slug")
    excerpt = meta.get("excerpt")
    content_type = meta.get("type", "post")  # "post" or "page"

    wp = WPClient()

    # カテゴリ解決（固定ページでは不要）
    category_ids: list[int] = []
    if content_type == "post" and meta.get("categories"):
        category_ids = wp.resolve_category_ids(list(meta["categories"]))

    wp_id = meta.get("wp_id")

    if content_type == "page":
        # 固定ページの作成/更新
        if wp_id:
            result = wp.update_page(
                int(wp_id),
                title=title,
                content=content_html,
                slug=slug,
                excerpt=excerpt or "",
            )
            action = "更新"
        else:
            result = wp.create_page(
                title=title,
                content=content_html,
                status="draft",
                slug=slug,
                excerpt=excerpt,
            )
            action = "作成"
            post_id = result.get("id")
            if not isinstance(post_id, int) or post_id <= 0:
                print("エラー: WordPress APIから不正なIDが返されました。", file=sys.stderr)
                return 1
            meta["wp_id"] = post_id
            post.metadata = meta
            path.write_text(frontmatter.dumps(post), encoding="utf-8")
        label = "固定ページ"
    else:
        # 投稿の作成/更新
        if wp_id:
            result = wp.update_post(
                int(wp_id),
                title=title,
                content=content_html,
                slug=slug,
                excerpt=excerpt or "",
                categories=category_ids,
            )
            action = "更新"
        else:
            result = wp.create_post(
                title=title,
                content=content_html,
                status="draft",
                slug=slug,
                excerpt=excerpt,
                categories=category_ids,
            )
            action = "作成"
            post_id = result.get("id")
            if not isinstance(post_id, int) or post_id <= 0:
                print("エラー: WordPress APIから不正なIDが返されました。", file=sys.stderr)
                return 1
            meta["wp_id"] = post_id
            post.metadata = meta
            path.write_text(frontmatter.dumps(post), encoding="utf-8")
        label = "下書き"

    print(f"✅ {label}{action}完了: id={result['id']}  title={title}")
    print(
        f"   編集URL: {wp.url}/wp-admin/post.php?post={result['id']}&action=edit"
    )
    print(f"   プレビュー: {result.get('link', '(なし)')}")
    return 0


def cmd_upload_images(args: argparse.Namespace) -> int:
    """articles/images/ 内の画像をWordPressにアップロードし、URLマッピングを表示"""
    import time

    img_dir = Path(args.dir)
    if not img_dir.exists():
        print(f"エラー: ディレクトリが見つかりません: {img_dir}", file=sys.stderr)
        return 1

    images = sorted(img_dir.glob("*.png")) + sorted(img_dir.glob("*.jpg"))
    if not images:
        print("アップロード対象の画像がありません。")
        return 0

    # 既存のマッピングを読み込む（成功済みはスキップ）
    map_path = img_dir / "uploaded_urls.txt"
    existing: dict[str, str] = {}
    if map_path.exists():
        for line in map_path.read_text(encoding="utf-8").strip().splitlines():
            parts = line.split("\t", 1)
            if len(parts) == 2:
                existing[parts[0]] = parts[1]

    wp = WPClient()
    results: dict[str, str] = dict(existing)

    for i, img_path in enumerate(images):
        if img_path.name in existing:
            print(f"⏭️  {img_path.name}（アップロード済み、スキップ）")
            continue

        if i > 0:
            time.sleep(2)  # WAF対策: リクエスト間に2秒待つ

        # SEO用alt_text: ファイル名→日本語マッピング
        alt_map = {
            "eyecatch-video-editing-beginner": "動画編集は未経験でも始められる？失敗しない始め方とおすすめスクール",
            "eyecatch-free-video-editing-software": "無料の動画編集ソフトおすすめ7選 用途別に徹底比較",
            "comparison-self-vs-school": "動画編集の独学とスクールの費用・期間・挫折率を比較した図",
            "roadmap-4steps": "動画編集未経験から案件獲得までの4ステップロードマップ",
            "usage-matrix": "無料動画編集ソフトの用途別おすすめ早見表",
            "income-roadmap": "動画編集未経験からの収入推移イメージ",
        }
        alt = alt_map.get(img_path.stem, img_path.stem.replace("-", " "))
        try:
            media = wp.upload_media(str(img_path), alt_text=alt)
            url = media.get("source_url", "")
            media_id = media.get("id", "")
            results[img_path.name] = url
            print(f"✅ {img_path.name} → id={media_id}")
            print(f"   URL: {url}")
        except Exception as e:
            print(f"❌ {img_path.name}: {e}", file=sys.stderr)

    # マッピングファイルを保存
    with open(map_path, "w", encoding="utf-8") as f:
        for name, url in sorted(results.items()):
            f.write(f"{name}\t{url}\n")
    print(f"\n📄 URLマッピング保存: {map_path}")
    print(f"成功: {len(results)}/{len(images)}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Markdownから WordPress 下書きを作成・更新するCLI"
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("ping", help="WordPress APIへの接続を確認")

    p_list = sub.add_parser("list", help="投稿一覧を表示")
    p_list.add_argument(
        "--status",
        default="draft,publish",
        help="対象のステータス（カンマ区切り）。default: draft,publish",
    )

    sub.add_parser("diff", help="ローカルMDとWordPress投稿を照合し未pushを表示")

    sub.add_parser("categories", help="カテゴリ一覧を表示")

    sub.add_parser(
        "init-categories",
        help="サイト構造設計書のカテゴリ（7種）を一括作成",
    )

    p_push = sub.add_parser(
        "push", help="Markdownファイルを下書きとしてアップロード/更新"
    )
    p_push.add_argument("file", help="Markdownファイルのパス")

    p_pm = sub.add_parser(
        "push-missing", help="WordPress未登録の記事をまとめてpush"
    )
    p_pm.add_argument("-y", "--yes", action="store_true", help="確認なしで実行")

    p_upload = sub.add_parser(
        "upload-images", help="画像フォルダをWordPressメディアにアップロード"
    )
    p_upload.add_argument(
        "dir",
        nargs="?",
        default="articles/images",
        help="画像フォルダのパス（default: articles/images）",
    )

    args = parser.parse_args()

    handlers = {
        "ping": cmd_ping,
        "list": cmd_list,
        "diff": cmd_diff,
        "categories": cmd_categories,
        "init-categories": cmd_init_categories,
        "push": cmd_push,
        "push-missing": cmd_push_missing,
        "upload-images": cmd_upload_images,
    }
    return handlers[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
