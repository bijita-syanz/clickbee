from telethon import TelegramClient, events
from telethon.tl.functions.channels import JoinChannelRequest
from selenium.webdriver.common.by import By
from selenium import webdriver
import asyncio
import time
import re
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import GetBotCallbackAnswerRequest
import requests
from urllib.parse import urlparse, parse_qs


API_ID = '21111033'
API_HASH = 'fda348618bf2d98a6abe132d33c9ed6e'
BOT_USERNAME = '@ClickBeeBot'
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

def check_if_app(link):
    if "?startapp=" in link :
        #print("the link is an app link ")
        return "App"
    elif "Bot?start=" in link :
        #print("the link is a bot link") 
        return "Bot"
    else :
        print_colored("ther is an error :[ in checking the link ]" , "red")
        return None

def extract_bot_username_from_link(link):
    try:
        parsed_url = urlparse(link)
        if parsed_url.netloc != "t.me":
            raise ValueError("Invalid Telegram link")

        path_parts = parsed_url.path.strip("/").split("/")
        if len(path_parts) == 1 and path_parts[0].endswith("bot"):
            return path_parts[0]  # Return the bot username
        else:
            path_parts = parsed_url.path.strip("/").split("?")
            if len(path_parts) == 1 and path_parts[0].endswith("bot"):
                return path_parts[0]  # Return the bot username
            elif len(path_parts) == 1 and path_parts[0].endswith("App"):
                return path_parts[0]  # Return the app username
            elif len(path_parts) == 1 and path_parts[0].endswith("Bot"):
                return path_parts[0]  # Return the app username
            else:
                    start_index = link.find("t.me/") + len("t.me/")
                    end_index = link.find("/app")
                    if start_index != -1 and end_index != -1:
                        return link[start_index:end_index]
            raise ValueError("Link does not point to a bot")
    except Exception as e:
        print(f"Error extracting bot username: {link}")
        return None
    
def extract_bot_link(app_link):
    try:
        parsed_url = urlparse(app_link)
        if parsed_url.netloc != "t.me":
            raise ValueError("Invalid Telegram link")

        bot_username = parsed_url.path.strip("/")
        query_params = parse_qs(parsed_url.query)
        start_param = query_params.get("start", [None])[0]

        if bot_username and start_param:
            bot_link = f"https://t.me/{bot_username}?start={start_param}"
            return bot_link
        else:
            raise ValueError("Bot username or parameters are missing")
    except Exception as e:
        print(f"Error extracting bot link: {e}")
        return None
    

def check_link_type(link):
    try:
        if "?startapp=" in link :
            #print("the link is an app link ")
            return "App"
        elif "Bot?start=" in link or "BOT?start" in link :
            #print("the link is a bot link") 
            return "Bot"
        else :
            print_colored("ther is an error :[ in checking the link ]" , "red")
            return None
    except Exception as e:
        print_colored(f"Error checking link type: {e}", "red")
        return None
    


# Visit site using Selenium
def visit_site(link):
    driver = webdriver.Chrome()  # Ensure ChromeDriver is installed and on PATH
    try:
        driver.get(link)
        time.sleep(5)  # Allow the page to load
        try:
            timer = driver.find_element(By.ID, "timer")
            if timer:
                time.sleep(32)
        except:
            print_colored("No timer found. Closing site.", "red")
            time.sleep(3)
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
async def send_and_receive(text , BOT_USERNAME):
    try:
        await client.start()
        async with client.conversation(BOT_USERNAME) as conv:
            await conv.send_message(text)
            response = await conv.get_response()
            return response.text
    except Exception as e:
        print_colored(f"Error communicating with bot: {e}", "red")

async def start_a_bot(bot_username):
    try:
        async with client.conversation(bot_username) as conv:
            await conv.send_message("/start")
            print("BOT STARTED SUCCESSFULLY")
            response = await conv.get_response()
            return response.text
    except Exception as e:
        print(f"Error communicating with bot: {e}")



async def forward_last_message(bot_username, target_chat):
    try:
        async with client:
            # Get the last message from the bot
            messages = await client.get_messages(bot_username, limit=1)
            if messages:
                last_message = messages[0]
                await client.forward_messages(target_chat, last_message)
                print(f"Successfully forwarded the last message from {bot_username} to {target_chat}")
            else:
                print(f"No messages found for bot {bot_username}")
    except Exception as e:
        print(f"Error forwarding message: {e}")


async def HANDEL_LINK_FROM_BUTTON(BUTTON_TEXT):
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
                        print_colored(f"Button URL found: {button.url}" , "green")
                        return button.url
                    else:
                        print(f"Button with text '{BUTTON_TEXT}' does not have a URL.")
                    return False
        print(f"No button with text '{BUTTON_TEXT}' found!")
        return False
    else:
        print("No buttons found in the message!")
        return False


async def click_button_in_last_message(BUTTON_TEXT ):
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

