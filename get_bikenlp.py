import logging,requests, xmltodict, json
import nltk

def getBikeNLP(bot, update,user_station):
    url = 'https://tracker.dashbot.io/track?platform=generic&v=9.4.0-rest&type=incoming&apiKey=GNBzfWCO7HSzfsLvNqImagfhBES8d7a1ZLlQQW59'
    # url = 'https://api.botanalytics.co/v1/messages/generic/'
    headers = {'Content-Type': 'application/json'}
    data = '{"userId": "newTestID","name": "TestName"},"message": {"timestamp": 1517941019 ,"text": "TestMessage"}}'
    analytics = '{{"text": "{2}", "userId": "{0}", "platformJson":{{"userName": "{1}","conversationId": "qwerty","timestamp": 1517941019}}}}'.format(update.effective_chat.id, update.message.from_user.username,update.message.text)
    print(analytics)
    r = requests.post(url, headers=headers, data=analytics)
    print(r)


    jsonstr = requests.get(
        'https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=2eb0463a8d6feabf397cf5babdc21d4e764701a9')
    data = (jsonstr.json())
    i = 0
    stations = []
    for d in data:
        stations.append(data[i]['address'])
        i = i +1


    for d in data:
        if d['address'] == user_station:
            avail_bikes = (d['available_bikes'])
            avail_slots = (d['available_bike_stands'])


    print(avail_bikes,avail_slots)

    update.message.reply_text("There are currently {0} bikes and {1} stands available at the {2} bike station.".format(avail_bikes, avail_slots, user_station))
