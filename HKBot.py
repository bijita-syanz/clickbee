from telethon import TelegramClient, events
from telethon.tl.functions.channels import JoinChannelRequest
from telethon import TelegramClient
from telethon.tl.functions.messages import GetBotCallbackAnswerRequest
from selenium.webdriver.common.by import By
from selenium import webdriver
import asyncio
import time
import re

API_ID = '21111033'
API_HASH = 'fda348618bf2d98a6abe132d33c9ed6e'
BOT_USERNAME = '@hkearn_trx_bot'
END_STR = "Oh no! There are NO TASKS available at the moment."
loop = asyncio.get_event_loop()

client = TelegramClient('session_name', API_ID, API_HASH)

# Print colored output for better readability
def print_colored(text, color):
    colors = {'red': '\033[31m', 'green': '\033[32m', 'reset': '\033[0m'}
    print(f"{colors.get(color, colors['reset'])}{text}{colors['reset']}")

# Function to extract links from message
def extract_link_from_message(message):
    pattern = r'(https?://t\.me/[a-zA-Z0-9_]+)'
    return re.findall(pattern, message)

# Visit site using Selenium
def visit_site(link):
    driver = webdriver.Chrome()  # Ensure ChromeDriver is installed and on PATH
    try:
        driver.get(link)
        time.sleep(5)  # Allow the page to load
        try:
            timer = driver.find_element(By.ID, "timer")
            time.sleep(int(timer.text))
        except:
            print_colored("No timer found. Closing site.", "red")
        finally:
            driver.quit()
    except Exception as e:
        print_colored(f"Error visiting site: {e}", "red")
        driver.quit()

# Join a Telegram channel
async def join_channel(channel_link):
    try:
        print(f"Joining channel: {channel_link}")
        result = await client(JoinChannelRequest(channel_link))
        print_colored(f"Joined channel: {result.chats[0].title}", "green")
    except Exception as e:
        print_colored(f"Error joining channel: {e}", "red")

# Handle Telegram bot interaction
async def send_and_receive(text):
    try:
        await client.start()
        async with client.conversation(BOT_USERNAME) as conv:
            await conv.send_message(text)
            response = await conv.get_response()
            return response.text
    except Exception as e:
        print_colored(f"Error communicating with bot: {e}", "red")

async def handle_last_message(BUTTON_TEXT):
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
                        return button.url
                    else:
                        print(f"Button with text '{BUTTON_TEXT}' does not have a URL.")
                    return False
        print(f"No button with text '{BUTTON_TEXT}' found!")
        return False
    else:
        print("No buttons found in the message!")
        return False
async def HANDEL_LINK_FROM_BUTTON(button_text):
    await handle_last_message(button_text)

async def click_button_in_last_message(BUTTON_TEXT):
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

        if last_message.buttons:
            print("Last message has buttons.")
            for row in last_message.buttons:  # Iterate over button rows
                for button in row:  # Iterate over buttons in a row
                    if button.text == BUTTON_TEXT:  # Match the button text
                        print(f"Clicking button: {button.text}")
                        response = await client(GetBotCallbackAnswerRequest(
                            peer=bot_entity.id,
                            msg_id=last_message.id,
                            data=button.data
                        ))
                        print(f"Bot response: {response.message}")
                        return
            print(f"No button with text '{BUTTON_TEXT}' found!")
        else:
            print("No buttons found in the last message!")

    except Exception as e:
        print(f"An error occurred: {e}")


# Main menu loop
def main():
    print_colored("Start the bot with the menu:", "green")
    print(" 1: Visit Sites\n 2: Join Channels\n 3: Join Bots (not implemented)\n 4: All\n 5: Settings\n 6: disply the meniu")

    # Ensure the client is connected
    if not client.is_connected():
            try :
                loop.run_until_complete(client.connect())
            except :
                print_colored("ERROR , MAYBE YOU ARE OFFLINE " , "red")            

    while True:
        choice = input("Enter a number (1-6): ")
        try:
            choice = int(choice)
        except ValueError:
            print_colored("Invalid input! Please enter a number.", "red")
            continue

        if choice == 1:  # Visit Sites
            while True:
                reply = loop.run_until_complete(send_and_receive("💻 Visit Sites"))
                if END_STR in reply:
                    print_colored("No more tasks. Sleeping for 300 seconds...", "red")
                    time.sleep(300)
                else:
                    with client:
                        url = client.loop.run_until_complete(HANDEL_LINK_FROM_BUTTON())
                    if url:
                        visit_site(url)
                        time.sleep(5)
                        print_colored("Task Completed :" , "green")
                    else:
                        print_colored("No valid link found in the reply.", "red")

        elif choice == 2:  # Join Channels
            loop.run_until_complete(send_and_receive("❇️ Earn cryptocurrency"))
            while True:
                with client :
                    client.loop.run_until_complete(click_button_in_last_message("📣 Join Chats"))
                    client.disconnect()
                """
                if END_STR in reply:
                    print_colored("No more tasks. Sleeping for 300 seconds...", "red")
                    time.sleep(300)
                else:"""
                with client:
                        try :
                            url = client.loop.run_until_complete(HANDEL_LINK_FROM_BUTTON(button_text="🔎 Go to Channel"))
                            if url != None :
                                loop.run_until_complete(join_channel(url))
                                print_colored("task completed" , "green")
                            else :
                                print_colored("error ??" , "red")
                        except Exception as excp:
                            print_colored(f"ERROR : {excp}" , "red")

        elif choice == 3:
            #comming soon 
            print_colored("Join Bots is not implemented.", "red")

        elif choice == 4:
            print_colored("All tasks option selected. Implement actions for all modes.", "red")

        elif choice == 5:
            print_colored("Settings option selected. Implement settings.", "red")

        elif choice == 6 :
            print_colored("Start the bot with the menu:", "green")
            print(" 1: Visit Sites\n 2: Join Channels\n 3: Join Bots (not implemented)\n 4: All\n 5: Settings\n 6: disply the meniu")



if __name__ == "__main__":
    main()
