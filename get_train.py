import logging,requests, xmltodict, json
import nltk
import time

def getTrain(bot, update):
    url = 'https://tracker.dashbot.io/track?platform=generic&v=9.4.0-rest&type=incoming&apiKey=GNBzfWCO7HSzfsLvNqImagfhBES8d7a1ZLlQQW59'
    url = 'https://api.botanalytics.co/v1/messages/generic/'
    headers = {'Content-Type': 'application/json', 'Authorization': '89725dfb6c81667d4b84a22f460abe00dc61007c'}
    data = '{"is_sender_bot": false,"user": {"id": "newTestID","name": "TestName"},"message": {"timestamp": 1517941019 ,"text": "TestMessage"}}'
    r = requests.post(url, headers=headers, data=data)
    print(r)
    print('done')

    stations = ['malahide', 'portmarnock', 'clongriffin', 'sutton', 'bayside', 'howth junction', 'howth',
                'kilbarrack', 'raheny', 'harmonstown', 'killester', 'clontarf road', 'dublin connolly',
                'tara street', 'dublin pearse', 'grand canal dock', 'lansdowne road', 'sandymount', 'sydney parade',
                'booterstown', 'blackrock', 'seapoint', 'salthill', 'dun laoghaire',
                'sandycove', 'glenageary', 'dalkey', 'killiney', 'shankill', 'bray', 'greystones', 'kilcoole']

    directions =['north','south','northbound','southbound','n','s']

    text = update.message.text.split()

    for direction in directions:
        for word in text:
            dir_diff = nltk.edit_distance(word.lower(), direction)
            if dir_diff == 0:
                user_d = direction.lower()

    if user_d in ('north','northbound','n','nth'):
        direction = 'Northbound'

    elif user_d in ('south', 'southbound', 's', 'sth'):
        direction = 'Southbound'


    for station in stations:
        # print(test[3])
        for word in text:
            diff = nltk.edit_distance(word, station)
            if diff < 2:
                print('Original: {0}  New: {1}'.format(text, station))
                myStation = station

                url = 'http://api.irishrail.ie/realtime/realtime.asmx/getStationDataByNameXML?StationDesc={0}'.format(
                    myStation)
                # xml -> dict -> json str -> json obj
                xml = requests.get(url)
                dict = xmltodict.parse(xml.content)
                jsonstr = json.dumps(dict)
                jsonobj = json.loads(jsonstr)

                # global array, set to empty at each call (new search)
                global trains
                trains = []

                try:
                    # For every object in the json obj
                    for attrs in jsonobj["ArrayOfObjStationData"]["objStationData"]:
                        # if the direction matches the requested direction
                        print(attrs)
                        if attrs['Direction'] == direction:
                            # add the trains to an array
                            trains.append(attrs)

                    # Pull out specific elements of the first element in the array - reqorked to use this array to allow the user to search for additional trains servicing the same station
                    # e.g Train due in 2 mins, user may be more interested in the next train - Show them [1] instead of [0]
                    dueIn = (trains[0]['Duein'])
                    stationName = (trains[0]["Stationfullname"])
                    destination = (trains[0]["Destination"])
                    dir = (trains[0]["Direction"])

                    # Return worthwhile string to user
                    update.message.reply_text(
                        "The next {0} train to service the {1} station is heading for {2}, it's due in {3} minutes.".format(
                            dir, stationName, destination, dueIn))

                    # Setting global var station name to the name of the station just searched for
                    global myDirection
                    myDirection = dir
                    myStation = (jsonobj["ArrayOfObjStationData"]["objStationData"][1]["Stationfullname"])

                    # Yes? No? MAybe? I don't know - test when stations closed
                    if not trains:
                        print(trains)
                        update.message.reply_text(
                            "There are no trains travelling {0} due at the {1} station within the next 90 minutes, or the {1} station cannot be found. Please try again later. ".format(
                                direction, myStation))
                        return;


                except:
                    update.message.reply_text(
                        "There are no trains travelling {0} due at the {1} station within the next 90 minutes, or the {1} station cannot be found. Please try again later. ".format(
                            direction, myStation))
                    return;
