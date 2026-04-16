"""X (Twitter) への投稿モジュール

tweepy を使って Twitter API v2 経由でポストする。
"""

import tweepy

import config


def _get_client() -> tweepy.Client:
    return tweepy.Client(
        consumer_key=config.X_API_KEY,
        consumer_secret=config.X_API_SECRET,
        access_token=config.X_ACCESS_TOKEN,
        access_token_secret=config.X_ACCESS_TOKEN_SECRET,
    )


def _get_api_v1() -> tweepy.API:
    """画像アップロード用 (v1.1 API)"""
    auth = tweepy.OAuth1UserHandler(
        config.X_API_KEY,
        config.X_API_SECRET,
        config.X_ACCESS_TOKEN,
        config.X_ACCESS_TOKEN_SECRET,
    )
    return tweepy.API(auth)


def post(text: str, image_path: str | None = None) -> dict:
    """X にテキスト（＋画像）を投稿する

    Args:
        text: 投稿テキスト（280文字以内）
        image_path: 添付画像のパス（任意）

    Returns:
        API レスポンスの情報を辞書で返す
    """
    client = _get_client()
    media_ids = None

    if image_path:
        api_v1 = _get_api_v1()
        media = api_v1.media_upload(filename=image_path)
        media_ids = [media.media_id]

    response = client.create_tweet(text=text, media_ids=media_ids)
    tweet_data = response.data

    return {
        "platform": "X",
        "tweet_id": tweet_data["id"],
        "text": tweet_data["text"],
    }
