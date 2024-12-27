import asyncio
from telethon import TelegramClient

API_ID = '21111033'
API_HASH = 'fda348618bf2d98a6abe132d33c9ed6e'
BOT_USERNAME = '@hkearn_trx_bot'  # Replace with your bot's username
BUTTON_TEXT = '🔗 Open Link'  # Replace with the text of the button you want to handle

client = TelegramClient('session_name', API_ID, API_HASH)

async def handle_last_message():
    await client.start()
    print("Fetching the last message...")

    messages = await client.get_messages(BOT_USERNAME, limit=1)
    if not messages:
        print("No messages found!")
        return

    last_message = messages[0]
    print(f"Last message: {last_message.text}")

    # Check if the message has buttons
    if last_message.buttons:
        print("Message has buttons.")
        for row in last_message.buttons:  # Iterate over button rows
            for button in row:  # Iterate over buttons in a row
                if button.text == BUTTON_TEXT:  # Match the button text
                    if button.url:  # Check if the button has a URL
                        print(f"Button URL found: {button.url}")
                    else:
                        print(f"Button with text '{BUTTON_TEXT}' does not have a URL.")
                    return
        print(f"No button with text '{BUTTON_TEXT}' found!")
    else:
        print("No buttons found in the message!")

async def main():
    await handle_last_message()

# Run the script
if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
