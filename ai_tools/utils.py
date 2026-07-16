from decouple import config
from google import genai

_client = None

def get_client():
    global _client
    if _client is None:
        api_key = config("GEMINI_API_KEY")
        _client = genai.Client(api_key=api_key)
    return _client


def ask_claude(system_prompt, user_message, max_tokens=1000):
    """
    Sends a prompt to Gemini and returns the plain text response.
    Kept the name ask_claude so views.py doesn''t need to change.
    Returns None if something goes wrong (so views can show a friendly error).
    """
    try:
        client = get_client()
        response = client.models.generate_content(
            model="gemini-flash-lite-latest",
            contents=user_message,
            config={
                "system_instruction": system_prompt,
                "max_output_tokens": max_tokens,
            }
        )
        return response.text
    except Exception as e:
        print(f"AI ERROR: {e}")
        return None



