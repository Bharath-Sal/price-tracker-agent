import smtplib
import ssl
import os
from dotenv import load_dotenv
from email.message import EmailMessage

# Load credentials from .env
load_dotenv()

def send_email(subject, body, receiver=None):
    email_sender = os.getenv("EMAIL_USER")
    email_password = os.getenv("EMAIL_PASS")
    
    # If no receiver is specified, send it to yourself
    if receiver is None:
        receiver = email_sender

    # Create the envelope
    msg = EmailMessage()
    msg['From'] = email_sender
    msg['To'] = receiver
    msg['Subject'] = subject
    msg.set_content(body)

    # Connect and Send
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(email_sender, email_password)
        server.send_message(msg)

if __name__ == "__main__":
    # Test call
    print("Testing emailer...")
    send_email("Test Subject", "Test Body")
    print("Test email sent!")
