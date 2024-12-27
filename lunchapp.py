import requests
from telethon import TelegramClient

# Telegram Bot and Channel Configuration
API_ID = 'your_api_id'
API_HASH = 'your_api_hash'
BOT_TOKEN = 'your_bot_token'

# App Link to Launch
APP_LINK = 'https://t.me/rating/app?startapp=ref_ad3fb55411968705'

# Initialize Telegram Client
client = TelegramClient('launch_app_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Function to Launch App
def launch_app(APP_LINK):
    try:
        print(f"Launching app with link: {APP_LINK}")
        # You can programmatically open the link if your platform supports it, e.g., webbrowser module
        response = requests.get(APP_LINK)  # Perform a GET request to simulate link interaction
        if response.status_code == 200:
            print("App launched successfully.")
        else:
            print(f"Failed to launch app. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error launching app: {e}")



