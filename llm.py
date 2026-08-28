from openai import OpenAI
from functions.call_functions import available_functions

def get_response(client: OpenAI, messages: list):
    return client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
        temperature=0,
    )
