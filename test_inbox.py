import imaplib
import os
from dotenv import load_dotenv

load_dotenv()

def test_connection():
    email_user = os.getenv("EMAIL_USER")
    email_pass = os.getenv("EMAIL_PASS")
    
    try:
        # Connect to Gmail's IMAP server
        print("🔍 Attempting to connect to Gmail IMAP...")
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        
        # Try to login
        mail.login(email_user, email_pass)
        print("✅ SUCCESS! Your inbox is listening.")
        
        # List folders just to be sure
        status, folders = mail.list()
        print(f"📂 Found {len(folders)} folders in your email.")
        
        mail.logout()
    except Exception as e:
        print(f"❌ CONNECTION FAILED: {e}")

if __name__ == "__main__":
    test_connection()
