# scraper.py
import time
import requests
import re
from playwright.sync_api import sync_playwright

def get_price(product_name: str) -> dict:
    with sync_playwright() as p:
        lat, lng = 17.3850, 78.4867
        browser = p.chromium.launch(headless=True)
        
        # 🆔 PRO IDENTITY: Identifying as a real browser
        context = browser.new_context(
            geolocation={"latitude": lat, "longitude": lng},
            permissions=["geolocation"],
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        try:
            encoded = requests.utils.quote(product_name)
            url = f"https://comparify.pro/?query={encoded}"
            print(f"📡 Navigating to {url}...")
            page.goto(url, timeout=60000)
            
            # 🕒 WAIT: Wait specifically for a price to appear on the screen
            try:
                page.wait_for_selector("text=₹", timeout=20000)
                time.sleep(5) # Extra buffer for all stores to load
            except:
                print(f"⚠️ Timeout waiting for prices for {product_name}")
                return {"product": product_name, "cheapest_price": "NOT FOUND", "store": "UNKNOWN"}

            # 🔍 SCAN: Look at all results
            results = []
            price_elements = page.locator("text=₹").all()
            
            for el in price_elements:
                try:
                    price_text = el.text_content().strip()
                    # Go up to find the context
                    container = el.locator("xpath=../../..")
                    content = container.text_content().lower()
                    
                    # 🛡️ MATCH CHECK: Use a simpler search
                    # We check if at least one word from your search is in the result
                    search_words = product_name.lower().split()
                    if any(word in content for word in search_words):
                        store = "Unknown"
                        for s in ["Blinkit", "Zepto", "Instamart", "BigBasket", "JioMart", "Flipkart", "Amazon", "DMart"]:
                            if s.lower() in content:
                                store = s
                                break
                        
                        clean_price = int(''.join(filter(str.isdigit, price_text)))
                        if clean_price > 5: # Ignore suspicious low prices
                            results.append({"price": price_text, "val": clean_price, "store": store})
                except:
                    continue

            if results:
                cheapest = min(results, key=lambda x: x['val'])
                return {
                    "product": product_name, 
                    "cheapest_price": cheapest['price'], 
                    "store": cheapest['store']
                }
            
            return {"product": product_name, "cheapest_price": "NOT FOUND", "store": "UNKNOWN"}

        except Exception as e:
            print(f"❌ Scraper Error: {e}")
            return {"product": product_name, "cheapest_price": "ERROR", "store": "UNKNOWN"}
        finally:
            browser.close()
