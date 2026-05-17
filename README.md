# 🛒 Interactive Price Tracker Agent (v3.0)

A high-performance, direct-to-source AI agent that compares prices between Blinkit and Zepto in real-time.

---

## 🚀 Overview
This version represents the "Gold Standard" of the project. We have removed unstable third-party aggregators and built **Direct Scrapers** for India's leading quick-commerce platforms.

### Key Features
*   **Direct Store Integration:** Scrapes live data directly from Blinkit and Zepto.
*   **Dual-Store Comparison:** Sends a side-by-side price report for every item.
*   **Visual Scraping Logic:** Uses advanced browser-level detection to find prices even when developer tags change.
*   **Interactive Messaging:** Full IMAP/SMTP integration for 2-way email communication.

---

## 🛠️ Tech Stack
*   **Core:** Python 3.x, Playwright (Chromium)
*   **Stores:** Blinkit, Zepto
*   **Infrastructure:** Git, Cron, Linux (Ubuntu/Debian)
*   **Security:** Environment Variables, App Passwords

---

## 🚦 Usage
1. **Request:** Reply to the daily agent email with your shopping list.
2. **Process:** Run `python listener.py` (or let Cron do it).
3. **Report:** Receive a formatted comparison email with the cheapest options highlighted.
