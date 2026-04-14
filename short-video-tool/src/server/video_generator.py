"""
FFmpegを使った動画生成ロジック。
まずは単一シーン（テロップ + 背景画像）の動画を生成する。
"""
import subprocess
import os
import json
import glob as glob_module

# テロッププリセット
TELOP_PRESETS = {
    # --- ベーシック系 ---
    "standard": {
        "label": "標準（白+黒縁）",
        "fontsize": 48, "fontcolor": "white",
        "borderw": 3, "bordercolor": "black",
        "position": "bottom",
    },
    "standard_top": {
        "label": "標準（上部）",
        "fontsize": 48, "fontcolor": "white",
        "borderw": 3, "bordercolor": "black",
        "position": "top",
    },
    # --- インパクト系 ---
    "impact": {
        "label": "インパクト（黄色）",
        "fontsize": 64, "fontcolor": "yellow",
        "borderw": 4, "bordercolor": "black",
        "position": "center",
    },
    "impact_red": {
        "label": "インパクト（赤）",
        "fontsize": 64, "fontcolor": "#FF3333",
        "borderw": 4, "bordercolor": "white",
        "position": "center",
    },
    # --- 字幕系 ---
    "subtitle": {
        "label": "字幕（黒帯）",
        "fontsize": 36, "fontcolor": "white",
        "borderw": 2, "bordercolor": "black",
        "position": "very_bottom",
        "box": True, "boxcolor": "black@0.6", "boxborderw": 10,
        "box_round": 0,
    },
    "subtitle_glass": {
        "label": "字幕（すりガラス）",
        "fontsize": 36, "fontcolor": "white",
        "borderw": 1, "bordercolor": "#333333",
        "position": "very_bottom",
        "box": True, "boxcolor": "#1a1a2e@0.7", "boxborderw": 14,
        "box_round": 0,
    },
    # --- ポップ系 ---
    "pop": {
        "label": "ポップ（ピンク）",
        "fontsize": 56, "fontcolor": "#FF6B9D",
        "borderw": 3, "bordercolor": "white",
        "position": "center",
    },
    "pop_neon": {
        "label": "ネオン（水色）",
        "fontsize": 52, "fontcolor": "#00FFFF",
        "borderw": 3, "bordercolor": "#0066FF",
        "position": "center",
    },
}


