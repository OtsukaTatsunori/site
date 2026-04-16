"""環境変数から各種APIの認証情報を読み込む"""

import os
import sys
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))


def _require(name: str) -> str:
    value = os.getenv(name)
    if not value:
        print(f"エラー: 環境変数 {name} が設定されていません。.env ファイルを確認してください。")
        sys.exit(1)
    return value


# X (Twitter) API
X_API_KEY = _require("X_API_KEY")
X_API_SECRET = _require("X_API_SECRET")
X_ACCESS_TOKEN = _require("X_ACCESS_TOKEN")
X_ACCESS_TOKEN_SECRET = _require("X_ACCESS_TOKEN_SECRET")

# Instagram Graph API
INSTAGRAM_BUSINESS_ACCOUNT_ID = _require("INSTAGRAM_BUSINESS_ACCOUNT_ID")
INSTAGRAM_ACCESS_TOKEN = _require("INSTAGRAM_ACCESS_TOKEN")

# サイト情報
SITE_URL = os.getenv("SITE_URL", "")
SITE_NAME = os.getenv("SITE_NAME", "大人の学びなおし")
