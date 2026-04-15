"""
Short Video Generator Tool - Backend (FastAPI)
"""
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from datetime import datetime

from .scene_splitter import split_text_to_scenes
from .duration_calc import calc_scenes_duration
from .assets_manager import list_assets, save_asset_tags
from .video_generator import generate_scene_video, render_full_video, TELOP_PRESETS
from .tts_engine import get_tts_engine, get_audio_duration
from .template_manager import list_templates, save_template, load_template, delete_template
from .project_manager import (
    list_projects, save_project, load_project,
    duplicate_project, delete_project, rename_project,
)

# プロジェクトルートのパス
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

app = FastAPI(title="Short Video Generator")

# CORS設定（開発中はReactの開発サーバーからのアクセスを許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静的ファイルの配信（素材・出力ファイル）
app.mount("/assets", StaticFiles(directory=os.path.join(BASE_DIR, "assets")), name="assets")
app.mount("/output", StaticFiles(directory=os.path.join(BASE_DIR, "output")), name="output")

# Docker用: ビルド済みフロントエンドを配信
STATIC_DIR = os.path.join(BASE_DIR, "static")
if os.path.isdir(STATIC_DIR):
    app.mount("/_static", StaticFiles(directory=os.path.join(STATIC_DIR, "_static")), name="frontend_assets")


# --- リクエスト/レスポンスモデル ---

class SplitRequest(BaseModel):
    text: str

class MergeRequest(BaseModel):
    scenes: list[dict]
    merge_indices: list[int]  # 結合するシーンのインデックス（連続する2つ）

class SplitSceneRequest(BaseModel):
    scenes: list[dict]
    split_index: int        # 分割するシーンのインデックス
    split_position: int     # テキスト内の分割位置（文字数）

class CalcDurationRequest(BaseModel):
    scenes: list[dict]
    global_speed: float = 1.0

class TagsRequest(BaseModel):
    asset_type: str   # "backgrounds" | "bgm" | "fonts"
    filename: str
    tags: list[str]

class RenderSceneRequest(BaseModel):
    scene: dict
    aspect_ratio: str = "9:16"

class RenderRequest(BaseModel):
    scenes: list[dict]
    bgm: dict | None = None
    bgm_volume: int = 80
    aspect_ratio: str = "9:16"
    transition: str = "cut"
    output_format: str = "mp4"  # "mp4" | "gif"

class ProjectSaveRequest(BaseModel):
    name: str
    filename: str | None = None  # 上書き保存時
    scenes: list[dict] = []
    text: str = ""
    bgm: dict | None = None
    bgm_volume: int = 80
    transition: str = "cut"
    aspect_ratio: str = "9:16"
    tts_engine: str = "voicevox"
    tts_speaker_id: int = 1
    tts_speed: float = 1.0
    global_speed: float = 1.0
    template_name: str = ""

class ProjectRenameRequest(BaseModel):
    filename: str
    new_name: str

class TemplateSaveRequest(BaseModel):
    name: str
    telop_style: str = "standard"
    transition: str = "cut"
    aspect_ratio: str = "9:16"
    bgm: dict | None = None
    bgm_volume: int = 80
    tts_engine: str = "voicevox"
    tts_speaker_id: int = 1
    tts_speed: float = 1.0
    ken_burns: bool = False

class TTSSynthRequest(BaseModel):
    text: str
    scene_id: int
    speaker_id: int = 1
    speed: float = 1.0
    engine: str = "voicevox"

class TTSBatchRequest(BaseModel):
    scenes: list[dict]
    speaker_id: int = 1
    speed: float = 1.0
    engine: str = "voicevox"


# --- エンドポイント ---

@app.get("/api/health")
def health_check():
    """サーバーが正常に動作しているか確認するエンドポイント"""
    return {"status": "ok", "message": "Short Video Generator is running!"}


@app.post("/api/scenes/split-text")
def split_text(req: SplitRequest):
    """テキストをシーンに自動分割し、尺も自動算出する"""
    scenes = split_text_to_scenes(req.text)
    scenes = calc_scenes_duration(scenes)
    return {"scenes": scenes}


@app.post("/api/scenes/calc-duration")
def calc_duration(req: CalcDurationRequest):
    """各シーンの尺を再計算する"""
    scenes = calc_scenes_duration(req.scenes, req.global_speed)
    return {"scenes": scenes}


@app.post("/api/scenes/merge")
def merge_scenes(req: MergeRequest):
    """隣接する2つのシーンを結合する"""
    scenes = req.scenes
    idx = req.merge_indices[0]
    if idx < 0 or idx + 1 >= len(scenes):
        return {"error": "結合できないインデックスです"}

    merged_text = scenes[idx]["text"] + scenes[idx + 1]["text"]
    merged_scene = {
        **scenes[idx],
        "text": merged_text,
    }
    new_scenes = scenes[:idx] + [merged_scene] + scenes[idx + 2:]
    # IDを振り直す
    for i, s in enumerate(new_scenes):
        s["id"] = i
    return {"scenes": new_scenes}


