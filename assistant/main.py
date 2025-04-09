from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline

app = Flask(__name__)

# Add this line to allow all origins (just for testing!)
CORS(app)

# OR for stricter control (recommended once it's working)
# CORS(app, resources={r"/chat": {"origins": "https://notai.onrender.com"}})

# 🔥 Add this to force headers
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'https://notai.onrender.com'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    return response

generator = pipeline("text-generation", model="gpt2")

def ai_response(message):
    response = generator(message, max_length=50, num_return_sequences=1)
    return response[0]['generated_text']

@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():
    if request.method == "OPTIONS":
        return '', 204  # Preflight check

    data = request.get_json()
    user_message = data.get("message", "")
    reply = ai_response(user_message)
    return jsonify({"response": reply})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
