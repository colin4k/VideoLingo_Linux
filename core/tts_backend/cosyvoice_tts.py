from pathlib import Path
import os, sys
from openai import OpenAI
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from core.config_utils import load_key

def cosyvoice_tts(text, save_path):
    """
    使用 CosyVoice API 将文本转换为语音
    
    参数:
    text: 要合成的文本
    save_path: 保存音频文件的路径
    """
    cosy_set = load_key("cosy_voice")

    client = OpenAI(
        base_url=cosy_set["api_url"].strip('/'),
        api_key=cosy_set["api_key"]
    )

    speech_file_path = Path(save_path)
    # make dir before save
    speech_file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 准备请求参数
    params = {
        "model": "tts-1",
        "input": text,
        "response_format": "wav",
        "speed": cosy_set["speed"]
    }
    
    # 根据设置决定是使用预设语音还是参考音频
    if cosy_set["use_reference_audio"]:
        # 使用参考文本克隆音色
        #if "reference_text" in cosy_set and cosy_set["reference_text"]:
            #params["reference_text"] = cosy_set["reference_text"]
        #if "reference_audio" in cosy_set and cosy_set["reference_audio"]:
        params["voice"] = cosy_set["reference_audio"]
    else:
        # 使用预设语音
        params["voice"] = cosy_set["voice"]
    
    with client.audio.speech.with_streaming_response.create(**params) as response:
        response.stream_to_file(speech_file_path)
    
    print(f"音频已保存到 {speech_file_path}")

if __name__ == "__main__":
    cosyvoice_tts("这是一个 CosyVoice TTS 测试。", "cosyvoice_tts.wav") 