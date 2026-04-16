#!/usr/bin/env python3
"""SNS 自動投稿ツール — 大人の学びなおし

使い方:
    python main.py blog   --title "記事タイトル" --summary "要約" --url "URL"
    python main.py tip    --category "英語" --tip "ワンポイント内容"
    python main.py custom --text "自由なテキスト"

オプション:
    --image       画像パス (X用) または 画像URL (Instagram用)
    --hashtags    追加ハッシュタグ（カンマ区切り）
    --x-only      X のみに投稿
    --ig-only     Instagram のみに投稿
    --dry-run     投稿せずにプレビューだけ表示
"""

import argparse
import sys

from content_creator import (
    PostContent,
    create_blog_share,
    create_custom,
    create_tip,
    validate_post,
)


def _parse_hashtags(raw: str | None) -> list[str] | None:
    if not raw:
        return None
    return [f"#{t.strip().lstrip('#')}" for t in raw.split(",") if t.strip()]


def _preview(content: PostContent) -> None:
    print("=" * 50)
    print("【X 投稿プレビュー】")
    print("-" * 50)
    print(content.x_text)
    print(f"（{len(content.x_text)} 文字）")
    print()
    print("=" * 50)
    print("【Instagram 投稿プレビュー】")
    print("-" * 50)
    print(content.instagram_caption)
    print(f"（{len(content.instagram_caption)} 文字）")
    print("=" * 50)

    if content.image_path:
        print(f"📷 画像: {content.image_path}")

    issues = validate_post(content)
    if issues:
        print()
        print("⚠️  注意:")
        for issue in issues:
            print(f"  - {issue}")


def _post(content: PostContent, x_only: bool, ig_only: bool) -> None:
    results = []

    if not ig_only:
        import x_poster

        print("X に投稿中...")
        try:
            result = x_poster.post(content.x_text, content.image_path)
            results.append(result)
            print(f"  ✅ X 投稿成功 (ID: {result['tweet_id']})")
        except Exception as e:
            print(f"  ❌ X 投稿失敗: {e}")

    if not x_only:
        import instagram_poster

        if not content.image_path:
            print("  ⚠️  Instagram は画像URLが必須です。--image で画像URLを指定してください。")
        else:
            print("Instagram に投稿中...")
            try:
                result = instagram_poster.post(
                    content.instagram_caption, content.image_path
                )
                results.append(result)
                print(f"  ✅ Instagram 投稿成功 (ID: {result['post_id']})")
            except Exception as e:
                print(f"  ❌ Instagram 投稿失敗: {e}")

    if results:
        print()
        print("投稿完了:")
        for r in results:
            print(f"  - {r['platform']}: OK")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="SNS 自動投稿ツール — 大人の学びなおし",
    )
    subparsers = parser.add_subparsers(dest="command", help="投稿タイプ")

    # blog サブコマンド
    blog_parser = subparsers.add_parser("blog", help="ブログ記事をシェア")
    blog_parser.add_argument("--title", required=True, help="記事タイトル")
    blog_parser.add_argument("--summary", required=True, help="記事の要約")
    blog_parser.add_argument("--url", required=True, help="記事URL")

    # tip サブコマンド
    tip_parser = subparsers.add_parser("tip", help="ワンポイント知識を投稿")
    tip_parser.add_argument("--category", required=True, help="カテゴリ名")
    tip_parser.add_argument("--tip", required=True, help="ワンポイント内容")

    # custom サブコマンド
    custom_parser = subparsers.add_parser("custom", help="自由テキストで投稿")
    custom_parser.add_argument("--text", required=True, help="投稿テキスト")
    custom_parser.add_argument("--ig-text", help="Instagram 用テキスト（省略時は --text と同じ）")

    # 共通オプション
    for p in [blog_parser, tip_parser, custom_parser]:
        p.add_argument("--image", help="画像パス/URL")
        p.add_argument("--hashtags", help="追加ハッシュタグ（カンマ区切り）")
        p.add_argument("--x-only", action="store_true", help="X のみ投稿")
        p.add_argument("--ig-only", action="store_true", help="Instagram のみ投稿")
        p.add_argument("--dry-run", action="store_true", help="投稿せずプレビュー表示")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    hashtags = _parse_hashtags(args.hashtags)

    # コンテンツ作成
    if args.command == "blog":
        content = create_blog_share(
            title=args.title,
            summary=args.summary,
            url=args.url,
            hashtags=hashtags,
            image_path=args.image,
        )
    elif args.command == "tip":
        content = create_tip(
            category=args.category,
            tip_text=args.tip,
            hashtags=hashtags,
            image_path=args.image,
        )
    elif args.command == "custom":
        content = create_custom(
            text=args.text,
            instagram_text=args.ig_text,
            hashtags=hashtags,
            image_path=args.image,
        )

    # バリデーション
    issues = validate_post(content)
    if issues:
        print("⚠️  投稿内容に問題があります:")
        for issue in issues:
            print(f"  - {issue}")
        if not args.dry_run:
            print("投稿を中止しました。内容を修正してください。")
            sys.exit(1)

    # プレビュー / 投稿
    _preview(content)

    if args.dry_run:
        print("\n(ドライランモード — 実際には投稿されていません)")
        return

    print()
    confirm = input("この内容で投稿しますか？ (y/N): ").strip().lower()
    if confirm != "y":
        print("投稿をキャンセルしました。")
        return

    _post(content, args.x_only, args.ig_only)


if __name__ == "__main__":
    main()
