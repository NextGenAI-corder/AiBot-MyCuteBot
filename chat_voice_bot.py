import os
import json
import requests # 音声合成ライブラリ
import winsound # 音声再生ライブラリ
import speech_recognition as sr # 音声認識ライブラリ
from openai import OpenAI

# 環境変数からAPIキーを取得してOpenAIクライアントを作成
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# 1.音声認識：音声を録音してテキストに変換
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        # 無音を検出する感度を調整
        recognizer.pause_threshold = 1.0 # 無音が1.0秒続いたら終了とみなす（デフォは0.8）

        print("話かけて下さい！")
        audio = recognizer.listen(source,phrase_time_limit=7) # 録音最大秒数を４秒に設定

    try:
        text = recognizer.recognize_google(audio, language="ja-JP")
        return text
    except sr.UnknownValueError:
        return "すみません、うまく聞き取れませんでした。"
    except sr.RequestError:
        return "音声認識サービスに接続できませんでした。"


# ２．ChatGPT連携：ChatGPTに質問を送ってテキストで返事をもらう
def ask_chatgpt(text):
    # AIの回答の言葉数に制限を設ける
    prompt = text + "。20文字以内で答えてください。"

    response = client.chat.completions.create(
        # model="gpt-3.5-turbo",
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
    )
    # ChatGPTの返答テキストを取り出して返す
    return response.choices[0].message.content


# ３．音声合成：VOICEVOXで合成音声を生成して再生
def speak(text, speaker=1):  # speaker=1 = ずんだもん
    try:
        # 発話クエリをVOICEVOXに送って取得
        query = requests.post(
            "http://127.0.0.1:50021/audio_query",
            params={"text": text, "speaker": speaker},
        ).json()

        # クエリから合成音声を生成
        synthesis = requests.post(
            "http://127.0.0.1:50021/synthesis",
            headers={"Content-Type": "application/json"},
            params={"speaker": speaker},
            data=json.dumps(query),
        )

        # 音声ファイルに保存
        with open("voicevox_output.wav", "wb") as f:
            f.write(synthesis.content)

        # 音声ファイルをバックグラウンド再生（GUIなし）
        winsound.PlaySound("voicevox_output.wav", winsound.SND_FILENAME)

    except Exception as e:
        print("VOICEVOXでエラーが発生しました：", e)


# ４．メイン：全体の流れを制御（聞く→考える→しゃべる）
def talk_with_bot():
    speak("何か話して？")
    while True:
        question = listen() #１を実行
        print("あなた：", question)

        # 「終了」と言ったら会話終了
        if "終了" in question or "おわり" in question:
            print("会話を終了します。")
            speak("また話そうね！")
            break

        answer = ask_chatgpt(question) #２を実行
        print("Bot：", answer)
        speak(answer) # ３を実行


# メイン処理の起動
if __name__ == "__main__":
    talk_with_bot() #４を実行
