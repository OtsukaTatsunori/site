"""投稿コンテンツを作成するモジュール

テンプレートを使って X / Instagram 向けの投稿文を生成する。
"""

from dataclasses import dataclass


@dataclass
class PostContent:
    """X と Instagram 両方の投稿内容をまとめるデータクラス"""
    x_text: str
    instagram_caption: str
    image_path: str | None = None


# ---------------------------------------------------------------------------
# テンプレート
# ---------------------------------------------------------------------------

# X 用テンプレート（280文字以内）
X_TEMPLATES = {
    "blog_share": (
        "📝 新着記事\n\n"
        "{title}\n\n"
        "{summary}\n\n"
        "▶ {url}\n\n"
        "{hashtags}"
    ),
    "tip": (
        "💡 {category}のワンポイント\n\n"
        "{tip_text}\n\n"
        "{hashtags}"
    ),
    "custom": "{text}",
}

# Instagram 用テンプレート（2,200文字以内）
INSTAGRAM_TEMPLATES = {
    "blog_share": (
        "📝 新着記事を公開しました！\n\n"
        "【{title}】\n\n"
        "{summary}\n\n"
        "詳しくはプロフィールのリンクから👆\n\n"
        "---\n"
        "{hashtags}"
    ),
    "tip": (
        "💡 {category}のワンポイント\n\n"
        "{tip_text}\n\n"
        "役に立ったら保存&フォローお願いします🙏\n\n"
        "---\n"
        "{hashtags}"
    ),
    "custom": "{text}",
}

# デフォルトハッシュタグ
DEFAULT_HASHTAGS = [
    "#大人の学びなおし",
    "#学び直し",
    "#スキルアップ",
    "#自己投資",
]


def _format_hashtags(extra_tags: list[str] | None = None) -> str:
    tags = DEFAULT_HASHTAGS.copy()
    if extra_tags:
        tags.extend(extra_tags)
    return " ".join(tags)


def create_blog_share(
    title: str,
    summary: str,
    url: str,
    hashtags: list[str] | None = None,
    image_path: str | None = None,
) -> PostContent:
    """ブログ記事をシェアする投稿を作成"""
    tag_str = _format_hashtags(hashtags)

    x_text = X_TEMPLATES["blog_share"].format(
        title=title, summary=summary, url=url, hashtags=tag_str,
    )
    instagram_caption = INSTAGRAM_TEMPLATES["blog_share"].format(
        title=title, summary=summary, hashtags=tag_str,
    )
    return PostContent(
        x_text=x_text,
        instagram_caption=instagram_caption,
        image_path=image_path,
    )


def create_tip(
    category: str,
    tip_text: str,
    hashtags: list[str] | None = None,
    image_path: str | None = None,
) -> PostContent:
    """ワンポイント知識の投稿を作成"""
    tag_str = _format_hashtags(hashtags)

    x_text = X_TEMPLATES["tip"].format(
        category=category, tip_text=tip_text, hashtags=tag_str,
    )
    instagram_caption = INSTAGRAM_TEMPLATES["tip"].format(
        category=category, tip_text=tip_text, hashtags=tag_str,
    )
    return PostContent(
        x_text=x_text,
        instagram_caption=instagram_caption,
        image_path=image_path,
    )


def create_custom(
    text: str,
    instagram_text: str | None = None,
    hashtags: list[str] | None = None,
    image_path: str | None = None,
) -> PostContent:
    """自由入力で投稿を作成"""
    tag_str = _format_hashtags(hashtags)

    x_text = f"{text}\n\n{tag_str}"
    ig_body = instagram_text if instagram_text else text
    instagram_caption = f"{ig_body}\n\n{tag_str}"

    return PostContent(
        x_text=x_text,
        instagram_caption=instagram_caption,
        image_path=image_path,
    )


def validate_post(content: PostContent) -> list[str]:
    """投稿内容のバリデーション。問題があればメッセージのリストを返す"""
    issues: list[str] = []
    if len(content.x_text) > 280:
        issues.append(
            f"X の投稿が280文字を超えています（現在 {len(content.x_text)} 文字）"
        )
    if len(content.instagram_caption) > 2200:
        issues.append(
            f"Instagram のキャプションが2,200文字を超えています"
            f"（現在 {len(content.instagram_caption)} 文字）"
        )
    return issues
