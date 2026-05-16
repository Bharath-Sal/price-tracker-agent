# send_prompt.py
import os
from dotenv import load_dotenv
from emailer import send_email

load_dotenv()

def send_daily_query():
    # We use this exact tag so the listener can find it later
    subject = "[Agent-Task] What should I check for today?"
    body = """Hello! 

Reply to this email with the names of any products you want me to price-check.
Example:
iPhone 15, Sony WH-1000XM5, Milk

I will scan and send you the cheapest options sorted by price."""
    
    print("📧 Sending daily prompt...")
    send_email(subject, body, os.getenv("EMAIL_USER"))
    print("✨ Prompt sent successfully!")

if __name__ == "__main__":
    send_daily_query()
