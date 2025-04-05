from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("gemini_api_key"))


def chat_with_gemini(input_prompt):
    base_prompt = """Please take this data, and return names and IDs of any \
        2 or more people with similar backgrounds or interests in fields \
        provided that you decipher as descriptive.

        Please return the related/similar people in separate groups. Please \
        separate these groups with the characters '{}' (left curly brace, \
        right curly brace), so I can split them up into individual objects \
        and manipulate them as such in my code.

        Please return *aggressively*, that is, return even if you are unsure \
        I would rather have lower quality matches to review than less matches. \
        Overall--quantity over quality. \n"""

    input_prompt = base_prompt + input_prompt

    response = client.models.generate_content(
        model="gemini-2.5-pro-exp-03-25", contents=input_prompt
    )

    print(response.text)
    return response.text
