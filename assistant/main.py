from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from transformers import pipeline

app = Flask(__name__)

# Enable CORS for all domains
CORS(app)

# If you want to restrict it to your specific frontend domain:
# CORS(app, resources={r"/chat": {"origins": "https://notai.onrender.com"}})

# Initialize Hugging Face model pipeline for text generation
generator = pipeline("text-generation", model="gpt2")

def ai_response(message):
    response = generator(message, max_length=50, num_return_sequences=1)
    return response[0]['generated_text']

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    reply = ai_response(user_message)
    return jsonify({"response": reply})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
