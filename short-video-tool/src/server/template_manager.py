"""
テンプレート管理（保存・一覧・読み込み・削除）。
テンプレートは templates/ にJSONファイルとして保存。
"""
import os
import json
from datetime import datetime


def list_templates(base_dir: str) -> list[dict]:
    """テンプレート一覧を取得"""
    template_dir = os.path.join(base_dir, "templates")
    if not os.path.isdir(template_dir):
        return []

    templates = []
    for filename in sorted(os.listdir(template_dir), reverse=True):
        if not filename.endswith(".json"):
            continue
        filepath = os.path.join(template_dir, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            templates.append({
                "filename": filename,
                "name": data.get("name", filename),
                "created_at": data.get("created_at", ""),
                "telop_style": data.get("telop_style", "standard"),
                "transition": data.get("transition", "cut"),
                "aspect_ratio": data.get("aspect_ratio", "9:16"),
            })
        except (json.JSONDecodeError, IOError):
            continue
    return templates


def save_template(base_dir: str, template_data: dict) -> dict:
    """テンプレートを保存"""
    template_dir = os.path.join(base_dir, "templates")
    os.makedirs(template_dir, exist_ok=True)

    name = template_data.get("name", "unnamed")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{name}.json"
    filepath = os.path.join(template_dir, filename)

    template_data["created_at"] = datetime.now().isoformat()

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(template_data, f, ensure_ascii=False, indent=2)

    return {"filename": filename, "name": name}


def load_template(base_dir: str, filename: str) -> dict | None:
    """テンプレートを読み込む"""
    filepath = os.path.join(base_dir, "templates", filename)
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def delete_template(base_dir: str, filename: str) -> bool:
    """テンプレートを削除"""
    filepath = os.path.join(base_dir, "templates", filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        return True
    return False
