import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse


def main():
    load_dotenv()
    api_key = os.environ.get('OPENROUTER_API_KEY')
    if not api_key:
        raise RuntimeError('api_key not found')

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    parser = argparse.ArgumentParser(description='Chatbot')
    parser.add_argument('user_prompt', type=str,
                        help='Send the message to the chatbot')
    parser.add_argument('--verbose', action='store_true',
                        help='Enable verbose output')
    args = parser.parse_args()

    messages = [
        {
            "role": "user",
            "content": args.user_prompt,
        }
    ]
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
    )

    if args.verbose == True:
        print(f'User prompt: {args.user_prompt}')
        print(f'Prompt tokens: {response.usage.prompt_tokens}')
        print(f'Response tokens: {response.usage.completion_tokens}')
    print(f'Response:\n{response.choices[0].message.content}')


if __name__ == "__main__":
    main()
