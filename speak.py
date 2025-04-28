import requests
import json
import winsound

def speak(text, speaker=1):  # speaker=1 → ずんだもん
    # VOICEVOXエンジンが起動している必要があります！

    # クエリ作成
    query = requests.post(
        "http://127.0.0.1:50021/audio_query",
        params={"text": text, "speaker": speaker}
    ).json()

    # 音声合成
    synthesis = requests.post(
        "http://127.0.0.1:50021/synthesis",
        headers={"Content-Type": "application/json"},
        params={"speaker": speaker},
        data=json.dumps(query)
    )

    # 音声ファイルとして保存
    with open("voicevox_output.wav", "wb") as f:
        f.write(synthesis.content)

    # GUIなしで再生
    winsound.PlaySound("voicevox_output.wav", winsound.SND_FILENAME)

if __name__ == "__main__":
    speak("こんにちは！今日はどんなお手伝いをしましょうか？")