import openai
import logging

from src.config.settings import OPENAI_API_KEY


# Random commit message suggestion
def openai_chat(prompt, model="gpt-3.5-turbo", temperature=0.5):
    openai.api_key = OPENAI_API_KEY
    try:
        messages = [{"role": "user", "content": prompt.replace("'", "").replace('"', '')}]
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature,
        )
        r = response.choices[0].message["content"]
        return r
    except Exception as e:
        logging.error(f"Error: {e}")
        return None
