"""Instagram への投稿モジュール

Instagram Graph API を使って投稿する。
Instagram Graph API では画像は公開URLが必要（ローカルファイル直接アップロード不可）。
"""

import time

import requests

import config

GRAPH_API_BASE = "https://graph.facebook.com/v21.0"


def _create_media_container(
    image_url: str, caption: str
) -> str:
    """メディアコンテナを作成して ID を返す"""
    url = f"{GRAPH_API_BASE}/{config.INSTAGRAM_BUSINESS_ACCOUNT_ID}/media"
    payload = {
        "image_url": image_url,
        "caption": caption,
        "access_token": config.INSTAGRAM_ACCESS_TOKEN,
    }
    resp = requests.post(url, data=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()["id"]


def _publish_media(container_id: str) -> str:
    """メディアコンテナを公開して投稿 ID を返す"""
    url = f"{GRAPH_API_BASE}/{config.INSTAGRAM_BUSINESS_ACCOUNT_ID}/media_publish"
    payload = {
        "creation_id": container_id,
        "access_token": config.INSTAGRAM_ACCESS_TOKEN,
    }
    resp = requests.post(url, data=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()["id"]


def post(caption: str, image_url: str) -> dict:
    """Instagram に画像付き投稿をする

    Args:
        caption: 投稿キャプション（2,200文字以内）
        image_url: 画像の公開URL（JPEG推奨、アスペクト比 4:5〜1.91:1）

    Returns:
        API レスポンスの情報を辞書で返す

    Note:
        Instagram Graph API はローカルファイルを直接アップロードできません。
        画像は公開URLで指定する必要があります。
        WordPress のメディアライブラリにアップロードした画像のURLが使えます。
    """
    container_id = _create_media_container(image_url, caption)

    # コンテナ処理待ち（Instagram側で画像を処理する時間が必要）
    time.sleep(5)

    post_id = _publish_media(container_id)

    return {
        "platform": "Instagram",
        "post_id": post_id,
        "caption": caption[:50] + "..." if len(caption) > 50 else caption,
    }
