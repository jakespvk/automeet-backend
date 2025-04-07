import os
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


load_dotenv()

gmail_user = os.getenv("gmail_user")
gmail_password = os.getenv("gmail_password")

# gpt_output = """\
# micahhuang@gmail.com,tigerheart@gmail.com
# []
# lauramichelle@gmail.com,entertainment@gmail.com,tigerheart@gmail.com
# []
# micahhuang@gmail.com,lauramichelle@gmail.com,tigerheart@gmail.com,cory@gmail.com
# []
# mitchell@gmail.com,adayinasilverdik@gmail.com
# []
# entertainment@gmail.com,tigerheart@gmail.com
# {}
# <p>
#   --- Group: Arts/Media & Social Impact ---<br>
#   <br>
#   Name: MicahHuang<br>
#   Email: micahhuang@gmail.com<br>
#   ID: 6125<br>
#   Matching Data:<br>
#   - 'I work at the intersection of performance arts and social justice, and would like to help cultivate mutually beneficial connections between communities, across nominal barriers of cultural identity and social position.'<br>
#   - 'Independent Artist (Harvard University affiliate)'<br>
#   <br>
#   Name: TigerHeart<br>
#   Email: tigerheart@gmail.com<br>
#   ID: 6517<br>
#   Matching Data:<br>
#   - 'I am an agent of change, a facilitator of the new world through music, media, and heart centered entrepreneurialism.'<br>
#   - 'Professionally, I have been successful in the film industry...partnering with a-list talent to create and produce the content.'<br>
#   - 'Musically, I have released one ep and one single...'<br>
#   - 'successful DJ for 10 years...'<br>
#   - 'Heart center productions | tigerheart healing'<br>
#   <br>
#   Potential Email Introduction Text:<br>
#   Hi Micah and TigerHeart,<br>
#   Connecting you both as you share interests and work at the intersection of arts/media (performance, film, music) and creating positive social impact/connections. Hope you find common ground!
# </p>
# {}
# <p>
#   --- Group: Founders / Business Owners / Entrepreneurs ---<br>
#   <br>
#   Name: LauraRamirez<br>
#   Email: lauramichelle@gmail.com<br>
#   ID: 5152<br>
#   Matching Data:<br>
#   - 'As an on-site owner/operator of a successful business in l.a.'<br>
#   - 'R Bar - Koreatown, L.A.'<br>
#   <br>
#   Name: SheilaTRUE<br>
#   Email: entertainment@gmail.com<br>
#   ID: 6440<br>
#   Matching Data:<br>
#   - 'I am the founder of my company'<br>
#   - 'Events Come True'<br>
#   <br>
#   Name: TigerHeart<br>
#   Email: tigerheart@gmail.com<br>
#   ID: 6517<br>
#   Matching Data:<br>
#   - 'heart centered entrepreneurialism'<br>
#   - 'create my own production company, heart center productions.'<br>
#   - 'for profit ventures: organic smoothie and smoke shop; building developments'<br>
#   - 'Heart center productions | tigerheart healing'<br>
#   <br>
#   Potential Email Introduction Text:<br>
#   Hi Laura, Sheila, and TigerHeart,<br>
#   Connecting you all as founders and entrepreneurs running your own distinct ventures, from hospitality and events to media production and wellness. Hope you find this connection valuable!
# </p>
# {}
# <p>
#   --- Group: Social Impact / Community Focus ---<br>
#   <br>
#   Name: MicahHuang<br>
#   Email: micahhuang@gmail.com<br>
#   ID: 6125<br>
#   Matching Data:<br>
#   - 'social justice'<br>
#   - 'cultivate mutually beneficial connections between communities'<br>
#   <br>
#   Name: LauraRamirez<br>
#   Email: lauramichelle@gmail.com<br>
#   ID: 5152<br>
#   Matching Data:<br>
#   - 'long for community'<br>
#   - 'Being a part of something bigger than my own personal world'<br>
#   <br>
#   Name: TigerHeart<br>
#   Email: tigerheart@gmail.com<br>
#   ID: 6517<br>
#   Matching Data:<br>
#   - 'agent of change, a facilitator of the new world'<br>
#   - 'creating the infrastructure for a more cohesive and harmonious society'<br>
#   - 'Heart centered entrepreneurialism'<br>
#   - 'nonprofit work to assure food and housing security for all'<br>
#   - 'communities of co-existence'<br>
#   - 'bring more peace, freedom, and connectedness to our human experience'<br>
#   <br>
#   Name: CoryWatkins-Suzuki<br>
#   Email: cory@gmail.com<br>
#   ID: 3568<br>
#   Matching Data:<br>
#   - 'SharingHuman' (Company name implies focus on human connection/stories)<br>
#   <br>
#   Potential Email Introduction Text:<br>
#   Hi Micah, Laura, TigerHeart, and Cory,<br>
#   Connecting you all as you've expressed interest in or focus on community building, social impact, fostering connection, and being part of something larger than yourselves. Hope you find valuable connections here!
# </p>
# {}
# <p>
#   --- Group: Agency / Consulting ---<br>
#   <br>
#   Name: MitchellMeislin<br>
#   Email: mitchell@gmail.com<br>
#   ID: 3369<br>
#   Matching Data:<br>
#   - 'Accenture'<br>
#   <br>
#   Name: Reha<br>
#   Email: adayinasilverdik@gmail.com<br>
#   ID: 3678<br>
#   Matching Data:<br>
#   - 'The Fearless Agency'<br>
#   <br>
#   Potential Email Introduction Text:<br>
#   Hi Mitchell and Reha,<br>
#   Connecting you both as you work in the agency/consulting space (Accenture and The Fearless Agency respectively). Perhaps you'll find some common ground or industry insights to share!
# </p>
# {}
# <p>
#   --- Group: Shared Internal Tags (Weak Match) ---<br>
#   <br>
#   Name: SheilaTRUE<br>
#   Email: entertainment@gmail.com<br>
#   ID: 6440<br>
#   Matching Data:<br>
#   - 'sp2'<br>
#   <br>
#   Name: TigerHeart<br>
#   Email: tigerheart@gmail.com<br>
#   ID: 6517<br>
#   Matching Data:<br>
#   - 'sp3'<br>
#   <br>
#   Potential Email Introduction Text:<br>
#   Hi Sheila and TigerHeart,<br>
#   Connecting you both - based on some internal data points ('sp2', 'sp3'), it looks like you might have engaged through similar channels or programs.
# </p>
# """


