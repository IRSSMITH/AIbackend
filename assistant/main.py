from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from transformers import pipeline

app = Flask(__name__)

# Enable CORS globally (OR for a specific route below)
CORS(app)

generator = pipeline("text-generation", model="gpt2")

def ai_response(message):
    response = generator(message, max_length=50, num_return_sequences=1)
    return response[0]['generated_text']

@app.route("/chat", methods=["POST", "OPTIONS"])
@cross_origin(origin="https://notai.onrender.com")  # Allow this origin for this route
def chat():
    if request.method == "OPTIONS":
        # Handle preflight request
        return jsonify({"message": "CORS preflight success"}), 200

    data = request.get_json()
    user_message = data.get("message", "")
    reply = ai_response(user_message)
    return jsonify({"response": reply})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
