from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

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
    app.run(host="0.0.0.0", port=8080)
