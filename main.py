from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# ✅ すべてのHTTPメソッドに対応 & GitHub Pagesからのリクエスト許可
CORS(app, origins=["https://akira-growtech.github.io"], supports_credentials=True)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():
    if request.method == "OPTIONS":
        # CORSプリフライトリクエストへの応答
        return jsonify({"message": "CORSプリフライトOK"}), 200

    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"reply": "メッセージが空です"}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "あなたは明良さん専用のAIアシスタントです。"},
                {"role": "user", "content": user_message}
            ]
        )
        reply_text = response.choices[0].message.content.strip()
        return jsonify({"reply": reply_text})
    except Exception as e:
        print("❌ エラー発生:", str(e))
        return jsonify({"reply": f"内部エラー: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

