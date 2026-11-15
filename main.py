import argparse
import os

from dotenv import load_dotenv
from openai import OpenAI


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
    args = parser.parse_args()

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {
                "role": "user",
                "content": args.user_prompt,
            }
        ],
    )
    if response.usage is not None:
        print("Prompt tokens: " + str(response.usage.prompt_tokens))
        print("Response tokens: " + str(response.usage.completion_tokens))
    else:
        raise RuntimeError("Usage is None")

    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
