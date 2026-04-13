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
        })

    return scenes
