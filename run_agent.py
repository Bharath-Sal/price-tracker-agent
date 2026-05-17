# run_agent.py
import time
import os
import sys
import re
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

def get_cheapest_deal(store_results):
    if not store_results:
        return "NOT FOUND", "N/A"
    
    cheapest_price = None
    cheapest_store = None
    
    for res in store_results:
        price_str = res['price']
        # Extract digits from price string (e.g. "₹122 ₹153" -> ["122", "153"])
        digits = re.findall(r'\d+', price_str)
        if not digits:
            continue
        price_val = int(digits[0])
        
        if cheapest_price is None or price_val < cheapest_price:
            cheapest_price = price_val
            cheapest_store = res['store']
            
    if cheapest_price is not None:
        return f"₹{cheapest_price}", cheapest_store
    return "NOT FOUND", "N/A"

def run_price_tracker():
    if len(sys.argv) > 1:
        products = sys.argv[1:]
        print(f"🎯 Targeted Scan: {products}")
    else:
        products = ["Amul Milk", "Ruchi Gold Oil"]
        print(f"🔍 Full Scan: {products}")

    report = "🛒 --- PRICE REPORT ---\n\n"
    
    for item in products:
        store_results = get_price(item)
        price, store = get_cheapest_deal(store_results)
        
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
