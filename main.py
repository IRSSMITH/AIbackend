from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# A super simple AI logic just to get started
def ai_response(message):
    message = message.lower().strip()
    if "hello" in message:
        return "Hello there! How can I assist you today?"
    elif "how are you" in message:
        return "I'm just a program, but I'm feeling great!"
    elif "what is 2 + 2" in message:
        return "That's easy! 2 + 2 is 4."
    else:
        return "Sorry, I didn't understand that."

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    reply = ai_response(user_message)
    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
