# listener.py
import imaplib
import email
import os
import re
from dotenv import load_dotenv
from scraper import get_price
from emailer import send_email

load_dotenv()

def get_latest_reply():
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))
    mail.select("inbox")

    # Search for UNREAD emails with our specific subject tag
    search_query = '(UNSEEN SUBJECT "[Agent-Task]")'
    status, messages = mail.search(None, search_query)
    
    if not messages[0]:
        return None

    latest_msg_id = messages[0].split()[-1]
    status, data = mail.fetch(latest_msg_id, "(RFC822)")
    
    for response_part in data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode()
            else:
                body = msg.get_payload(decode=True).decode()
            
            clean_body = body.split("On ")[0].split("---")[0].strip()
            return clean_body
    return None

def main():
    user_input = get_latest_reply()
    if not user_input:
        print("😴 No new requests found.")
        return

    print(f"📥 New Request Received: {user_input}")
    items = [i.strip() for i in re.split(r'[,\n]', user_input) if i.strip()]
    
    report = "🛍️ --- SIDE-BY-SIDE PRICE COMPARISON ---\n\n"
    
    for item in items:
        print(f"🔍 Scraping {item} from stores...")
        store_results = get_price(item)
        
        report += f"📍 ITEM: {item.upper()}\n"
        if not store_results:
            report += "   ❌ Not found in any stores.\n"
        else:
            for res in store_results:
                report += f"   ✅ {res['store']}: {res['price']} ({res['name']})\n"
        
        report += "\n"

    print("📧 Sending your comparison report...")
    send_email("Your Store Comparison Results", report)
    print("✨ All done!")

if __name__ == "__main__":
    main()
