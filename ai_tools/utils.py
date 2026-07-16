from decouple import config
from anthropic import Anthropic

_client = None

def get_client():
    global _client
    if _client is None:
        api_key = config("ANTHROPIC_API_KEY")
        _client = Anthropic(api_key=api_key)
    return _client


def ask_claude(system_prompt, user_message, max_tokens=1000):
    """
    Sends a prompt to Claude and returns the plain text response.
    Returns None if something goes wrong (so views can show a friendly error).
    """
    try:
        client = get_client()
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        return response.content[0].text
    except Exception as e:
        print(f"AI ERROR: {e}")
        return None
