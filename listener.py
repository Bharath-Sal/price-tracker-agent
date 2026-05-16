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

    # 🎯 SEARCH FILTER: Only UNREAD emails with our specific subject tag
    search_query = '(UNSEEN SUBJECT "[Agent-Task]")'
    status, messages = mail.search(None, search_query)
    
    if not messages[0]:
        return None

    # Get the most recent unread reply
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
            
            # Remove the "history" of the email to just get your new reply
            clean_body = body.split("On ")[0].split("---")[0].strip()
            return clean_body
    return None

def main():
    user_input = get_latest_reply()
    if not user_input:
        print("😴 No new product requests found.")
        return

    print(f"📥 New Request Received: {user_input}")
    items = [i.strip() for i in re.split(r'[,\n]', user_input) if i.strip()]
    
    results = []
    for item in items:
        print(f"🔍 Scraping: {item}...")
        data = get_price(item)
        
        # Clean price for sorting (remove ₹ and commas)
        try:
            price_val = int(re.sub(r'[^\d]', '', data['cheapest_price']))
        except:
            price_val = 999999
            
        results.append({
            "name": item,
            "price": data['cheapest_price'],
            "store": data['store'],
            "val": price_val
        })

    # 📈 Sort by price (Cheapest first)
    results.sort(key=lambda x: x['val'])

    # Format reply
    report = "📊 --- CHEAPEST DEALS FOUND ---\n\n"
    for r in results:
        report += f"✅ {r['name']}\n   Price: {r['price']}\n   Store: {r['store']}\n\n"
    
    print("📧 Sending your sorted report...")
    send_email("Results: Your Price Check", report)
    print("✨ All done!")

if __name__ == "__main__":
    main()
