import asyncio
from telethon import TelegramClient
from telethon.tl.functions.messages import GetBotCallbackAnswerRequest

API_ID = '21111033'
API_HASH = 'fda348618bf2d98a6abe132d33c9ed6e'
BOT_USERNAME = '@hkearn_trx_bot'  # Replace with your bot's username
BUTTON_TEXT = '🔎 Go to Channel'   # Replace with the text of the button you want to click

client = TelegramClient('session_name', API_ID, API_HASH)

async def click_button_in_forwarded_message():
    try:
        # Start the client
        await client.start()

        print(f"Fetching the last message from {BOT_USERNAME}...")
        # Get the bot's entity
        bot_entity = await client.get_entity(BOT_USERNAME)

        # Fetch the last message from the bot's chat
        last_message = await client.get_messages(bot_entity, limit=1)

        if not last_message:
            print("No messages found in the bot's chat!")
            return

        last_message = last_message[0]

        # Check if the last message is forwarded and has buttons
        if last_message.fwd_from and last_message.buttons:
            print("Last message is forwarded and has buttons.")
            for row in last_message.buttons:  # Iterate over button rows
                for button in row:  # Iterate over buttons in a row
                    if button.text == BUTTON_TEXT:  # Match the button text
                        print(f"Clicking button: {button.text}")
                        response = await client(GetBotCallbackAnswerRequest(
                            peer=bot_entity.id,  # Use bot chat as peer
                            msg_id=last_message.id,  # Message ID of the forwarded message
                            data=button.data
                        ))
                        print(f"Bot response: {response.message}")
                        return
            print(f"No button with text '{BUTTON_TEXT}' found!")
        else:
            print("Last message is not forwarded or has no buttons!")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(click_button_in_forwarded_message())
