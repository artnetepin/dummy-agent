import argparse
import os
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI


def generate_content(client: OpenAI, messages: list[Any], is_verbose: bool) -> None:
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
    )
    if not response.usage:
        raise RuntimeError("No usage information in response")

    if is_verbose:
        print("User prompt: ", messages[0]["content"])
        print("Prompt tokens: ", response.usage.prompt_tokens)
        print("Response tokens: ", response.usage.completion_tokens)
    print("Response: ")
    print(response.choices[0].message.content)


def main():
    load_dotenv()
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY not set")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true",
                        help="Enable verbose output")
    args = parser.parse_args()

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    messages: list[dict[str, str]] = [
        {"role": "user", "content": args.user_prompt},
    ]
    is_verbose = args.verbose

    generate_content(client, messages, is_verbose)


if __name__ == "__main__":
    main()
