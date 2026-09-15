# AI Grammar Checker

A fast, interactive Flask grammar checker powered by Google Gemini. It corrects grammar, spelling, punctuation, capitalization, and tense while preserving the original meaning.

## Features

- Animated loading workspace while AI is processing
- Grammar, spelling, punctuation, and clarity correction
- Live character counter with a 1,000-character limit
- Copy correction and read-aloud actions
- Responsive design for desktop and mobile
- Configurable Gemini model

## Run locally

1. Create a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

3. Create your environment file:

   ```powershell
   Copy-Item .env.example .env
   ```

4. Add your Gemini API key to `.env`.

5. Start the app:

   ```powershell
   python app.py
   ```

6. Open http://127.0.0.1:5000

## GitHub safety

Never commit `.env` or expose your API key. The repository ignores `.env` by default. If an API key has already been shared or committed, revoke it in Google AI Studio and create a new one before publishing.
