"""Sends a prompt to a model on OpenRouter and returns the model's reply."""
from pathlib import Path

from dotenv import dotenv_values
from openai import OpenAI

MODEL = "baidu/ernie-5.5-flash-preview:free"

# Read the settings in the .env file that is in the same folder as this file.
settings = dotenv_values(Path(__file__).with_name(".env"))


def ask_llm(system_prompt, user_prompt):
    """Send a system prompt and a user prompt to the model and return its reply."""
    api_key = settings.get("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("No OPENROUTER_API_KEY found in the .env file")

    # Point the OpenAI client at OpenRouter instead of OpenAI.
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.choices[0].message.content or ""
