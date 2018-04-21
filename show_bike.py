import logging,requests, xmltodict, json
import nltk
import time

def showBike(bot, update, userStation):
    url = 'https://tracker.dashbot.io/track?platform=generic&v=9.4.0-rest&type=incoming&apiKey=GNBzfWCO7HSzfsLvNqImagfhBES8d7a1ZLlQQW59'
    headers = {'Content-Type': 'application/json'}
    analytics = '{{"text": "{2}", "userId": "{0}", "platformJson":{{"userName": "{1}","Action": "Show bike station"}}}}'.format(
        update.effective_chat.id, update.message.from_user.username, update.message.text)
    requests.post(url, headers=headers, data=analytics)


    jsonstr = requests.get(
        'https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=2eb0463a8d6feabf397cf5babdc21d4e764701a9')
    data = (jsonstr.json())
    i = 0
    stations = []
    for d in data:
        stations.append(data[i]['address'])
        i = i + 1

    print(stations)
    for station in stations:
        if userStation == station:
            user_station = station
            # for word in text:
            #     dir_diff = nltk.edit_distance(word.lower(), station.lower())
            #     if dir_diff < 4:
            #         user_station = station

    print(user_station)
    print(data)
    for d in data:
        if d['address'] == user_station:
            lat = (d['position']['lat'])
            lng = (d['position']['lng'])

    print(lat,lng)

    msg = "See map below for directions to the {0} station.".format(user_station)
    update.message.reply_text(msg)
    # Send a map to the user - retrieve the chat id from the original function call and use the lat/lng vars set above
    bot.sendLocation(update.effective_chat.id, latitude=lat, longitude=lng, live_period=600);

    url = 'https://tracker.dashbot.io/track?platform=generic&v=9.4.0-rest&type=outgoing&apiKey=GNBzfWCO7HSzfsLvNqImagfhBES8d7a1ZLlQQW59'
    headers = {'Content-Type': 'application/json'}
    analytics = '{{"text": "{0}", "userId": "DublinTravelBot", "platformJson":{{"userName": "DublinTravelBot",' \
                '"Action": "Show bike station"}}}}'.format(msg)
    requests.post(url, headers=headers, data=analytics)
