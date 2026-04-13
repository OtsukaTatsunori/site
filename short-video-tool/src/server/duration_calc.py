"""
シーンの尺（秒）を自動算出するロジック。
"""

# デフォルト設定
CHARS_PER_SECOND = 4     # 1秒あたりの文字数
MIN_DURATION = 1.5       # 最低尺（秒）
PADDING = 0.3            # 前後余白（秒）


def calc_duration_from_text(text: str, speed: float = 1.0) -> float:
    """
    テキストの文字数からシーンの尺を算出する（TTS OFF時）。

    ルール:
    - 尺 = 文字数 ÷ (1秒あたり4文字) ÷ 速度倍率 + 前後余白(0.3秒×2)
    - 最低 1.5秒
    """
    char_count = len(text)
    base_duration = char_count / CHARS_PER_SECOND / speed
    duration = base_duration + (PADDING * 2)
    return round(max(duration, MIN_DURATION), 1)


def calc_scenes_duration(scenes: list[dict], global_speed: float = 1.0) -> list[dict]:
    """
    各シーンに尺を自動設定する。
    既に手動で尺が設定されている場合（manual_duration）はそちらを優先。
    """
    for scene in scenes:
        if scene.get("manual_duration") is not None:
            scene["duration"] = scene["manual_duration"]
        else:
            scene["duration"] = calc_duration_from_text(
                scene["text"],
                speed=global_speed
            )
    return scenes
