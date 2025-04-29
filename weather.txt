import os
import openai
import requests
from openai import OpenAI

# ==== APIキー ====
WEATHER_API = os.getenv("WEATHER_API")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

city="流山市"
# ==== OpenAIクライアント初期化 ====
client = OpenAI(api_key=OPENAI_API_KEY)

# ==== 天気取得 ====
def get_weather(city):
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": WEATHER_API, "lang": "ja", "units": "metric"}
    res = requests.get(url, params=params)
    if res.status_code == 200:
        data = res.json()
        desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        return f"{city}の天気は「{desc}」、気温は{temp}℃です。"
    return "天気情報の取得に失敗しました。"

# ==== プロンプト生成 ====
def build_prompt(weather_info):
    prompt = (
        "あなたは社長にとって可愛い秘書です。以下の天気情報をもとに、出発前のアドバイスを丁寧に作成してください。\n"
        #"\n"
        f"最初に{city}近辺のロケーションを説明して\n"
        "【条件】\n"
        "- 雨なら、傘を持ってってね！」と促す\n"
        "- 曇りなら、服装の注意を軽く入れる\n"
        "- 晴れなら、気持ちの良い一日をと激励する\n"
        "- 寒いなら、厚着の方が良いとアドバイス\n"
        "- 暑くなるなら、水分をまめに補給してねとアドバイス\n"
        "- あなたもお酒が好きです。仕事の後に飲みに連れていってとせがんで下さい\n"
        "- 表現は40文字以内、やさしく可愛く丁寧に\n"
    )
    return prompt

# ==== ChatGPT応答（v1.1+対応） ====
def get_advice():
    weather_info = get_weather(city)
    prompt = build_prompt(weather_info)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        #model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()

# ==== 実行 ====
if __name__ == "__main__":
    print("🔔 社長 ? ちょっと待って！\n")
    print(get_advice())
