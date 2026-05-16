# run_agent.py
import time
import os
import sys
import csv  # <--- New Connection: Talking to Data Files
from datetime import datetime
from scraper import get_price
from emailer import send_email

def save_to_history(product, price, store):
    file_exists = os.path.isfile("price_history.csv")
    
    with open("price_history.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        # If the file is brand new, add the "Header" (column names)
        if not file_exists:
            writer.writerow(["Timestamp", "Product", "Price", "Store"])
        
        # Write the data
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), product, price, store])

def run_price_tracker():
    if len(sys.argv) > 1:
        products = sys.argv[1:]
        print(f"🎯 Targeted Scan: {products}")
    else:
        products = ["Amul Milk", "Ruchi Gold Oil"]
        print(f"🔍 Full Scan: {products}")

    report = "🛒 --- PRICE REPORT ---\n\n"
    
    for item in products:
        data = get_price(item)
        price = data['cheapest_price']
        store = data['store']
        
        line = f"✅ {item}: {price} at {store}\n"
        report += line
        print(line.strip())
        
        # 💾 THE MEMORY: Save each result to our CSV file
        if price not in ["NOT FOUND", "ERROR"]:
            save_to_history(item, price, store)
            
        time.sleep(2)

    report += f"\n⏰ Updated: {time.ctime()}\n"
    report += "🔗 Powered by your Automation Agent"
    
    print("\n📧 Sending email...")
    send_email(f"Price Update: {', '.join(products)}", report, os.getenv("EMAIL_USER"))
    print("✨ Complete!")

if __name__ == "__main__":
    run_price_tracker()
