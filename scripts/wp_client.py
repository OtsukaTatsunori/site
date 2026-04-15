"""
WordPress REST API クライアント

下書きの作成・更新・一覧取得、カテゴリ取得などを行います。
認証は Application Password を使用。
"""
from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

# .env をリポジトリルートから読み込む
ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")


class WPClient:
    def __init__(self) -> None:
        self.url = os.getenv("WP_URL", "").rstrip("/")
        self.user = os.getenv("WP_USER", "")
        self.app_password = os.getenv("WP_APP_PASSWORD", "")

        if not all([self.url, self.user, self.app_password]):
            sys.exit(
                "エラー: .env に WP_URL / WP_USER / WP_APP_PASSWORD を設定してください。\n"
                "       .env.example をコピーして .env を作成してください。"
            )

        self.api = f"{self.url}/wp-json/wp/v2"
        self.auth = (self.user, self.app_password)

    # ---------- 接続確認 ----------
    def ping(self) -> dict[str, Any]:
        """認証して /users/me を取得できるか確認"""
        r = requests.get(f"{self.api}/users/me", auth=self.auth, timeout=15)
        r.raise_for_status()
        return r.json()

    # ---------- 投稿 ----------
    def create_post(
        self,
        title: str,
        content: str,
        status: str = "draft",
        slug: str | None = None,
        excerpt: str | None = None,
        categories: list[int] | None = None,
        tags: list[int] | None = None,
        meta: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "title": title,
            "content": content,
            "status": status,
        }
        if slug:
            payload["slug"] = slug
        if excerpt:
            payload["excerpt"] = excerpt
        if categories:
            payload["categories"] = categories
        if tags:
            payload["tags"] = tags
        if meta:
            payload["meta"] = meta

        r = requests.post(
            f"{self.api}/posts", auth=self.auth, json=payload, timeout=30
        )
        r.raise_for_status()
        return r.json()

    def update_post(self, post_id: int, **fields: Any) -> dict[str, Any]:
        r = requests.post(
            f"{self.api}/posts/{post_id}",
            auth=self.auth,
            json=fields,
            timeout=30,
        )
        r.raise_for_status()
        return r.json()

    def list_posts(
        self, status: str = "draft,publish", per_page: int = 20
    ) -> list[dict[str, Any]]:
        r = requests.get(
            f"{self.api}/posts",
            auth=self.auth,
            params={"status": status, "per_page": per_page, "context": "edit"},
            timeout=15,
        )
        r.raise_for_status()
        return r.json()

    def get_post(self, post_id: int) -> dict[str, Any]:
        r = requests.get(
            f"{self.api}/posts/{post_id}",
            auth=self.auth,
            params={"context": "edit"},
            timeout=15,
        )
        r.raise_for_status()
        return r.json()

    # ---------- カテゴリ / タグ ----------
    def list_categories(self) -> list[dict[str, Any]]:
        r = requests.get(
            f"{self.api}/categories",
            auth=self.auth,
            params={"per_page": 100},
            timeout=15,
        )
        r.raise_for_status()
        return r.json()

    def resolve_category_ids(self, names_or_slugs: list[str]) -> list[int]:
        """カテゴリ名またはスラッグのリストをIDのリストに変換"""
        if not names_or_slugs:
            return []
        cats = self.list_categories()
        ids: list[int] = []
        missing: list[str] = []
        for key in names_or_slugs:
            match = next(
                (c for c in cats if c["name"] == key or c["slug"] == key),
                None,
            )
            if match:
                ids.append(match["id"])
            else:
                missing.append(key)
        if missing:
            raise ValueError(f"カテゴリが見つかりません: {missing}")
        return ids

    def create_category(
        self,
        name: str,
        slug: str,
        description: str = "",
    ) -> dict[str, Any]:
        r = requests.post(
            f"{self.api}/categories",
            auth=self.auth,
            json={"name": name, "slug": slug, "description": description},
            timeout=15,
        )
        r.raise_for_status()
        return r.json()

    def update_category(self, cat_id: int, **fields: Any) -> dict[str, Any]:
        r = requests.post(
            f"{self.api}/categories/{cat_id}",
            auth=self.auth,
            json=fields,
            timeout=15,
        )
        r.raise_for_status()
        return r.json()

    def list_tags(self) -> list[dict[str, Any]]:
        r = requests.get(
            f"{self.api}/tags",
            auth=self.auth,
            params={"per_page": 100},
            timeout=15,
        )
        r.raise_for_status()
        return r.json()