@app.post("/api/scenes/split-scene")
def split_scene(req: SplitSceneRequest):
    """1つのシーンを指定位置で2つに分割する"""
    scenes = req.scenes
    idx = req.split_index
    pos = req.split_position
    if idx < 0 or idx >= len(scenes):
        return {"error": "無効なインデックスです"}

    original_text = scenes[idx]["text"]
    if pos <= 0 or pos >= len(original_text):
        return {"error": "分割位置が無効です"}

    scene1 = {**scenes[idx], "text": original_text[:pos]}
    scene2 = {**scenes[idx], "text": original_text[pos:]}

    new_scenes = scenes[:idx] + [scene1, scene2] + scenes[idx + 1:]
    # IDを振り直す
    for i, s in enumerate(new_scenes):
        s["id"] = i
    return {"scenes": new_scenes}


# --- テロッププリセット ---

@app.get("/api/telop-presets")
def get_telop_presets():
    """テロッププリセット一覧を返す"""
    presets = []
    for key, val in TELOP_PRESETS.items():
        presets.append({
            "id": key,
            "label": val.get("label", key),
            "fontsize": val["fontsize"],
            "fontcolor": val["fontcolor"],
            "borderw": val["borderw"],
            "bordercolor": val["bordercolor"],
            "position": val["position"],
            "box": val.get("box", False),
            "boxcolor": val.get("boxcolor", ""),
        })
    return {"presets": presets}


# --- 素材管理 ---

ASSET_TYPES = ("backgrounds", "bgm", "fonts", "overlays", "se")


@app.get("/api/assets/{asset_type}")
def get_assets(asset_type: str):
    """素材一覧を取得する（backgrounds / bgm / fonts / overlays / se）"""
    if asset_type not in ASSET_TYPES:
        return {"error": "Invalid asset type"}
    assets = list_assets(BASE_DIR, asset_type)
    return {"assets": assets}


@app.post("/api/assets/{asset_type}/upload")
async def upload_assets(asset_type: str, files: list[UploadFile] = File(...), category: str = Form("")):
    """素材ファイルをアップロード（複数対応）"""
    if asset_type not in ASSET_TYPES:
        return {"error": "無効な素材タイプです"}

    target_dir = os.path.join(BASE_DIR, "assets", asset_type)
    if category:
        target_dir = os.path.join(target_dir, category)
    os.makedirs(target_dir, exist_ok=True)

    uploaded = []
    for file in files:
        filepath = os.path.join(target_dir, file.filename)
        with open(filepath, "wb") as f:
            content = await file.read()
            f.write(content)
        uploaded.append(file.filename)

    return {"status": "ok", "uploaded": uploaded, "count": len(uploaded)}


@app.post("/api/assets/tags")
def update_tags(req: TagsRequest):
    """素材にタグを設定する"""
    success = save_asset_tags(BASE_DIR, req.asset_type, req.filename, req.tags)
    if success:
        return {"status": "ok"}
    return {"error": "ファイルが見つかりません"}


# --- 動画生成 ---

RESOLUTIONS = {
    "9:16": (1080, 1920),
    "1:1": (1080, 1080),
    "16:9": (1920, 1080),
}

@app.post("/api/render/scene")
def render_scene(req: RenderSceneRequest):
    """単一シーンの動画を生成する（テスト用）"""
    resolution = RESOLUTIONS.get(req.aspect_ratio, (1080, 1920))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(BASE_DIR, "output", f"scene_{timestamp}.mp4")

    result = generate_scene_video(
        base_dir=BASE_DIR,
        scene=req.scene,
        output_path=output_path,
        resolution=resolution,
    )

    if result["success"]:
        filename = os.path.basename(output_path)
        result["url"] = f"/output/{filename}"

    return result


@app.post("/api/render/full")
def render_full(req: RenderRequest):
    """全シーンを結合してフル動画を書き出す"""
    resolution = RESOLUTIONS.get(req.aspect_ratio, (1080, 1920))
    result = render_full_video(
        base_dir=BASE_DIR,
        scenes=req.scenes,
        bgm=req.bgm,
        bgm_volume=req.bgm_volume,
        aspect_ratio=req.aspect_ratio,
        transition=req.transition,
        resolution=resolution,
        output_format=req.output_format,
    )
    return result


@app.post("/api/render/preview")
def render_preview(req: RenderRequest):
    """低解像度のクイックプレビューを生成する"""
    resolution = RESOLUTIONS.get(req.aspect_ratio, (1080, 1920))
    result = render_full_video(
        base_dir=BASE_DIR,
        scenes=req.scenes,
        bgm=req.bgm,
        bgm_volume=req.bgm_volume,
        aspect_ratio=req.aspect_ratio,
        transition=req.transition,
        resolution=resolution,
        quick_mode=True,
    )
    return result


# --- TTS ---

@app.get("/api/tts/status")
def tts_status():
    """TTSエンジンの接続状態を確認する"""
    engine = get_tts_engine(BASE_DIR)
    available = engine.is_available()
    return {
        "engine": "voicevox",
        "available": available,
        "message": "VOICEVOX接続OK" if available else "VOICEVOXに接続できません",
    }


