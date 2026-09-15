from flask import Flask, render_template, request
from google import genai
from dotenv import load_dotenv
import os
import random
import time

load_dotenv()

app = Flask(__name__)
MAX_SENTENCE_LENGTH = 1000
api_key = os.getenv("GEMINI_API_KEY")
model_name = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
client = genai.Client(api_key=api_key) if api_key else None


@app.route("/")
def home():
    return render_template("question.html")


@app.route("/check", methods=["POST"])
def check_grammar():
    user_message = request.form.get("sentence", "").strip()
    if not user_message:
        return render_template("question.html", error="Please enter a sentence.", sentence=user_message)
    if len(user_message) > MAX_SENTENCE_LENGTH:
        return render_template("question.html", error=f"Please keep your sentence under {MAX_SENTENCE_LENGTH} characters.", sentence=user_message[:MAX_SENTENCE_LENGTH])
    if client is None:
        return render_template("question.html", error="Add GEMINI_API_KEY to your .env file to enable checking.", sentence=user_message)

    prompt = f"""You are an English grammar correction assistant.
Correct grammar, spelling, capitalization, punctuation, tense, agreement, articles, and prepositions. Preserve the original meaning. Return ONLY the corrected sentence, without explanations, labels, or quotation marks.
User input:
{user_message}
"""
    last_error = ""
    for attempt in range(2):
        try:
            print(f"Trying {model_name} (attempt {attempt + 1}/2)")
            response = client.models.generate_content(model=model_name, contents=prompt)
            if not response.text:
                raise RuntimeError("Gemini returned an empty response.")
            return render_template("answer.html", original=user_message, corrected=response.text.strip())
        except Exception as error:
            last_error = str(error)
            print(f"Gemini error: {last_error}")
            if "401" in last_error or "API_KEY_INVALID" in last_error:
                return render_template("question.html", error="Invalid Gemini API key. Please check your .env file.", sentence=user_message)
            if "403" in last_error or "PERMISSION_DENIED" in last_error:
                return render_template("question.html", error="Gemini API access is denied. Check your Google AI Studio project.", sentence=user_message)
            if "404" in last_error or "NOT_FOUND" in last_error:
                return render_template("question.html", error=f"The Gemini model '{model_name}' is unavailable. Update GEMINI_MODEL in .env.", sentence=user_message)
            if ("503" in last_error or "UNAVAILABLE" in last_error or "high demand" in last_error.lower()) and attempt == 0:
                time.sleep(0.8 + random.uniform(0, 0.4))
                continue
            break
    return render_template("question.html", error="Gemini is temporarily unavailable. Please try again in a few seconds.", sentence=user_message)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
