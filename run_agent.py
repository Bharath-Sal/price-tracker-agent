# run_agent.py
import time
import os
from scraper import get_price
from emailer import send_email

def run_price_tracker():
    # Simple list as requested
    products = ["Amul Milk", "Ruchi Gold Oil"]
    report = "🛒 --- PRICE REPORT ---\n\n"
    
    print("🚀 Starting Simple Price Tracker...")
    
    for item in products:
        data = get_price(item)
        line = f"✅ {item}: {data['cheapest_price']} at {data['store']}\n"
        report += line
        print(line.strip())
        time.sleep(2)

    report += f"\n⏰ Updated: {time.ctime()}\n"
    report += "🔗 Powered by your Automation Agent"
    
    print("\n📧 Sending email...")
    send_email("Price Update", report, os.getenv("EMAIL_USER"))
    print("✨ Complete!")

if __name__ == "__main__":
    run_price_tracker()
