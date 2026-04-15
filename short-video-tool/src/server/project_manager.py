"""
プロジェクト管理（保存・一覧・読み込み・複製・削除・リネーム）。
projects/ にJSONファイルとして保存。
"""
import os
import json
from datetime import datetime


def list_projects(base_dir: str) -> list[dict]:
    """プロジェクト一覧を取得（日付降順）"""
    project_dir = os.path.join(base_dir, "projects")
    if not os.path.isdir(project_dir):
        return []

    projects = []
    for filename in sorted(os.listdir(project_dir), reverse=True):
        if not filename.endswith(".json"):
            continue
        # オートセーブは一覧に出さない
        if filename.startswith("_autosave"):
            continue
        filepath = os.path.join(project_dir, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            projects.append({
                "filename": filename,
                "name": data.get("name", filename),
                "created_at": data.get("created_at", ""),
                "updated_at": data.get("updated_at", ""),
                "scene_count": len(data.get("scenes", [])),
                "total_duration": sum(
                    s.get("duration", 0) for s in data.get("scenes", [])
                ),
            })
        except (json.JSONDecodeError, IOError):
            continue
    return projects


def save_project(base_dir: str, project_data: dict, filename: str | None = None) -> dict:
    """プロジェクトを保存"""
    project_dir = os.path.join(base_dir, "projects")
    os.makedirs(project_dir, exist_ok=True)

    now = datetime.now()

    if filename:
        # 既存ファイルを上書き
        filepath = os.path.join(project_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                existing = json.load(f)
            project_data["created_at"] = existing.get("created_at", now.isoformat())
        else:
            project_data["created_at"] = now.isoformat()
    else:
        name = project_data.get("name", "unnamed")
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{name}.json"
        project_data["created_at"] = now.isoformat()

    project_data["updated_at"] = now.isoformat()

    filepath = os.path.join(project_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(project_data, f, ensure_ascii=False, indent=2)

    return {"filename": filename, "name": project_data.get("name", "")}


def load_project(base_dir: str, filename: str) -> dict | None:
    """プロジェクトを読み込む"""
    filepath = os.path.join(base_dir, "projects", filename)
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def duplicate_project(base_dir: str, filename: str) -> dict | None:
    """プロジェクトを複製する"""
    data = load_project(base_dir, filename)
    if data is None:
        return None

    data["name"] = data.get("name", "unnamed") + " (コピー)"
    return save_project(base_dir, data)


def delete_project(base_dir: str, filename: str) -> bool:
    """プロジェクトを削除"""
    filepath = os.path.join(base_dir, "projects", filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        return True
    return False


def rename_project(base_dir: str, filename: str, new_name: str) -> bool:
    """プロジェクトの名前を変更"""
    filepath = os.path.join(base_dir, "projects", filename)
    if not os.path.exists(filepath):
        return False
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    data["name"] = new_name
    data["updated_at"] = datetime.now().isoformat()
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return True
