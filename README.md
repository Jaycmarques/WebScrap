Price Monitoring Bot
This Python script monitors the price of a specific product from various e-commerce websites and sends notifications via Telegram if the price drops below a defined threshold.

Features
Price Monitoring: Checks prices on multiple websites to find the lowest price.
Telegram Notifications: Sends a message to a Telegram chat when the price falls below a specified target.
Automatic Scheduling: Uses APScheduler to run the price check periodically.
Web Scraping: Utilizes BeautifulSoup and Selenium to scrape product prices from web pages.
Requirements
Python 3.x
requests
beautifulsoup4
python-telegram-bot
apscheduler
selenium
webdriver-manager
python-decouple

Add your Telegram bot token and chat ID to the .env file:
TELEGRAM_TOKEN=your_telegram_bot_token
CHAT_ID=your_chat_id

Install Dependencies:
Use pipenv to install the required packages

Setup
Create a Telegram Bot:

Chat with BotFather on Telegram to create a new bot and get your bot token.
Configure Your Environment:

Create a .env file in the root directory of the project.
Add your Telegram bot token and chat ID to the .env file

Update the Product URL and Target Price:

Modify the target_url variable in the script to the URL of the product you want to monitor.
Set the preco_alvo (target price) to your desired value.

Usage
Run the script to test sending a message:
python test_bot.py

Run the script to start monitoring:
python webscrap.py

License
This project is licensed under the MIT License. See the LICENSE file for details.

Feel free to adjust any specifics based on your needs!


