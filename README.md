# 🛒 Price Tracker Agent: A Modular AI-Powered Scraper

An automated market research agent that tracks grocery prices across multiple vendors (Blinkit, Zepto, BigBasket, etc.) and delivers a consolidated report via email.

---

## 🚀 Overview
This project is an **Autonomous Price Tracking Agent** designed to bypass modern web restrictions. It uses headless browser automation to simulate human behavior, extracts real-time pricing data, and handles secure notification delivery.

### Key Features
*   **Geolocation Emulation:** Bypasses regional content blocks by spoofing GPS coordinates.
*   **Multi-Vendor Scraping:** Dynamically identifies store names and prices from DOM structures.
*   **Secure Notifications:** Uses SMTP with SSL encryption for automated email reporting.
*   **Environment Isolation:** Implements `.env` for secret management and `venv` for dependency control.

---

## 🛠️ Technical Stack
*   **Language:** Python 3.x
*   **Automation:** Playwright (Chromium)
*   **Communication:** SMTP (Simple Mail Transfer Protocol)
*   **Version Control:** Git & GitHub
*   **Security:** Dotenv (Secret Management)

---

## 📂 Project Structure
*   `run_agent.py`: The Orchestrator (Manager) that runs the end-to-end workflow.
*   `scraper.py`: The Researcher (Eyes) that handles browser automation and data extraction.
*   `emailer.py`: The Messenger (Notifier) that manages SMTP connections and email delivery.
*   `.env`: The Vault (Secrets) where sensitive API keys and passwords reside.
*   `.gitignore`: The Security Guard that prevents sensitive files from being leaked to GitHub.

---

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Bharath-Sal/price-tracker-agent.git
   cd price_tracker
   ```

2. **Create a Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install playwright python-dotenv
   playwright install chromium
   ```

4. **Configure Secrets:**
   Create a `.env` file in the root directory:
   ```env
   EMAIL_USER=your_email@gmail.com
   EMAIL_PASS=your_app_password
   ```

---

## 🚦 Usage
Run the main agent script:
```bash
python run_agent.py
```

## 🛡️ Security Best Practices
*   **App Passwords:** Do not use your primary Gmail password. Generate an [App Password](https://myaccount.google.com/apppasswords).
*   **Environment Variables:** Never commit your `.env` file to version control.