def get_video_duration(filepath: str) -> float:
    """FFprobeで動画の長さを取得する"""
    cmd = [
        "ffprobe", "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        filepath,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        data = json.loads(result.stdout)
        return float(data.get("format", {}).get("duration", 0))
    return 0


def find_font(base_dir: str) -> str:
    """assets/fonts/ からフォントファイルを探す"""
    font_dir = os.path.join(base_dir, "assets", "fonts")
    for ext in ("*.ttf", "*.otf"):
        fonts = glob_module.glob(os.path.join(font_dir, ext))
        if fonts:
            return fonts[0]
    return ""


def get_telop_position(position: str, fontsize: int, custom_x: int | None = None, custom_y: int | None = None) -> str:
    """テロップ配置位置を取得。セーフエリア(10%)を考慮。カスタム座標対応。"""
    if custom_x is not None and custom_y is not None:
        return f"x={custom_x}:y={custom_y}"
    if position == "center":
        return "x=(w-text_w)/2:y=(h-text_h)/2"
    elif position == "top":
        return "x=(w-text_w)/2:y=h*0.10"
    elif position == "very_bottom":
        return "x=(w-text_w)/2:y=h-text_h-h*0.05"
    else:  # bottom (default)
        return "x=(w-text_w)/2:y=h-text_h-h*0.12"


def build_drawtext_filter(
    text: str,
    preset_name: str,
    font_path: str,
    duration: float,
    fade_in: bool = True,
    fade_out: bool = True,
    custom_x: int | None = None,
    custom_y: int | None = None,
    custom_box: dict | None = None,
) -> str:
    """drawtextフィルタ文字列を構築する"""
    preset = TELOP_PRESETS.get(preset_name, TELOP_PRESETS["standard"])

    # テキスト内の特殊文字をエスケープ
    escaped_text = (
        text.replace("\\", "\\\\")
        .replace("'", "\\'")
        .replace(":", "\\:")
        .replace("[", "\\[")
        .replace("]", "\\]")
    )

    pos = get_telop_position(preset["position"], preset["fontsize"], custom_x, custom_y)

    parts = [
        f"drawtext=text='{escaped_text}'",
        f"fontsize={preset['fontsize']}",
        f"fontcolor={preset['fontcolor']}",
        f"borderw={preset['borderw']}",
        f"bordercolor={preset['bordercolor']}",
        pos,
    ]

    if font_path:
        escaped_font = font_path.replace("\\", "/").replace(":", "\\:")
        parts.append(f"fontfile='{escaped_font}'")

    # 背景帯: カスタム設定 > プリセット設定
    use_box = custom_box.get("enabled") if custom_box else preset.get("box")
    if use_box:
        box_color = custom_box.get("color", "black") if custom_box else preset.get("boxcolor", "black")
        box_opacity = custom_box.get("opacity", 0.6) if custom_box else 0.6
        box_padding = custom_box.get("padding", 10) if custom_box else preset.get("boxborderw", 10)
        # boxcolorに@opacityを含むか確認
        if "@" not in str(box_color):
            box_color = f"{box_color}@{box_opacity}"
        parts.append("box=1")
        parts.append(f"boxcolor={box_color}")
        parts.append(f"boxborderw={box_padding}")

    # フェードイン/フェードアウト
    alpha_parts = []
    if fade_in:
        alpha_parts.append(f"if(lt(t\\,0.3)\\,t/0.3\\,1)")
    if fade_out:
        fade_start = max(0, duration - 0.3)
        alpha_parts.append(
            f"if(gt(t\\,{fade_start:.1f})\\,(({duration:.1f}-t)/0.3)\\,1)"
        )

    if alpha_parts:
        if len(alpha_parts) == 2:
            alpha_expr = f"min({alpha_parts[0]}\\,{alpha_parts[1]})"
        else:
            alpha_expr = alpha_parts[0]
        parts.append(f"alpha='{alpha_expr}'")

    return ":".join(parts)


def generate_scene_video(
    base_dir: str,
    scene: dict,
    output_path: str,
    resolution: tuple[int, int] = (1080, 1920),
) -> dict:
    """
    単一シーンの動画を生成する。

    scene: {
        text: str,
        duration: float,
        background: str (パス, 例: "/assets/backgrounds/sample.jpg"),
        telop_style: str (プリセット名),
    }
    """
    duration = scene.get("duration", 3.0)
    text = scene.get("text", "")
    ken_burns = scene.get("ken_burns", False)
    bg_path = scene.get("background")
    telop_style = scene.get("telop_style", "standard")
    overlay_image = scene.get("overlay_image")  # 画像オーバーレイ
    telop_x = scene.get("telop_x")  # カスタムテロップ位置
    telop_y = scene.get("telop_y")
    custom_box = scene.get("custom_box")  # カスタム背景帯
    width, height = resolution

    font_path = find_font(base_dir)

    # 背景の入力ソース
    if bg_path and not bg_path.startswith("/"):
        bg_full_path = os.path.join(base_dir, bg_path)
    elif bg_path:
        bg_full_path = os.path.join(base_dir, bg_path.lstrip("/"))
    else:
        bg_full_path = None

    # 背景が画像かどうか判定
    is_image_bg = bg_full_path and bg_full_path.lower().endswith(
        (".jpg", ".jpeg", ".png", ".webp")
    )
    is_video_bg = bg_full_path and bg_full_path.lower().endswith(
        (".mp4", ".mov", ".avi", ".webm")
    )

    # FFmpegコマンド構築
    cmd = ["ffmpeg", "-y"]

    if is_image_bg and os.path.exists(bg_full_path):
        # 画像背景: ループして動画化
        cmd += ["-loop", "1", "-i", bg_full_path, "-t", str(duration)]
    elif is_video_bg and os.path.exists(bg_full_path):
        # 動画背景: 尺に応じてトリミングまたはループ
        bg_duration = get_video_duration(bg_full_path)
        if bg_duration > 0 and bg_duration < duration:
            # 動画が短い → ループで伸ばす
            loop_count = int(duration / bg_duration) + 1
            cmd += [
                "-stream_loop", str(loop_count),
                "-i", bg_full_path,
            ]
        else:
            # 動画が長い → 先頭からトリミング（-t で制限）
            cmd += ["-i", bg_full_path]
    else:
        # 背景なし: 黒背景を生成
        cmd += [
            "-f", "lavfi",
            "-i", f"color=c=black:s={width}x{height}:d={duration}:r=30",
        ]

    # フィルタ構築
    filters = []

    if ken_burns and is_image_bg:
        # Ken Burns効果: zoompanでゆっくりズーム+パン
        total_frames = int(duration * 30)
        # 1.0x → 1.15x にゆっくりズームイン
        zoom_expr = f"1+0.15*on/{total_frames}"
        # 画像を大きめにスケール → zoompan で切り出す
        filters.append(f"scale=-1:{height * 2}")
        filters.append(
            f"zoompan=z='{zoom_expr}':d={total_frames}:s={width}x{height}:fps=30"
        )
        filters.append("setsar=1")
    else:
        # スケーリング（解像度に合わせる）
        filters.append(f"scale={width}:{height}:force_original_aspect_ratio=decrease")
        filters.append(f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:black")
        filters.append(f"setsar=1")

        # 画像背景の場合、フレームレートを設定
        if is_image_bg:
            filters.append("fps=30")

    # テロップ追加
    if text:
        drawtext = build_drawtext_filter(
            text, telop_style, font_path, duration,
            custom_x=telop_x, custom_y=telop_y,
            custom_box=custom_box,
        )
        filters.append(drawtext)

    # 画像オーバーレイ対応
    overlay_full = None
    if overlay_image:
        ov_path = overlay_image if not overlay_image.startswith("/") else overlay_image.lstrip("/")
        overlay_full = os.path.join(base_dir, ov_path)
        if not os.path.exists(overlay_full):
            overlay_full = None

    if overlay_full:
        # filter_complex で背景 + オーバーレイ + テロップ
        cmd += ["-i", overlay_full]
        bg_filter = ",".join(filters[:-1]) if text else ",".join(filters)
        telop_filter = filters[-1] if text else ""
        fc = f"[0:v]{bg_filter}[bg];[1:v]scale={width}:{height}:force_original_aspect_ratio=decrease,format=rgba[ov];[bg][ov]overlay=(W-w)/2:(H-h)/2[merged]"
        if telop_filter:
            fc += f";[merged]{telop_filter}[outv]"
            map_label = "[outv]"
        else:
            map_label = "[merged]"
        cmd += [
            "-filter_complex", fc,
            "-map", map_label,
            "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
            "-t", str(duration), "-r", "30",
            output_path,
        ]
    else:
        filter_str = ",".join(filters)
        cmd += [
            "-vf", filter_str,
            "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
            "-t", str(duration), "-r", "30",
            output_path,
        ]

    # 実行
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=base_dir,
    )

    if result.returncode != 0:
        return {
            "success": False,
            "error": result.stderr,
            "command": " ".join(cmd),
        }

    return {
        "success": True,
        "output": output_path,
        "duration": duration,
    }


def concat_scenes_simple(scene_files: list[str], output_path: str, base_dir: str) -> dict:
    """シーン動画をconcat（カット結合）する"""
    # concat用のリストファイルを作成
    list_path = os.path.join(base_dir, "temp", "concat_list.txt")
    with open(list_path, "w") as f:
        for filepath in scene_files:
            f.write(f"file '{filepath}'\n")

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", list_path,
        "-c", "copy",
        output_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=base_dir)
    if result.returncode != 0:
        return {"success": False, "error": result.stderr}
    return {"success": True, "output": output_path}


