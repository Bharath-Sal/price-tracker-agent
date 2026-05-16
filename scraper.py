# scraper.py
import time
from playwright.sync_api import sync_playwright
import re

# HYDERABAD GPS
LAT, LNG = 17.3850, 78.4867

def get_blinkit_price(page, product_name):
    try:
        print(f"📦 Checking Blinkit for {product_name}...")
        page.goto(f"https://blinkit.com/s/?q={product_name}", timeout=60000)
        page.wait_for_selector(".tw-line-clamp-2", timeout=15000)
        
        price_elements = page.locator("div:has-text('₹')").all()
        price = "N/A"
        for el in price_elements:
            txt = el.text_content().strip()
            if '₹' in txt and any(char.isdigit() for char in txt) and "ADD" not in txt and len(txt) < 15:
                price = txt
                break
        
        name = page.locator(".tw-line-clamp-2").first.text_content().strip()
        return {"store": "Blinkit", "name": name, "price": price}
    except:
        return None

def get_zepto_price(page, product_name):
    try:
        print(f"📦 Checking Zepto for {product_name}...")
        page.goto(f"https://www.zeptonow.com/search?query={product_name}", timeout=60000)
        
        # 🕒 Give it time to load results
        time.sleep(8)
        
        # 🎯 VISUAL SELECTOR: Find the first element that looks like a price tag
        # We look for ANY element containing ₹ that is near the top
        price_locator = page.locator("xpath=//div[contains(text(), '₹')] | //span[contains(text(), '₹')] | //p[contains(text(), '₹')]").first
        price_locator.wait_for(timeout=10000)
        
        price = price_locator.text_content().strip()
        
        # The name is usually in a heading or bold text nearby
        # We'll look for the text in the same product card container
        container = price_locator.locator("xpath=./ancestor::a")
        full_text = container.text_content().strip()
        
        # Extract name (the first long string of text in the container)
        name_match = re.search(r'([A-Z][a-z]+(?:\s[A-Z][a-z]+)+)', full_text)
        name = name_match.group(0) if name_match else "Product Found"
        
        return {"store": "Zepto", "name": name, "price": price}
    except Exception as e:
        page.screenshot(path="zepto_error.png")
        print(f"⚠️ Zepto Error: {e}")
        return None

def get_price(product_name: str) -> list:
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            geolocation={"latitude": LAT, "longitude": LNG},
            permissions=["geolocation"],
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        # Check Blinkit
        b_res = get_blinkit_price(page, product_name)
        if b_res: results.append(b_res)
        
        # Check Zepto
        z_res = get_zepto_price(page, product_name)
        if z_res: results.append(z_res)
        
        browser.close()
    return results
