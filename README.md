# **Pikmin Death Tracker**\
\
## **What is this\
\
## **Setup:**\
\
### **Python Setup:**\
\
This written for Python 3.13.15, found here: https://www.python.org/downloads/release/python-3130/ \
After cloning the repo, setup the venv by doing the following in the repo in vscode terminal, command line(cmd), or powershell(ps) if you are evil: \
`python -m venv .venv` \
cmd command: `.venv\Scripts\activate.bat`  ps command: `.venv\Scripts\Activate.ps1` \
At this point a (.venv) should be seen to the far left of the terminal \
run this command to install all the packages \
`pip install -r requirements.txt` \
\
\
### **Twitch Setup:** \
\
Go to https://dev.twitch.tv/console \
Make an application by doing "Register Your Application" \
Name it whatever you would like. \
For the OAuth Redirect URLs we are using http://localhost:17563 so add that as a URL. \
Note: This was chosen by TwitchAPI python library to spin up a simple webservice so we can get permissions to use Twitch APIs. \
Category can be anything, I went with Game Integration \
Client Type is Confidential \
Once that is all filled out, hit "Create" \
Go back into your application and grab the Client ID and the Client Secret. \
**NOTE**: DO NOT SHOW/LEAK THE CLIENT SECRET. If you think it has been leaked, make a new one. \
\
\
### **.env Setup:** \
\
Once you have everything else setup, you need to take the Client ID, Client Secret, and your username(the name that appears in your url i.e twitch.tv/whosever0 so put whosever0) and put them inside of the .env Setup file. \
If the file is missing it should look like this at the root of the project and be called `.env`.\
\
CLIENT_ID='YOUR_ID_HERE'\
CLIENT_SECRET='YOUR_SECRET_HERE'\
USERNAME='YOUR_USERNAME_HERE'\
\
## **How to Run** \
Just do: \
\
`python dolphintracking.py`\
\
Note: On start a website will popup asking if you want to allow the application to connect to twitch.  You should only need to allow it once. If you want that authorization gone after you are done using it you can always go to Twitch Settings->Connections and at the very bottom there is Other Connections, you can remove access from there. It should be named whatever you named the application.
