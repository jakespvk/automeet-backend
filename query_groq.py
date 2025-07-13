from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)


def chat_with_groq(input_prompt):
    base_prompt = """Please take this data, and return names, emails, and IDs \
        of any 2 or more people with similar backgrounds or interests in \
        fields provided that you decipher as descriptive. Please also include \
        the data you pulled that helped you come to these conclusions for each \
        person.

        Please return the related/similar people in separate groups. Please \
        separate these groups with the characters '{}' (left curly brace, \
        right curly brace), so I can split them up into individual objects \
        and manipulate them as such in my code. Please format these groups \
        as HTML <p> tags, and include <br> tags or other methods to show \
        line breaks instead of backslash-n.

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

    # input_prompt = (
    #     base_prompt
    #     + """
    # micahhuang@gmail.com,lauramichelle@gmail.com,tigerheart@gmail.com
    # []
    # lauramichelle@gmail.com,entertainment@gmail.com,tigerheart@gmail.com
    # []
    # micahhuang@gmail.com,tigerheart@gmail.com
    # []
    # elvish_treaty@icloud.com,mitchell@gmail.com,adayinasilverdik@gmail.com
    # []
    # elvish_treaty@icloud.com,mitchell@gmail.com,adayinasilverdik@gmail.com,13154955@163.com,micahhuang@gmail.com,lauramichelle@gmail.com,cory@gmail.com,entertainment@gmail.com,tigerheart@gmail.com
    # []
    # tigerheart@gmail.com,cory@gmail.com
    # {}
    # Name: Micah Huang
    # Email: micahhuang@gmail.com
    # ID: 6125
    #
    # Name: Laura Ramirez
    # Email: lauramichelle@gmail.com
    # ID: 5152
    #
    # Name: TigerHeart
    # Email: tigerheart@gmail.com
    # ID: 6517
    #
    # Potential email introduction text: Hi all, I'm connecting you as you each expressed an interest in community building and fostering meaningful connections in your backgrounds. Perhaps you might find common ground or opportunities to collaborate.
    # {}
    # Name: Laura Ramirez
    # Email: lauramichelle@gmail.com
    # ID: 5152
    #
    # Name: Sheila TRUE
    # Email: entertainment@gmail.com
    # ID: 6440
    #
    # Name: TigerHeart
    # Email: tigerheart@gmail.com
    # ID: 6517
    #
    # Potential email introduction text: Hi all, connecting you as you share experience as founders, owner/operators, or entrepreneurs leading your own ventures. Thought you might benefit from sharing insights.
    # {}
    # Name: Micah Huang
    # Email: micahhuang@gmail.com
    # ID: 6125
    #
    # Name: TigerHeart
    # Email: tigerheart@gmail.com
    # ID: 6517
    #
    # Potential email introduction text: Hi both, I noticed you both have backgrounds involving creative fields like performance arts, music, film, or media. Thought you might find a connection valuable.
    # {}
    # Name: Langston Tolbert
    # Email: elvish_treaty@icloud.com
    # ID: 13286
    #
    # Name: Mitchell Meislin
    # Email: mitchell@gmail.com
    # ID: 3369
    #
    # Name: Reha
    # Email: adayinasilverdik@gmail.com
    # ID: 3678
    #
    # Potential email introduction text: Hi all, connecting you as you seem to work in professional services fields (legal, consulting, agency). Perhaps there's overlap or shared experiences worth discussing.
    # {}
    # Name: Langston Tolbert
    # Email: elvish_treaty@icloud.com
    # ID: 13286
    #
    # Name: Mitchell Meislin
    # Email: mitchell@gmail.com
    # ID: 3369
    #
    # Name: Reha
    # Email: adayinasilverdik@gmail.com
    # ID: 3678
    #
    # Name: Tess Zhang
    # Email: 13154955@163.com
    # ID: 14491
    #
    # Name: Micah Huang
    # Email: micahhuang@gmail.com
    # ID: 6125
    #
    # Name: Laura Ramirez
    # Email: lauramichelle@gmail.com
    # ID: 5152
    #
    # Name: Cory Watkins-Suzuki
    # Email: cory@gmail.com
    # ID: 3568
    #
    # Name: Sheila TRUE
    # Email: entertainment@gmail.com
    # ID: 6440
    #
    # Name: TigerHeart
    # Email: tigerheart@gmail.com
    # ID: 6517
    #
    # Potential email introduction text: Hi all, I'm connecting this group as you all provided professional links (like LinkedIn or company websites) in your info, suggesting a focus on professional networking or online presence. Perhaps you can share insights or connect further.
    # {}
    # Name: TigerHeart
    # Email: tigerheart@gmail.com
    # ID: 6517
    #
    # Name: Cory Watkins-Suzuki
    # Email: cory@gmail.com
    # ID: 3568
    #
    # Potential email introduction text: Hi both, I noticed a potential shared interest in themes of healing, wellness, or human connection based on your provided info (TigerHeart's mention of healing, Cory's 'SharingHuman'). Thought a connection might be interesting.
    # """
    # )

    response = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": input_prompt,
            }
        ],
        # model="llama-3.3-70b-versatile",
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        stream=False,
    )

    print(response.choices[0].message.content)
    return response.choices[0].message.content
