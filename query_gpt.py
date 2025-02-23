from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("openai_test_key"))


def chat_with_gpt(input_prompt):
    base_prompt = (
        "Please take this data, and return names and IDs of any 2 or more people \
        with similar backgrounds or interests in their description fields.  \
        Please return the related/similar people in separate groups. \
        Please return *aggressively*, that is, return even if you are unsure \
        I would rather have lower quality matches to review than less matches. \
        Overall--quantity over quality. \n"
    )
    input_prompt = base_prompt + input_prompt
    completion = client.chat.completions.create(
        model="gpt-4o-mini", messages=[{"role": "user", "content": input_prompt}]
    )
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content
