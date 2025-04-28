import speech_recognition as sr


def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("話しかけてください…")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio, language="ja-JP")
        print("あなたが言ったこと：", text)
        return text
    except sr.UnknownValueError:
        print("うまく聞き取れませんでした。もう一度話してみてください。")
    except sr.RequestError:
        print("音声認識サービスに接続できませんでした。")


if __name__ == "__main__":
    listen()
