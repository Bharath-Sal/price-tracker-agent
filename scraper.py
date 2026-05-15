# scraper.py
import time
import re
from playwright.sync_api import sync_playwright

def get_price(product_name: str) -> dict:
    with sync_playwright() as p:
        print(f"🚀 Scanning for {product_name} in Hyderabad (GPS Mode)...")
        # Hyderabad GPS Coordinates
        lat, lng = 17.3850, 78.4867
        
        browser = p.chromium.launch(headless=True)
        # We tell the browser it is physically in Hyderabad
        context = browser.new_context(
            geolocation={"latitude": lat, "longitude": lng},
            permissions=["geolocation"],
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        try:
            # 1. Search directly via URL
            import requests
            encoded = requests.utils.quote(product_name)
            page.goto(f"https://comparify.pro/?query={encoded}", timeout=60000)
            page.wait_for_load_state("networkidle")
            
            # Wait for the site to read the GPS
            time.sleep(12)

            # 2. Extract price
            print("💰 Reading prices...")
            price_locator = page.locator("text=₹").first
            if price_locator.is_visible():
                price = price_locator.text_content().strip()
                container = price_locator.locator("xpath=../../..")
                context_text = container.text_content()
                
                store = "UNKNOWN"
                for s in ["Blinkit", "Zepto", "Instamart", "BigBasket", "JioMart", "Flipkart", "DMart"]:
                    if s.lower() in context_text.lower():
                        store = s
                        break
                
                return {"product": product_name, "cheapest_price": price, "store": store}
            
            return {"product": product_name, "cheapest_price": "NOT FOUND", "store": "UNKNOWN"}

        except Exception as e:
            print(f"❌ Scraper Exception: {e}")
            return {"product": product_name, "cheapest_price": "ERROR", "store": "UNKNOWN"}
        finally:
            browser.close()

def get_smart_results(search, keywords, top_n=1):
    return [get_price(search)]
