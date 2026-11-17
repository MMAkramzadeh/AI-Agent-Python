import argparse
import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from call_function import available_functions, call_function
from prompts import system_prompt


def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError("No API key is set.")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    parser = argparse.ArgumentParser()
    parser.add_argument("user_prompt", type=str, help="Your prompt")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )
    args = parser.parse_args()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        temperature=0,
        tools=available_functions,
    )

    message = response.choices[0].message
    if message.tool_calls is not None:
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, args.verbose)
            if result_message["content"] == "":
                raise Exception
            if args.verbose:
                print(f"-> {result_message['content']}")
    if response.usage is None:
        raise RuntimeError("Usage is None")

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
