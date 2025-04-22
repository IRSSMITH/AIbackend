from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from transformers import pipeline, set_seed

app = Flask(__name__)
CORS(app)

print("🧠 Loading GPT-2 model...")
generator = pipeline("text-generation", model="gpt2")
set_seed(42)  # Optional: for more consistent outputs
print("✅ Model loaded.")

@app.route("/chat", methods=["POST"])
def chat():
    print("📥 Received /chat request")
    data = request.get_json()
    print("📦 Payload:", data)

    if not data or "message" not in data:
        print("⚠️ Missing 'message' field in request")
        return jsonify({"error": "Missing 'message' field"}), 400

    user_input = data["message"]
    print(f"[User] {user_input}")

    try:
        print("🤖 Generating response...")
        result = generator(
            user_input,
            max_length=100,
            num_return_sequences=1,
            do_sample=True,
            temperature=0.7,
            truncation=True
        )
        print("✅ Generation complete")

        full_text = result[0]["generated_text"]
        response_text = full_text[len(user_input):].strip()

        print(f"[Bot] {response_text}")
        return jsonify({"response": response_text or "Hmm... I had a brain fart 🧠💨"})

    except Exception as e:
        print("🚨 Error during generation:", str(e))
        return jsonify({"response": "Oops! Something went wrong on the AI side."}), 500

@app.route("/", methods=["GET"])
def home():
    return "🤖 NotAI backend is running!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Starting server on port {port}...")
    app.run(host="0.0.0.0", port=port)
