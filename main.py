import os, argparse, sys
from dotenv import load_dotenv
from openai import OpenAI
from config import ITERATIONS
from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("api_key not found")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="Send the message to the chatbot")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": args.user_prompt,
        },
    ]
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")

    for _ in range(ITERATIONS):
        generated_content = generate_content(client, messages, args.verbose)
        if generated_content:
            print(f"Final response:\n{generated_content}")
            return

    print("Error: Maximum iterations reached")
    sys.exit(1)


def generate_content(client: OpenAI, messages: list, verbose: bool) -> list:
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        temperature=0,
        tools=available_functions,
    )
    if not response.usage:
        raise RuntimeError("API response appears to be malformed")

    if verbose:
        print("Prompt tokens:", response.usage.prompt_tokens)
        print("Response tokens:", response.usage.completion_tokens)

    message = response.choices[0].message
    messages.append(message)
    if message.tool_calls is None:
        return message.content
    for tool_call in message.tool_calls:
        result_message = call_function(tool_call, verbose)
        if not result_message["content"]:
            raise RuntimeError(f"Empty response for {tool_call.function.name}")
        if verbose:
            print(f"-> {result_message["content"]}")
        messages.append(result_message)


if __name__ == "__main__":
    main()