@app.get("/api/tts/speakers")
def tts_speakers():
    """TTS話者一覧を取得する"""
    engine = get_tts_engine(BASE_DIR)
    if not engine.is_available():
        return {"speakers": [], "error": "VOICEVOXに接続できません"}
    speakers = engine.get_speakers()
    return {"speakers": speakers}


@app.post("/api/tts/synthesize")
def tts_synthesize(req: TTSSynthRequest):
    """1シーンのTTS音声を生成する"""
    engine = get_tts_engine(BASE_DIR, req.engine)
    if not engine.is_available():
        return {"success": False, "error": "VOICEVOXに接続できません"}

    tts_dir = os.path.join(BASE_DIR, "temp", "tts")
    os.makedirs(tts_dir, exist_ok=True)
    output_path = os.path.join(tts_dir, f"scene_{req.scene_id}.wav")

    result = engine.synthesize(
        text=req.text,
        output_path=output_path,
        speaker_id=req.speaker_id,
        speed=req.speed,
    )

    if result["success"]:
        result["tts_path"] = f"/temp/tts/scene_{req.scene_id}.wav"

    return result


@app.post("/api/tts/batch")
def tts_batch(req: TTSBatchRequest):
    """全シーンのTTS音声を一括生成し、尺を再計算する"""
    engine = get_tts_engine(BASE_DIR, req.engine)
    if not engine.is_available():
        return {"success": False, "error": "VOICEVOXに接続できません", "scenes": req.scenes}

    tts_dir = os.path.join(BASE_DIR, "temp", "tts")
    os.makedirs(tts_dir, exist_ok=True)

    padding = 0.3  # 前後余白

    updated_scenes = []
    for scene in req.scenes:
        if not scene.get("tts_enabled", True):
            updated_scenes.append(scene)
            continue

        output_path = os.path.join(tts_dir, f"scene_{scene['id']}.wav")
        result = engine.synthesize(
            text=scene["text"],
            output_path=output_path,
            speaker_id=req.speaker_id,
            speed=req.speed,
        )

        if result["success"]:
            tts_duration = result["duration"]
            scene_duration = tts_duration + (padding * 2)
            scene_duration = round(max(scene_duration, 1.5), 1)
            updated_scenes.append({
                **scene,
                "duration": scene_duration,
                "tts_duration": tts_duration,
                "tts_path": f"/temp/tts/scene_{scene['id']}.wav",
            })
        else:
            updated_scenes.append(scene)

    return {"success": True, "scenes": updated_scenes}


# --- テンプレート ---

@app.get("/api/templates")
def get_templates():
    """テンプレート一覧を取得する"""
    templates = list_templates(BASE_DIR)
    return {"templates": templates}


@app.post("/api/templates")
def create_template(req: TemplateSaveRequest):
    """テンプレートを保存する"""
    result = save_template(BASE_DIR, req.model_dump())
    return {"status": "ok", **result}


@app.get("/api/templates/{filename}")
def get_template(filename: str):
    """テンプレートを読み込む"""
    data = load_template(BASE_DIR, filename)
    if data is None:
        return {"error": "テンプレートが見つかりません"}
    return data


@app.delete("/api/templates/{filename}")
def remove_template(filename: str):
    """テンプレートを削除する"""
    success = delete_template(BASE_DIR, filename)
    if success:
        return {"status": "ok"}
    return {"error": "テンプレートが見つかりません"}


# --- プロジェクト ---

@app.get("/api/projects")
def get_projects():
    """プロジェクト一覧を取得する"""
    projects = list_projects(BASE_DIR)
    return {"projects": projects}


@app.post("/api/projects")
def create_project(req: ProjectSaveRequest):
    """プロジェクトを保存する"""
    result = save_project(BASE_DIR, req.model_dump(), req.filename)
    return {"status": "ok", **result}


@app.get("/api/projects/{filename}")
def get_project(filename: str):
    """プロジェクトを読み込む"""
    data = load_project(BASE_DIR, filename)
    if data is None:
        return {"error": "プロジェクトが見つかりません"}
    return data


@app.post("/api/projects/{filename}/duplicate")
def dup_project(filename: str):
    """プロジェクトを複製する"""
    result = duplicate_project(BASE_DIR, filename)
    if result is None:
        return {"error": "プロジェクトが見つかりません"}
    return {"status": "ok", **result}


@app.delete("/api/projects/{filename}")
def remove_project(filename: str):
    """プロジェクトを削除する"""
    success = delete_project(BASE_DIR, filename)
    if success:
        return {"status": "ok"}
    return {"error": "プロジェクトが見つかりません"}


@app.post("/api/projects/rename")
def ren_project(req: ProjectRenameRequest):
    """プロジェクトの名前を変更する"""
    success = rename_project(BASE_DIR, req.filename, req.new_name)
    if success:
        return {"status": "ok"}
    return {"error": "プロジェクトが見つかりません"}


# --- フロントエンド配信 (Docker用、最後に定義) ---

if os.path.isdir(STATIC_DIR):
    @app.get("/{full_path:path}")
    def serve_spa(full_path: str):
        file_path = os.path.join(STATIC_DIR, full_path)
        if full_path and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(STATIC_DIR, "index.html"))
