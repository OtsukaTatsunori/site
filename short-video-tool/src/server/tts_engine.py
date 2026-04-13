"""
TTS（テキスト読み上げ）エンジン。
VOICEVOX（ローカル）をデフォルト。Google Cloud TTS / OpenAI TTSもオプション対応。
"""
import httpx
import os
import json
import struct
import wave


def get_audio_duration(filepath: str) -> float:
    """WAVファイルの長さ（秒）を取得する"""
    try:
        with wave.open(filepath, 'rb') as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            return frames / float(rate)
    except Exception:
        pass

    # WAV以外の場合はffprobeで取得
    import subprocess
    cmd = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", filepath]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        data = json.loads(result.stdout)
        return float(data.get("format", {}).get("duration", 0))
    return 0


def load_config(base_dir: str) -> dict:
    """config.jsonを読み込む"""
    config_path = os.path.join(base_dir, "config.json")
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


class VoicevoxTTS:
    """VOICEVOX TTSエンジン"""

    def __init__(self, host: str = "http://localhost:50021"):
        self.host = host

    def is_available(self) -> bool:
        """VOICEVOXが起動しているか確認"""
        try:
            r = httpx.get(f"{self.host}/version", timeout=2.0)
            return r.status_code == 200
        except Exception:
            return False

    def get_speakers(self) -> list[dict]:
        """話者一覧を取得"""
        try:
            r = httpx.get(f"{self.host}/speakers", timeout=5.0)
            if r.status_code == 200:
                speakers = r.json()
                result = []
                for speaker in speakers:
                    for style in speaker.get("styles", []):
                        result.append({
                            "id": style["id"],
                            "name": f"{speaker['name']} ({style['name']})",
                        })
                return result
        except Exception:
            pass
        return []

    def synthesize(
        self,
        text: str,
        output_path: str,
        speaker_id: int = 1,
        speed: float = 1.0,
    ) -> dict:
        """テキストを音声に変換してWAVファイルとして保存"""
        try:
            # 1. 音声合成用のクエリを作成
            query_res = httpx.post(
                f"{self.host}/audio_query",
                params={"text": text, "speaker": speaker_id},
                timeout=30.0,
            )
            if query_res.status_code != 200:
                return {"success": False, "error": f"audio_query失敗: {query_res.status_code}"}

            query = query_res.json()
            query["speedScale"] = speed

            # 2. 音声合成
            synth_res = httpx.post(
                f"{self.host}/synthesis",
                params={"speaker": speaker_id},
                json=query,
                timeout=60.0,
            )
            if synth_res.status_code != 200:
                return {"success": False, "error": f"synthesis失敗: {synth_res.status_code}"}

            # 3. WAVファイルとして保存
            with open(output_path, "wb") as f:
                f.write(synth_res.content)

            duration = get_audio_duration(output_path)
            return {
                "success": True,
                "output": output_path,
                "duration": duration,
            }

        except httpx.TimeoutException:
            return {"success": False, "error": "VOICEVOXへの接続がタイムアウトしました"}
        except httpx.ConnectError:
            return {"success": False, "error": "VOICEVOXに接続できません。VOICEVOXエンジンが起動しているか確認してください。"}
        except Exception as e:
            return {"success": False, "error": str(e)}


def get_tts_engine(base_dir: str, engine_name: str = "voicevox"):
    """TTSエンジンのインスタンスを取得"""
    config = load_config(base_dir)
    tts_config = config.get("tts", {})

    if engine_name == "voicevox":
        host = tts_config.get("voicevox", {}).get("host", "http://localhost:50021")
        return VoicevoxTTS(host=host)

    # 将来的にGoogle Cloud TTS / OpenAI TTSもここに追加
    return VoicevoxTTS()