async def click_button_in_last_message_for_post(BUTTON_TEXT ):
    try:
        # Start the client
        await client.start()

        print(f"Fetching the last message from {BOT_USERNAME}...")
        # Get the bot's entity
        bot_entity = await client.get_entity(BOT_USERNAME)

        # Fetch the last message from the bot's chat
        last_messages = await client.get_messages(bot_entity, limit=2)

        if not last_messages:
            print("No messages found in the bot's chat!")
            return

        last_messages
        for last_message in last_messages :
            if last_message.buttons:
                print("Last message has buttons.")
                for row in last_message.buttons:  # Iterate over button rows
                    for button in row:  # Iterate over buttons in a row
                        if button.text == BUTTON_TEXT:  # Match the button text
                            print_colored(f"Clicking button: {button.text}" , "green")
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
def main(choise):
    print_colored("Start the bot with the menu:", "green")
    print(" 1: Visit Sites\n 2: Join Channels\n 3: Join Bots (not implemented)\n 4: View Post\n 5: All\n 6: Settings\n 7: disply the meniu")

    # Ensure the client is connected
    if not client.is_connected():
            try :
                loop.run_until_complete(client.connect())
            except :
                print_colored("ERROR , MAYBE YOU ARE OFFLINE " , "red")            

    while True:
        if choise == 0 :
            choice = input("Enter a number (1-7): ")
        elif choise > 0 :
            choice = choise
        try:
            choice = int(choice)
        except ValueError:
            print_colored("Invalid input! Please enter a number.", "red")
            continue

        if choice == 1:  # Visit Sites
            while True:
                reply = loop.run_until_complete(send_and_receive("💻 Visit Sites" , BOT_USERNAME))
                if END_STR in reply:
                    print_colored("No more [💻 Visit Sites] tasks. Sleeping for 300 seconds...", "red")
                    time.sleep(5)
                else:
                    with client:
                        url = client.loop.run_until_complete(HANDEL_LINK_FROM_BUTTON("🌐 Open Link 🌐"))
                    if url:
                        visit_site(url)
                        time.sleep(5)
                        print_colored("Task Completed :" , "green")
                    else:
                        print_colored("No valid link found in the reply.", "red")

        elif choice == 2:  # Join Channels
            while True:
                reply = loop.run_until_complete(send_and_receive("📢 Join Channels" , BOT_USERNAME))
                if END_STR in reply:
                    print_colored("No more [📢 Join Channels] tasks. Sleeping for 300 seconds...", "red")
                    time.sleep(5)
                else:
                    with client:
                        try :
                            url = client.loop.run_until_complete(HANDEL_LINK_FROM_BUTTON("👁 Join the Channel 👁"))
                            time.sleep(0.25)
                            loop.run_until_complete(join_channel(url))
                            time.sleep(0.25)
                            loop.run_until_complete(click_button_in_last_message("✅Joined"))
                            print_colored("task completed !" , "green")

                        except Exception as excp:
                            print_colored(f"ERROR : {excp}" , "red")

        elif choice == 3:
            pass
            while True:
                reply = loop.run_until_complete(send_and_receive("🤖 Join Bots" , BOT_USERNAME))
                if END_STR in reply:
                    print_colored("No more [🤖 Join Bots] tasks. Sleeping for 300 seconds...", "red")
                    time.sleep(5)
                else:
                    with client:
                        try :
                            url = client.loop.run_until_complete(HANDEL_LINK_FROM_BUTTON("🤖 Start the Bot 🤖"))
                            time.sleep(0.25)
                            link_type = check_link_type(url)
                            print(link_type)
                            if link_type == 'App' :
                                try :
                                    launch_app(url)
                                    time.sleep(0.25)
                                    bot_username = extract_bot_username_from_link(url)
                                    if bot_username :
                                       print_colored('LINK EXTRACTED SECCESFULY' , "green")
                                       loop.run_until_complete(send_and_receive("/start", bot_username))
                                       loop.run_until_complete(click_button_in_last_message("✅ Started"))
                                       loop.run_until_complete(forward_last_message(bot_username=bot_username , target_chat=BOT_USERNAME))
                                except Exception as exception:
                                    print_colored(exception , "red")
                                    break
                            elif link_type == "Bot" :
                                try :
                                    bot_username = extract_bot_username_from_link(url)
                                    loop.run_until_complete(send_and_receive("/start",bot_username))
                                    loop.run_until_complete(click_button_in_last_message("✅ Started"))
                                    loop.run_until_complete(forward_last_message(bot_username=bot_username , target_chat=BOT_USERNAME))
                                except Exception as exception:
                                    print_colored(exception , "green")
                                time.sleep(1)
                            else:
                                break
                        except Exception as excp:
                            print_colored(f"ERROR : {excp}" , "red")
        elif choice == 4:
            loop.run_until_complete(send_and_receive("/start" , BOT_USERNAME))
            loop.run_until_complete(send_and_receive("🤩 More" , BOT_USERNAME))
            while True:
                reply = loop.run_until_complete(send_and_receive("📄 View Posts" , BOT_USERNAME))
                if END_STR in reply:
                    print_colored("No more [📄 View Posts] tasks. Sleeping for 50 seconds...", "red")
                    time.sleep(5)
                else:
                    time.sleep(15)
                    loop.run_until_complete(click_button_in_last_message_for_post("✅ Watched"))


