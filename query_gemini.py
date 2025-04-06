from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("gemini_api_key"))


def chat_with_gemini(input_prompt):
    base_prompt = """Please take this data, and return names, emails, and IDs \
        of any 2 or more people with similar backgrounds or interests in \
        fields provided that you decipher as descriptive.

        Please return the related/similar people in separate groups. Please \
        separate these groups with the characters '{}' (left curly brace, \
        right curly brace), so I can split them up into individual objects \
        and manipulate them as such in my code.

        Please also add a brief "potential email introduction text" at the \
        end of each group, using the data you matched them on, for easy \
        copy-pasting.

        Please return *aggressively*, that is, return even if you are unsure \
        I would rather have lower quality matches to review than less matches. \
        Overall--quantity over quality. 

        Please also return the emails from the groups a second time, \
        separated as comma-separated lists, also separated by groups but \
        with '[]' (left square bracket, right square bracket), at beginning \
        of the output (no need for a code block like ```, just use this \
        format). For example:
            email@email.com,email2@gmail.com,email3@gmail.com
            []
            email4@gmail.com,email5@gmail.com
            []
            email6@gmail.com,email7@gmail.com,email8@gmail.com
            {}
            --rest of output--
        \n\n"""

    input_prompt = base_prompt + input_prompt

    response = client.models.generate_content(
        # model="gemini-2.0-flash",
        model="gemini-2.5-pro-exp-03-25",
        contents=input_prompt,
    )

    print(response.text)
    return response.text
