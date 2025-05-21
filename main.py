from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import openai
from dotenv import load_dotenv

load_dotenv()  # .envファイルの読み込み

app = Flask(__name__)
CORS(app)  # CORS対応

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"reply": "メッセージが空です"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "あなたは明良さん専用のAIアシスタントです。"},
                {"role": "user", "content": user_message}
            ]
        )
        reply_text = response.choices[0].message.content.strip()
        return jsonify({"reply": reply_text})

    except Exception as e:
        # ✅ エラー内容をログに出す
        print("❌ エラー発生:", str(e))
        return jsonify({"reply": f"内部エラー: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
