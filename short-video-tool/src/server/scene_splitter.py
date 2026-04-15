"""
テキストをシーン（カード）に自動分割するロジック。
句読点・改行を基準に分割する。
"""
import re


def split_text_to_scenes(text: str) -> list[dict]:
    """
    テキストを句読点・改行で分割し、シーンのリストを返す。

    分割ルール:
    - 改行（\\n）で分割
    - 句点（。）で分割
    - 感嘆符（！）・疑問符（？）で分割
    - 空行は無視
    """
    if not text.strip():
        return []

    # まず改行で分割
    lines = text.split('\n')

    raw_segments = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # 句点・感嘆符・疑問符で分割（区切り文字を保持）
        parts = re.split(r'(。|！|！|？|\?|!)', line)
        # 区切り文字を前の部分に結合
        merged = []
        i = 0
        while i < len(parts):
            segment = parts[i]
            # 次の要素が区切り文字なら結合
            if i + 1 < len(parts) and re.match(r'^[。！！？\?!]$', parts[i + 1]):
                segment += parts[i + 1]
                i += 2
            else:
                i += 1
            segment = segment.strip()
            if segment:
                merged.append(segment)
        raw_segments.extend(merged)

    # シーンオブジェクトに変換
    scenes = []
    for idx, text_content in enumerate(raw_segments):
        scenes.append({
            "id": idx,
            "text": text_content,
            "duration": None,       # Step 3 で自動算出
            "background": None,     # Step 4 で設定
            "tts_enabled": True,
            "telop_style": "standard",
            # --- 拡張フィールド（後方互換のため全て既定値） ---
            "text_anim": "none",           # A-1: テキストアニメ
            "emphasis_ranges": [],         # A-2: 強調範囲
            "se_path": None,               # A-3: 効果音
            "telop_layers": [],            # B-6: 複数テロップレイヤー
            "color_adjust": None,          # C-9: 色調補正
            "emphasis_effect": "none",     # C-10: ズーム/シェイク
        })

    return scenes


def ensure_scene_defaults(scene: dict) -> dict:
    """旧プロジェクトのシーンに新フィールドを補完する（後方互換用）"""
    defaults = {
        "text_anim": "none",
        "emphasis_ranges": [],
        "se_path": None,
        "telop_layers": [],
        "color_adjust": None,
        "emphasis_effect": "none",
    }
    for k, v in defaults.items():
        if k not in scene:
            scene[k] = v
    return scene
