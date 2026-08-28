from functions.call_functions import call_function
from prompts import system_prompt
from dotenv import load_dotenv
from llm import get_response
from openai import OpenAI
import argparse
import sys
import os

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

    for i in range(20):
        response = get_response(client, messages)
        message = response.choices[0].message
        messages.append(message)

        if not response.usage:
            raise RuntimeError("The api request failed.")


        for tool_call in message.tool_calls or []:
            result_message = call_function(tool_call, args.verbose)
            if not result_message["content"]:
                raise RuntimeError(f'Content is empty: {result_message["content"]}')
            if args.verbose:
                print(f"-> {result_message['content']}")
            messages.append(result_message)

        if args.verbose:
            print(f'User prompt: {args.user_prompt}')
            print(f'Prompt tokens: {response.usage.prompt_tokens}')
            print(f'Response tokens: {response.usage.completion_tokens}')
        if not message.tool_calls and message.content:
            print(message.content)
            return
    print(f'Error: exceeded maximum loop tries of {i} out of 20')
    sys.exit("1")


if __name__ == "__main__":
    main()
