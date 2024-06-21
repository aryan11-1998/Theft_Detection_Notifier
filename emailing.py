import  smtplib, os
from email.message import EmailMessage
import imghdr

SENDER = "aryantyagi680@gmail.com"
RECEIVER = "aryantyagi680@gmail.com"
PASSWORD = os.getenv("PASSWORDS")

def send_email(images_path):
    email_message = EmailMessage()
    email_message["subject"] = "New Person showed up!"
    email_message.set_content("Hey, we just saw a new Person.")

    with open(images_path,"rb") as file:
        content = file.read()

    email_message.add_attachment(content,maintype = "image",subtype=imghdr.what(None,content))

    gmail = smtplib.SMTP("smtp.gmail.com",587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER,PASSWORD)
    gmail.sendmail(SENDER,RECEIVER,email_message.as_string())
    gmail.quit()

