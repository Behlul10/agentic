from functions.call_functions import (
    available_functions,
    call_function,
)
from prompts import system_prompt
from dotenv import load_dotenv
from openai import OpenAI
import os
import argparse

def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt",)
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("the openrouter api key is missing!")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
        temperature=0,
    )

    if not response.usage:
        raise RuntimeError("The api request failed.")

    message = response.choices[0].message

    for tool_call in message.tool_calls or []:
        result_message = call_function(tool_call, args.verbose)
        if not result_message["content"]:
            raise RuntimeError(f'Content is empty: {result_message["content"]}')
        if args.verbose:
            print(f"-> {result_message['content']}")

    if args.verbose:
        print(f'User prompt: {args.user_prompt}')
        print(f'Prompt tokens: {response.usage.prompt_tokens}')
        print(f'Response tokens: {response.usage.completion_tokens}')
    if message.content:
        print(message.content)

if __name__ == "__main__":
    main()
