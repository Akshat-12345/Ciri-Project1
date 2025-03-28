from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import pyttsx3
import waitress

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# OpenAI API Key (Replace with your actual API key)
openai.api_key = "your_openai_api_key_here"

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)

def speak(text):
    """Convert text to speech"""
    engine.say(text)
    engine.runAndWait()

def chat_with_gpt(prompt):
    """Communicate with OpenAI's ChatGPT API"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/chat", methods=["POST"])
def chat():
    """Handle chatbot queries from the website"""
    data = request.json
    user_query = data.get("query", "")

    if not user_query:
        return jsonify({"error": "Query is missing"}), 400
    
    response = chat_with_gpt(user_query)
    return jsonify({"response": response})

@app.route("/speak", methods=["POST"])
def tts():
    """Convert text to speech"""
    data = request.json
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "Text is missing"}), 400

    speak(text)
    return jsonify({"message": "Speaking..."})

if __name__ == "__main__":
    from waitress import serve  # Production-grade server
    serve(app, host="0.0.0.0", port=8080)