#=================================all============================================
        elif choice == 5:
            print_colored("All tasks STARTed.", "green")
            while True:
                reply = loop.run_until_complete(send_and_receive("💻 Visit Sites" , BOT_USERNAME))
                if END_STR in reply:
                    print_colored("No more [💻 Visit Sites] tasks. Sleeping for 300 seconds...", "red")
                    time.sleep(5)
                else:
                    with client:
                        url = client.loop.run_until_complete(HANDEL_LINK_FROM_BUTTON("🌐 Open Link 🌐"))
                    if url:
                        visit_site(url)
                        time.sleep(5)
                        print_colored("Task Completed :" , "green")
                    else:
                        print_colored("No valid link found in the reply.", "red")


                reply = loop.run_until_complete(send_and_receive("📢 Join Channels" , BOT_USERNAME))
                if END_STR in reply:
                    print_colored("No more [📢 Join Channels] tasks. Sleeping for 300 seconds...", "red")
                    time.sleep(5)
                else:
                    with client:
                        try :
                            url = client.loop.run_until_complete(HANDEL_LINK_FROM_BUTTON("👁 Join the Channel 👁"))
                            time.sleep(0.25)
                            loop.run_until_complete(join_channel(url))
                            time.sleep(0.25)
                            loop.run_until_complete(click_button_in_last_message("✅Joined"))
                            print_colored("task completed !" , "green")

                        except Exception as excp:
                            print_colored(f"ERROR : {excp}" , "red")
                time.sleep(5)
                reply = loop.run_until_complete(send_and_receive("🤖 Join Bots" , BOT_USERNAME))
                if END_STR in reply:
                    print_colored("No more [🤖 Join Bots] tasks. Sleeping for 300 seconds...", "red")
                    time.sleep(5)
                else:
                    with client:
                        try :
                            url = client.loop.run_until_complete(HANDEL_LINK_FROM_BUTTON("🤖 Start the Bot 🤖"))
                            time.sleep(0.25)
                            link_type = check_link_type(url)
                            print(link_type)
                            if link_type == 'App' :
                                print_colored("the link is [APP]" , "green")
                                try :
                                    launch_app(url)
                                    time.sleep(0.25)
                                    bot_username = extract_bot_username_from_link(url)
                                    if bot_username :
                                       print_colored('username  EXTRACTED SECCESFULY' , "green")
                                       loop.run_until_complete(send_and_receive("/start", bot_username))
                                       loop.run_until_complete(click_button_in_last_message("✅ Started"))
                                       loop.run_until_complete(forward_last_message(bot_username=bot_username , target_chat=BOT_USERNAME))
                                except Exception as exception:
                                    print_colored(exception , "red")
                                    break
                            elif link_type == "Bot" :
                                print_colored("the link is [BOT]" , "green")
                                try :
                                    bot_username = extract_bot_username_from_link(url)
                                    loop.run_until_complete(send_and_receive("/start",bot_username))
                                    loop.run_until_complete(click_button_in_last_message("✅ Started"))
                                    loop.run_until_complete(forward_last_message(bot_username=bot_username , target_chat=BOT_USERNAME))
                                except Exception as exception:
                                    print_colored(exception , "red")
                                time.sleep(0.1)
                            else:
                                break
                        except Exception as excp:
                            print_colored(f"ERROR : {excp}" , "red")
                time.sleep(0.2)
                loop.run_until_complete(send_and_receive("/start" , BOT_USERNAME))
                loop.run_until_complete(send_and_receive("🤩 More" , BOT_USERNAME))
                reply = loop.run_until_complete(send_and_receive("📄 View Posts" , BOT_USERNAME))
                if END_STR in reply:
                    print_colored("No more [📄 View Posts] tasks. Sleeping for 50 seconds...", "red")
                    time.sleep(5)
                else:
                    time.sleep(15)
                    loop.run_until_complete(click_button_in_last_message_for_post("✅ Watched"))

        elif choice == 6:
            print_colored("Settings option selected. Implement settings.", "red")

        elif choice == 7 :
            print_colored("Start the bot with the menu:", "green")
            print(" 1: Visit Sites\n 2: Join Channels\n 3: Join Bots (not implemented)\n 4: View Post\n 5: All\n 6: Settings\n 7: disply the meniu")


def import_data(data_file):


    pass
    
if __name__ == "__main__" :
    main(0)
