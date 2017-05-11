#!/usr/bin/python3
import json
import time
import re
import requests




def message_matches(user_id, message_text):
    '''
    Check if the username and the word 'bot' appears in the text
    '''
    regex_expression = '.*@' + user_id + '.*bot.*'
    regex = re.compile(regex_expression)
    # Check if the message text matches the regex above
    match = regex.match(message_text)
    # returns true if the match is not None (ie the regex had a match)
    return match != None 


# In[ ]:

def extract_date(message_text):
    '''
    Extract the date.
    '''
    regex_expression = 'How many ebola deaths occurred on ([0-9]{4}\-[0-9]{2}\-[0-9]{2})'
    regex= re.compile(regex_expression)
    matches = regex.finditer(message_text)
    for match in matches:
        return match.group(1)
    
    # if there were no matches, return None
    return None


# In[ ]:

from datetime import date, datetime, timedelta
def get_ebola_data(user_date):

    data = requests.get("https://ebola-outbreak.p.mashape.com/cases",
      headers={
        "X-Mashape-Key": "5wOSqCitXnmshZqducSXXSpnMgA0p1SQfb8jsnticr7ef6tPYu"
      }
    )
    
    data = data.text
    data = json.loads(data)
    date_user = datetime.striptime(user_date,'%Y-%m-%d')
    
    for entry in data:
        cases = entry['cases']

        date_split = entry['date'][0:10]

        date = datetime.strptime(date_split, 
                             '%Y-%m-%d')



        deaths = entry['deaths']

        if date == date_user:
            response = deaths
    
        else:
            response = 0
    
    
    return response


# In[ ]:

def create_message(username,deaths):

    if deaths != 0:
       
        message = "Bad news @{u},there were {d} deaths on this day.\n".format(u=username, d=deaths)

    else:
        message = "Good news @{u},either you entered an invalid date or no deaths occured on this day!\n".format(u=username)
        
    return message

# Read the access token from the file
secrets_file = 'slack_secret.json'
f = open(secrets_file, 'r') 
content = f.read()
f.close()

auth_info = json.loads(content)
auth_token = auth_info["access_token"]
bot_user_id = auth_info["user_id"]

from slackclient import SlackClient
sc = SlackClient(auth_token)

# Connect to the Real Time Messaging API of Slack and process the events

if sc.rtm_connect():
    # We are going to be polling the Slack API for recent events continuously
    while True:
        # We are going to wait 1 second between monitoring attempts
        time.sleep(1)
        # If there are any new events, we will get a response. If there are no events, the response will be empty
        response = sc.rtm_read()
        for item in response:
            # Check that the event is a message. If not, ignore and proceed to the next event.
            if item.get("type") != 'message':
                continue
                
            # Check that the message comes from a user. If not, ignore and proceed to the next event.
            if item.get("user") == None:
                continue
            
            user_id = auth_info["user_id"]
            # Check that the message is asking the bot to do something. If not, ignore and proceed to the next event.
            message_text = item.get('text')
            if not message_matches(user_id, message_text):
                continue
                
            # Get the username of the user who asked the question
            response = sc.api_call("users.info", user=item["user"])
            username = response['user'].get('name')
            
            # Extract the station name from the user's message
            date = extract_date(message_text)

            # Prepare the message that we will send back to the user
            message = create_message(username,get_ebola_data(date))

            # Post a response to the #bots channel
            sc.api_call("chat.postMessage", channel="#bots", text=message)


