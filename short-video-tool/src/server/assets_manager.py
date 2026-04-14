"""
素材管理（背景画像/動画、BGM）のファイル一覧・メタデータ管理。
"""
import os
import json

# 対応ファイル拡張子
IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.webp'}
VIDEO_EXTS = {'.mp4', '.mov', '.avi', '.webm'}
AUDIO_EXTS = {'.mp3', '.wav', '.ogg', '.m4a'}
FONT_EXTS = {'.ttf', '.otf', '.woff', '.woff2'}


def get_file_type(filename: str) -> str:
    """ファイル拡張子からタイプを判定"""
    ext = os.path.splitext(filename)[1].lower()
    if ext in IMAGE_EXTS:
        return 'image'
    if ext in VIDEO_EXTS:
        return 'video'
    if ext in AUDIO_EXTS:
        return 'audio'
    if ext in FONT_EXTS:
        return 'font'
    return 'unknown'


def list_assets(base_dir: str, asset_type: str) -> list[dict]:
    """
    指定フォルダの素材ファイル一覧を返す。サブフォルダ（カテゴリ）にも対応。

    asset_type: "backgrounds" | "bgm" | "fonts" | "overlays"
    """
    folder = os.path.join(base_dir, "assets", asset_type)
    if not os.path.isdir(folder):
        return []

    assets = []
    for root, dirs, files in os.walk(folder):
        # .gitkeep等を除外
        rel_root = os.path.relpath(root, folder)
        category = "" if rel_root == "." else rel_root.replace("\\", "/")

        for filename in sorted(files):
            filepath = os.path.join(root, filename)

            file_type = get_file_type(filename)
            if file_type == 'unknown':
                continue

            # メタデータファイルがあれば読み込む
            meta_path = filepath + '.json'
            tags = []
            if os.path.exists(meta_path):
                try:
                    with open(meta_path, 'r', encoding='utf-8') as f:
                        meta = json.load(f)
                        tags = meta.get('tags', [])
                except (json.JSONDecodeError, IOError):
                    pass

            rel_path = os.path.relpath(filepath, os.path.join(base_dir))
            url_path = "/" + rel_path.replace("\\", "/")

            assets.append({
                'filename': filename,
                'path': url_path,
                'type': file_type,
                'size': os.path.getsize(filepath),
                'tags': tags,
                'category': category,
            })

    return assets


def save_asset_tags(base_dir: str, asset_type: str, filename: str, tags: list[str]) -> bool:
    """素材にタグを保存する"""
    filepath = os.path.join(base_dir, "assets", asset_type, filename)
    if not os.path.exists(filepath):
        return False

    meta_path = filepath + '.json'
    meta = {}
    if os.path.exists(meta_path):
        try:
            with open(meta_path, 'r', encoding='utf-8') as f:
                meta = json.load(f)
        except (json.JSONDecodeError, IOError):
            pass

    meta['tags'] = tags
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    return True
