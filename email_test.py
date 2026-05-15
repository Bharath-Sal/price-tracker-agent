import smtplib
import ssl
import os
from dotenv import load_dotenv
from email.message import EmailMessage

# 1. Open the .env safe
load_dotenv()
email_sender = os.getenv("EMAIL_USER")
email_password = os.getenv("EMAIL_PASS")
email_receiver = email_sender # We will send the test to ourselves!

# 2. Create the envelope
msg = EmailMessage()
msg['From'] = email_sender
msg['To'] = email_receiver
msg['Subject'] = "Hello from your AI Agent!"
msg.set_content("This is a test email. Stage 1 is working!")

# 3. Connect to the Post Office and Send
print("Connecting to Gmail...")
context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(email_sender, email_password)
    server.send_message(msg)

print("Success! Check your inbox.")
