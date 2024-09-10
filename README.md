# Price Monitoring Bot

This Python script monitors the price of a specific product from various e-commerce websites and sends notifications via Telegram if the price drops below a defined threshold.

## Features

- **Price Monitoring:** Checks prices on multiple websites to find the lowest price.
- **Telegram Notifications:** Sends a message to a Telegram chat when the price falls below a specified target.
- **Automatic Scheduling:** Uses APScheduler to run the price check periodically.
- **Web Scraping:** Utilizes BeautifulSoup to scrape product prices from web pages.

## Requirements

- Python 3.x
- `requests`
- `beautifulsoup4`
- `python-telegram-bot`
- `apscheduler`
- `python-decouple`

## Setup

1. **Create a Telegram Bot:**
   - Chat with [BotFather](https://t.me/botfather) on Telegram to create a new bot and get your bot token.

2. **Configure Your Environment:**
   - Create a `.env` file in the root directory of the project.
   - Add your Telegram bot token and chat ID to the `.env` file:
     ```plaintext
     TELEGRAM_TOKEN=your_telegram_bot_token
     CHAT_ID=your_chat_id
     ```

3. **Install Dependencies:**
   - Use `pipenv` to install the required packages:
     ```bash
     pipenv install requests beautifulsoup4 python-telegram-bot apscheduler python-decouple
     ```

4. **Update the Product URL and Target Price:**
   - Modify the `target_url` variable in the script to the URL of the product you want to monitor.
   - Set the `price_target` to your desired value.

## Usage

- **Run the script to test sending a message:**
  ```bash
  python test_bot.py

- **Run the script to start monitoring:**
  ```bash
  python webscrap.py


License
This project is licensed under the MIT License. See the LICENSE file for details.
