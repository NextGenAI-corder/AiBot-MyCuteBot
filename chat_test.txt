import os
from openai import OpenAI

def get_chatgpt(): #ChatGPTの応答を得る関数
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) #環境変数からAPIきーを取得

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "こんにちは"}] #プロンプトを設定
    )

    print(response.choices[0].message.content)

if __name__ == "__main__":
    get_chatgpt()