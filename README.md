# 🛒 Interactive Price Tracker Agent (v2.0)

An autonomous, conversational AI agent that tracks market prices across multiple vendors and interacts via secure email.

---

## 🚀 Overview
This project has evolved from a simple scraper into a **Modular Interactive System**. It doesn't just find prices—it listens for your commands, organizes data, and reports back autonomously.

### Key Features
*   **Interactive Mode:** Reply to the agent's daily email to request specific price checks.
*   **Intelligent Sorting:** Automatically sorts results from cheapest to most expensive.
*   **Geolocation Spoofing:** Bypasses regional blocks using Playwright's browser context.
*   **Persistence:** Saves every scan to `price_history.csv` to track long-term trends.
*   **Secure Secrets:** Uses `.env` and `.gitignore` to protect your email credentials.

---

## 🛠️ Project Architecture
1. **`run_agent.py`**: The Orchestrator (handles command-line arguments and CSV logging).
2. **`send_prompt.py`**: The "Daily Alarm" that asks you what to buy.
3. **`listener.py`**: The "Ear" that reads your email replies using IMAP.
4. **`scraper.py`**: The "Researcher" that performs headless browser automation.
5. **`emailer.py`**: The "Messenger" that handles SMTP/SSL email delivery.

---

## ⚙️ Setup & Installation

1. **Clone & Environment:**
   ```bash
   git clone https://github.com/Bharath-Sal/price-tracker-agent.git
   cd price_tracker
   python3 -m venv venv
   source venv/bin/activate
   pip install playwright python-dotenv
   playwright install chromium
   ```

2. **Configuration:**
   Create a `.env` file with your Google App Password:
   ```env
   EMAIL_USER=your_email@gmail.com
   EMAIL_PASS=your_google_app_password
   ```

---

## 🚦 How to Use
*   **Automated Mode:** The agent runs via Cron (10:00 AM Prompt, 10:30 AM Listen).
*   **Manual Scan:** `python run_agent.py "Product Name"`
*   **Check Inbox:** `python listener.py`

---

## 🌍 Open Source
This is a DevOps-ready project. Contributions are welcome! Future updates will include Cloud Deployment (AWS) and LLM-based product matching.
