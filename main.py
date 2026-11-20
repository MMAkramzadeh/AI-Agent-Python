import argparse
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI

from call_function import available_functions, call_function
from prompts import system_prompt


def main():
    load_dotenv()
    api_key = os.environ.get("NVIDIA_API_KEY")
    if api_key is None:
        raise RuntimeError("No API key is set.")

    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
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
    tool_call_limit = True
    for _ in range(30):
        response = client.chat.completions.create(
            model="nvidia/nemotron-3.5-super-vl-120b-a12b",
            messages=messages,
            temperature=0,
            tools=available_functions,
            max_tokens=16384,
        )
        message = response.choices[0].message
        messages.append(message)
        if message.tool_calls is not None:
            for tool_call in message.tool_calls:
                result_message = call_function(tool_call, args.verbose)
                if result_message["content"] == "":
                    raise Exception("No Content on message.")
                if args.verbose:
                    print(f"-> {result_message['content']}")
                messages.append(result_message)
        else:
            tool_call_limit = False
            break

    if tool_call_limit:
        print("Maximum tool calling")
        sys.exit(1)

    if response.usage is None:
        raise RuntimeError("Usage is None")
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