def concat_with_xfade(
    scene_files: list[str],
    scene_durations: list[float],
    output_path: str,
    transition: str,
    base_dir: str,
) -> dict:
    """xfadeフィルタでトランジション付きの結合"""
    if len(scene_files) < 2:
        return concat_scenes_simple(scene_files, output_path, base_dir)

    xfade_duration = 0.5  # トランジション時間

    # xfadeのトランジション名マッピング
    xfade_map = {
        "crossfade": "fade",
        "slide": "slideleft",
        "wipe": "wiperight",
    }
    xfade_type = xfade_map.get(transition, "fade")

    cmd = ["ffmpeg", "-y"]
    for f in scene_files:
        cmd += ["-i", f]

    # filter_complex構築
    n = len(scene_files)
    filter_parts = []
    current_offset = 0

    if n == 2:
        offset = max(0, scene_durations[0] - xfade_duration)
        filter_parts.append(
            f"[0:v][1:v]xfade=transition={xfade_type}:duration={xfade_duration}:offset={offset:.2f}[outv]"
        )
        out_label = "[outv]"
    else:
        # 3つ以上のシーンをチェーン
        prev_label = "[0:v]"
        accumulated = 0
        for i in range(1, n):
            offset = accumulated + scene_durations[i - 1] - xfade_duration
            if i == 1:
                in1 = "[0:v]"
            else:
                in1 = f"[v{i-1}]"

            if i == n - 1:
                out = "[outv]"
            else:
                out = f"[v{i}]"

            filter_parts.append(
                f"{in1}[{i}:v]xfade=transition={xfade_type}:duration={xfade_duration}:offset={offset:.2f}{out}"
            )
            accumulated = offset
        out_label = "[outv]"

    filter_str = ";".join(filter_parts)
    cmd += [
        "-filter_complex", filter_str,
        "-map", out_label,
        "-c:v", "libx264",
        "-preset", "fast",
        "-pix_fmt", "yuv420p",
        output_path,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, cwd=base_dir)
    if result.returncode != 0:
        return {"success": False, "error": result.stderr}
    return {"success": True, "output": output_path}


