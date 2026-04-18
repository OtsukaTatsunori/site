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
    for p in posts:
        title = p["title"]["rendered"] or "(無題)"
        print(f"[{p['status']}] id={p['id']}  {title}")
        print(f"   edit: {wp.url}/wp-admin/post.php?post={p['id']}&action=edit")
    return 0


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

    allowed_dir = Path("articles/drafts").resolve()
    if not path.resolve().is_relative_to(allowed_dir):
        print("エラー: articles/drafts/ 内のファイルのみ指定できます。", file=sys.stderr)
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
    slug = meta.get("slug")
    excerpt = meta.get("excerpt")

    wp = WPClient()

    # カテゴリ解決
    category_ids: list[int] = []
    if meta.get("categories"):
        category_ids = wp.resolve_category_ids(list(meta["categories"]))

    wp_id = meta.get("wp_id")

    if wp_id:
        # 既存の下書きを更新
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
        # 新規作成
        result = wp.create_post(
            title=title,
            content=content_html,
            status="draft",
            slug=slug,
            excerpt=excerpt,
            categories=category_ids,
        )
        action = "作成"
        # frontmatter に wp_id を書き戻す（検証付き）
        post_id = result.get("id")
        if not isinstance(post_id, int) or post_id <= 0:
            print("エラー: WordPress APIから不正なIDが返されました。", file=sys.stderr)
            return 1
        meta["wp_id"] = post_id
        post.metadata = meta
        path.write_text(frontmatter.dumps(post), encoding="utf-8")

    print(f"✅ 下書き{action}完了: id={result['id']}  title={title}")
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

    sub.add_parser("categories", help="カテゴリ一覧を表示")

    sub.add_parser(
        "init-categories",
        help="サイト構造設計書のカテゴリ（7種）を一括作成",
    )

    p_push = sub.add_parser(
        "push", help="Markdownファイルを下書きとしてアップロード/更新"
    )
    p_push.add_argument("file", help="Markdownファイルのパス")

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
        "categories": cmd_categories,
        "init-categories": cmd_init_categories,
        "push": cmd_push,
        "upload-images": cmd_upload_images,
    }
    return handlers[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
