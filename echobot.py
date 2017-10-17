import json
import requests
import time
import telegram


#API Key & URL construction
TOKEN = "460295615:AAEUzHYLg9s1f6YNr1Ng2s5dKMv27lZZcWE"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

#gets contents of url
def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

#adds getUpdates to url and accesses it - returns list of messages sent to bot
def get_updates():
    url = URL + "getUpdates"
    js = get_json_from_url(url)
    return js

#get chat id and message text from most recent messgae - tuple
def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)

#sends message matching parameters passed in
def send_message(text, chat_id):
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

def main():
    last_textchat = (None, None)
    while True:
        #get message, send message
        text, chat = get_last_chat_id_and_text(get_updates())
        #if text & chat aren't = to current value (either empty or last message sent), send message. Wait .5 seconds. Repeat.
        if(text, chat) != last_textchat:
            send_message(text, chat)
            last_textchat = (text, chat)
        time.sleep(0.5)

if __name__ == '__main__':
    main()