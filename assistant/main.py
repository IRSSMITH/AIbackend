from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from transformers import pipeline

# Set up Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the model (keep it light for free hosting)
generator = pipeline("text-generation", model="gpt2")

# Chat endpoint
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"error": "Missing 'message' field"}), 400

    user_input = data["message"]

    # Generate response
    result = generator(
        user_input,
        max_length=100,
        num_return_sequences=1,
        do_sample=True,
        temperature=0.7,
    )

    response_text = result[0]["generated_text"]
    
    return jsonify({"response": response_text})

# Optional: root route just to show it's alive
@app.route("/", methods=["GET"])
def home():
    return "🤖 NotAI backend is running!"

# Start the server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render uses this PORT env var
    app.run(host="0.0.0.0", port=port)