def add_bgm(
    video_path: str,
    bgm_path: str,
    output_path: str,
    volume: int,
    base_dir: str,
    tts_audio_paths: list[str] | None = None,
) -> dict:
    """動画にBGMを追加する。最後2秒フェードアウト。"""
    bgm_full = os.path.join(base_dir, bgm_path.lstrip("/"))
    if not os.path.exists(bgm_full):
        return {"success": False, "error": f"BGMファイルが見つかりません: {bgm_full}"}

    # 動画の長さを取得
    video_duration = get_video_duration(video_path)
    fade_start = max(0, video_duration - 2.0)
    vol = volume / 100.0

    cmd = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-i", bgm_full,
    ]

    # TTS音声がある場合
    input_idx = 2
    tts_inputs = []
    if tts_audio_paths:
        for tts_path in tts_audio_paths:
            full_tts = os.path.join(base_dir, tts_path.lstrip("/"))
            if os.path.exists(full_tts):
                cmd += ["-i", full_tts]
                tts_inputs.append(input_idx)
                input_idx += 1

    # BGMフィルタ: 音量調整 + フェードアウト + 動画に合わせてトリミング
    bgm_filter = f"[1:a]volume={vol:.2f},afade=t=out:st={fade_start:.2f}:d=2.0[bgm]"

    if tts_inputs:
        # TTS音声をミックス
        tts_mix = ""
        for idx in tts_inputs:
            tts_mix += f"[{idx}:a]"
        filter_complex = f"{bgm_filter};{tts_mix}amix=inputs={len(tts_inputs)}[tts];[bgm][tts]amix=inputs=2:duration=first[outa]"
        cmd += [
            "-filter_complex", filter_complex,
            "-map", "0:v",
            "-map", "[outa]",
        ]
    else:
        cmd += [
            "-filter_complex", bgm_filter,
            "-map", "0:v",
            "-map", "[bgm]",
        ]

    cmd += [
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        output_path,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True, cwd=base_dir)
    if result.returncode != 0:
        return {"success": False, "error": result.stderr}
    return {"success": True, "output": output_path}


def render_full_video(
    base_dir: str,
    scenes: list[dict],
    bgm: dict | None,
    bgm_volume: int,
    aspect_ratio: str,
    transition: str,
    resolution: tuple[int, int],
) -> dict:
    """全シーンを結合して最終動画を生成する"""
    from datetime import datetime

    temp_dir = os.path.join(base_dir, "temp")
    os.makedirs(temp_dir, exist_ok=True)

    # 1. 各シーンの個別動画を生成
    scene_files = []
    scene_durations = []
    for i, scene in enumerate(scenes):
        scene_path = os.path.join(temp_dir, f"scene_{i:03d}.mp4")
        result = generate_scene_video(
            base_dir=base_dir,
            scene=scene,
            output_path=scene_path,
            resolution=resolution,
        )
        if not result["success"]:
            return {"success": False, "error": f"シーン{i+1}の生成に失敗: {result.get('error', '')}"}
        scene_files.append(scene_path)
        scene_durations.append(scene.get("duration", 3.0))

    # 2. シーンを結合
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if transition == "cut" or len(scene_files) == 1:
        concat_path = os.path.join(temp_dir, f"concat_{timestamp}.mp4")
        result = concat_scenes_simple(scene_files, concat_path, base_dir)
    else:
        concat_path = os.path.join(temp_dir, f"concat_{timestamp}.mp4")
        result = concat_with_xfade(
            scene_files, scene_durations, concat_path, transition, base_dir
        )

    if not result["success"]:
        return {"success": False, "error": f"シーン結合に失敗: {result.get('error', '')}"}

    # 3. BGMを追加（あれば）
    if bgm and bgm.get("path"):
        final_path = os.path.join(base_dir, "output", f"{timestamp}.mp4")
        result = add_bgm(concat_path, bgm["path"], final_path, bgm_volume, base_dir)
        if not result["success"]:
            return {"success": False, "error": f"BGM追加に失敗: {result.get('error', '')}"}
    else:
        final_path = os.path.join(base_dir, "output", f"{timestamp}.mp4")
        # BGMなし: そのまま出力フォルダにコピー
        import shutil
        shutil.copy2(concat_path, final_path)

    filename = os.path.basename(final_path)
    total_duration = sum(scene_durations)

    return {
        "success": True,
        "output": final_path,
        "url": f"/output/{filename}",
        "duration": total_duration,
        "filename": filename,
    }
