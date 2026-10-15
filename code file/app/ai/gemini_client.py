from google import genai

from app.config import (
    GEMINI_API_KEY
)


def get_gemini_client():

    if not GEMINI_API_KEY:

        raise RuntimeError(
            "GEMINI_API_KEY is missing. "
            "Please add your Gemini API key "
            "inside the .env file."
        )


    client = genai.Client(
        api_key=GEMINI_API_KEY
    )


    return client