def manipulate_gpt_output_to_scaffold_email(gpt_output):
    groups = gpt_output.split("{}")
    if len(groups) == 0:
        return gpt_output

    emails = groups[0].split("[]")

    html_blocks_for_output = []

    for idx, group in enumerate(groups[1:]):
        # email_intro_text = group[
        #     group.index("Potential email introduction text:") : group.index("<")
        # ].strip()
        # print(email_intro_text)
        html_blocks_for_output.append(
            f"""{group}<br>
                <a style="background-color:#000;padding:10px;\
                text-decoration:none;color:#FFF;border-radius:5px;" \
                href="mailto:?to={emails[idx].strip()}\
                &subject=Introduction&body=Hey [names]">Send Intro</a>\
                </div><p style="padding-top:10px;">*Note: \
                this will not send an email\
                until you make changes and confirm</p><br><br>"""
        )

    final_html_email = """"""
    for html_block in html_blocks_for_output:
        final_html_email = f"""{final_html_email}{html_block}"""

    final_html_email = (
        """\
        <html>
            <head>
                <meta name="color-scheme" content="light dark">
                <meta name="supported-color-schemes" content="light dark">
                <style>
                body {
                    margin-left: auto;
                    margin-right: auto;
                }
                a {
                    text-decoration: none;
                    padding: 15px;
                    border-radius: 5px;
                }
                @media (prefers-color-scheme: dark) {
                    a {
                        background-color: white;
                        color: black;
                    }
                }
                @media (prefers-color-scheme: light) {
                    a {
                        background-color: black;
                        color: white;
                    }
                }
                </style>
            </head>
            <body> 
                <h1 style="font-size:2rem;">Automeet</h1>
                """
        + final_html_email
        + """
            </body>
        </html>
    """
    )

    print(final_html_email)
    return final_html_email


def send_email(recipient_email, gpt_output):
    msg = MIMEMultipart("alternative")
    msg["From"] = "Automeet"
    msg["To"] = recipient_email
    msg["Subject"] = "Automated output from Automeet"

    msg.attach(MIMEText(f"""{gpt_output}""", "plain"))
    msg.attach(
        MIMEText(f"""{manipulate_gpt_output_to_scaffold_email(gpt_output)}""", "html")
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
        s.ehlo()
        s.login(gmail_user, gmail_password)
        s.sendmail("Automeet", recipient_email, msg.as_string())
