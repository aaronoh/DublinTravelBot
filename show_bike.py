import logging,requests, xmltodict, json
import nltk
import time

def getBike(bot, update, userStation):
    # url = 'https://tracker.dashbot.io/track?platform=generic&v=9.4.0-rest&type=incoming&apiKey=GNBzfWCO7HSzfsLvNqImagfhBES8d7a1ZLlQQW59'
    # url = 'https://api.botanalytics.co/v1/messages/generic/'
    # headers = {'Content-Type': 'application/json', 'Authorization': '89725dfb6c81667d4b84a22f460abe00dc61007c'}
    # data = '{"is_sender_bot": false,"user": {"id": "newTestID","name": "TestName"},"message": {"timestamp": 1517941019 ,"text": "TestMessage"}}'
    # r = requests.post(url, headers=headers, data=data)
    # print(r)


    jsonstr = requests.get(
        'https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=2eb0463a8d6feabf397cf5babdc21d4e764701a9')
    data = (jsonstr.json())
    i = 0
    stations = []
    for d in data:
        stations.append(data[i]['address'])
        i = i + 1
    text = 'Smithfield North'

    print(stations)
    for station in stations:
        if text == station:
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

    update.message.reply_text("See map below for directions to the {0} station.".format(user_station))
    # Send a map to the user - retrieve the chat id from the original function call and use the lat/lng vars set above
    bot.sendLocation(update.effective_chat.id, latitude=lat, longitude=lng, live_period=600);
