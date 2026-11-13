import os
from dotenv import load_dotenv
import random
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope
from twitchAPI.helper import first


# # You need a Client ID and an OAuth token from the Twitch Developer Console
# OAUTH_TOKEN='your_oauth_access_token'  # Must include the 'moderator:read:chatters' scope
# BROADCASTER_ID='your_numeric_twitch_channel_id'
# MODERATOR_ID='your_numeric_twitch_user_id' # Usually the same as broadcaster ID if self-running

# url = "https://twitch.tv"

# 1. Load credentials securely (e.g., from environment variables)
# Never hardcode your Client Secret in your source code!
CLIENT_ID = os.getenv("CLIENT_ID", "your_client_id_here")
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "your_client_secret_here")
USERNAME = os.getenv("USERNAME", "your_client_secret_here")


#GLOBALS
twitch = None
user_id = None
token = None
refresh_token = None
# Change this value for how long you want the user to be timed out in seconds
# NEVER SET IT TO 0, THIS WILL BAN THE USER INSTEAD.
# Default is 60 seconds, 32400 is 9 hours
timeout_time = 60

#NOTE - this list is to exclude chatters you do not want timed out
blacklist = ["whosever0", "StreamElements"]
timeoutlist = []

TARGET_SCOPES = [
    AuthScope.CHAT_READ,
    AuthScope.CHAT_EDIT, 
    AuthScope.MODERATOR_MANAGE_BANNED_USERS,
    AuthScope.MODERATOR_READ_CHATTERS
    ]

async def get_twitch_user():
    
    # Fetch user data by login name. 
    # get_users returns an async generator, so we use the `first` helper to grab the first match.
    user = await first(twitch.get_users(logins=[USERNAME]))
    
    if user:
        print(f"User ID: {user.id}")
        print(f"Display Name: {user.display_name}")
        print(f"Profile Picture URL: {user.profile_image_url}")
        print(f"Broadcaster Type: {user.broadcaster_type}")
        print(f"Description: {user.description}")
    else:
        print("User not found.")
    return user.id


async def get_chatters():
    result = await twitch.get_chatters(
          broadcaster_id=user_id,
          moderator_id=user_id,  # Must be broadcaster or moderator ID
          first=1000,
    )
    return result

async def timeout_chatter(name):
    global timeout_time
    result = await twitch.ban_user(
        broadcaster_id=user_id,
        moderator_id=user_id,
        user_id=name,
        reason="Died in pikmin",
        #THIS SHOULD NEVER BE 0, 0 IS AN ACTUAL BAN
        duration=timeout_time, # timeout in seconds, default is 60, 32400 is 9 hours
    )   

async def kill_chatters(total):
    global timeoutlist
    chat = await get_chatters()
    print(chat)
    # maybe this could be done with sample, but doing black list checks would be annoying 
    #died = random.sample(chat.data, k=total)
    for i in range(0,total):
        while True:
            index = random.randint(0,chat.total - 1)
            output = "trying to kill user " + chat.data[index].user_name
            print(output)
            if (chat.data[index].user_name in blacklist) or chat.data[index].user_id in timeoutlist:
                continue
            else:
                timeoutlist.append(chat.data[index].user_id)
                await timeout_chatter(chat.data[index].user_id)
                break

async def init():
    global token
    global twitch
    global refresh_token
    global user_id
    twitch = await Twitch(CLIENT_ID, CLIENT_SECRET)
    # Initialize the local authenticator helper
    auth = UserAuthenticator(twitch, TARGET_SCOPES, force_verify=False)
    # This line automatically opens your default web browser to the Twitch login page.
    # After you click 'Authorize', it intercepts the token on your localhost port.
    token, refresh_token = await auth.authenticate()
    await twitch.set_user_authentication(token, TARGET_SCOPES, refresh_token)
    user_id = await get_twitch_user()
    chatters = await get_chatters()
    print("inital chatters check")
    print(chatters)
    print(chatters.total)
    print(chatters.data[chatters.total-1].user_name)
