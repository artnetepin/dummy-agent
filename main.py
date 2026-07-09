import argparse
import os
import sys
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

from prompts import system_prompt
from call_function import available_functions, call_function


def generate_content(client: OpenAI, messages: list[Any], is_verbose: bool) -> str | None:
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,  # type: ignore[arg-type]
    )
    if not response.usage:
        raise RuntimeError("No usage information in response")

    if is_verbose:
        print("Prompt tokens: ", response.usage.prompt_tokens)
        print("Response tokens: ", response.usage.completion_tokens)

    message = response.choices[0].message
    messages.append(message)

    if not message.tool_calls:
        return message.content

    for tool_call in message.tool_calls:
        if tool_call.type != "function":
            continue

        result_message = call_function(tool_call, verbose=is_verbose)

        if is_verbose:
            print(f"-> {result_message['content']}")

        messages.append(result_message)

    return None


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
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]
    is_verbose = args.verbose

    if is_verbose:
        print("User prompt: ", args.user_prompt)

    for _ in range(20):
        try:
            final_response = generate_content(client, messages, args.verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                return
        except Exception as e:
            print(f"Error in generate_content: {e}")

    print(f"Maximum iterations ({20}) reached")
    sys.exit(1)


if __name__ == "__main__":
    main()
