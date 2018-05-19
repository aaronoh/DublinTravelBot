import logging,requests, xmltodict, json
import nltk
import time
import telegram

def determine_direction(bot, update, userStation):

    N = 'Northbound {0}'.format(userStation)
    S = 'Southbound {0}'.format(userStation)
    keyboard = [[telegram.InlineKeyboardButton("Northbound", callback_data=N ),
                 telegram.InlineKeyboardButton("Southbound", callback_data=S)]]

    reply_markup = telegram.InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Please specify the direction of travel', reply_markup=reply_markup)

def callback_direction(bot, update):
    query = update.callback_query
    data = query.data.split()
    print(data)

def getTrain(bot, update, userStation):
    directions =['north','south','northbound','southbound','n','s']
    user_d =''
    text = update.message.text.split()
    for direction in directions:
        for word in text:
            dir_diff = nltk.edit_distance(word.lower(), direction)
            if dir_diff == 0:
                user_d = direction.lower()

    if not user_d:
        determine_direction(bot, update, userStation)
        return

    elif user_d in ('north','northbound','n','nth'):
        direction = 'Northbound'

    elif user_d in ('south', 'southbound', 's', 'sth'):
        direction = 'Southbound'

    fetch_train(bot, update, userStation,direction)

def fetch_train(bot, update, userStation,direction):
    apiurl = 'http://api.irishrail.ie/realtime/realtime.asmx/getStationDataByNameXML?StationDesc={0}'.format(
        userStation)
    # xml -> dict -> json str -> json obj
    xml = requests.get(apiurl)
    dict = xmltodict.parse(xml.content)
    jsonstr = json.dumps(dict)
    jsonobj = json.loads(jsonstr)
    print(apiurl, direction)
    print('sdfoksdlf',update)
    url = 'https://tracker.dashbot.io/track?platform=generic&v=9.4.0-rest&type=incoming&apiKey=GNBzfWCO7HSzfsLvNqImagfhBES8d7a1ZLlQQW59'
    headers = {'Content-Type': 'application/json'}
    analytics = '{{"text": "Direction: {1} Station: {2} ", "userId": "{0}", "platformJson":{{Action": "Fetch Train"}}}}'.format(update.effective_chat.id, direction, userStation)
    requests.post(url, headers=headers, data=analytics)
    # global array, set to empty at each call (new search)
    global trains
    trains = []
    if jsonobj == {'ArrayOfObjStationData': {'@xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance', '@xmlns': 'http://api.irishrail.ie/realtime/', '@xmlns:xsd': 'http://www.w3.org/2001/XMLSchema'}}:
        bot.send_message(chat_id=update.effective_chat.id, text='There are no trains currently running. Please check the IrishRail website for service disruptions. http://www.irishrail.ie/')
        return
    try:
        # For every object in the json obj
        for attrs in jsonobj["ArrayOfObjStationData"]["objStationData"]:
            # if the direction matches the requested direction
            print(attrs)
            if attrs['Direction'] == direction:
                # add the trains to an array
                trains.append(attrs)

        if not trains:
            print(trains)
            bot.send_message(chat_id=update.effective_chat.id, text=
            "There are no trains travelling {0} due at the {1} station within the next 90 minutes, or the {1} station cannot be found. Please try again later. ".format(
                direction, userStation))
            return;

        # Pull out specific elements of the first element in the array -
        #  reworked to use this array to allow the user to search for additional trains servicing the same station
        # e.g Train due in 2 mins, user may be more interested in the next train - Show them [1] instead of [0]
        dueIn = (trains[0]['Duein'])
        stationName = (trains[0]["Stationfullname"])
        destination = (trains[0]["Destination"])

        dir = (trains[0]["Direction"])

        print(dueIn,stationName,destination,dir)
        # Return worthwhile string to user
        msg = "The next {0} train to service the {1} station is heading for {2}, it's due in {3} minutes.".format(
                dir, stationName, destination, dueIn)
        bot.send_message(chat_id=update.effective_chat.id, text=msg)

        url = 'https://tracker.dashbot.io/track?platform=generic&v=9.4.0-rest&type=outgoing&apiKey=GNBzfWCO7HSzfsLvNqImagfhBES8d7a1ZLlQQW59'
        headers = {'Content-Type': 'application/json'}
        analytics = '{{"text": "{0}", "userId": "DublinTravelBot", "platformJson":{{"userName": "DublinTravelBot","Action": "Fetch train Reply"}}}}'.format(
            msg)
        requests.post(url, headers=headers, data=analytics)


        # Setting global var station name to the name of the station just searched for
        global myDirection
        myDirection = dir
        myStation = (jsonobj["ArrayOfObjStationData"]["objStationData"][0]["Stationfullname"])
        print(userStation)
        print(myStation)
        print(myDirection)


    except:
        print(jsonobj)
        print(myStation)
        bot.send_message(chat_id=update.effective_chat.id, text=
            "Sorry! I couldn't identify the station you're looking for. Please try again, use /list if you're unsure of the station name.")
        return;
