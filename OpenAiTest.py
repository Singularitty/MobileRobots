import os
import openai

def read_api_key() -> str:
    with open("apikey", "r") as file:
        key = file.read()
    return key


def main():
    openai.api_key = read_api_key()

    MODEL = "gpt-3.5-turbo"
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "" }
        ]
    )

    



if __name__ == "__main__":
    main()
    