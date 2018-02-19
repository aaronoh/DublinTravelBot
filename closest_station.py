import logging,requests, xmltodict, json
import gpxpy.geo
import telegram


def find(bot, update):
    button_keyboard = [[telegram.KeyboardButton(text="Dart Station!", request_location=True)],[telegram.KeyboardButton(text="Bike Station!", request_location=True)]]

    reply_markup = telegram.ReplyKeyboardMarkup(button_keyboard, one_time_keyboard=True)
    bot.send_message(chat_id=update.effective_chat.id,
    text = "Would you mind sharing your location with me so that I can provide you with your nearest station?",
    reply_markup = reply_markup)


def station_type(bot, update):
    #just need to figure out how to get long/lat from s_t to PrintIT
    myLat = update.message.location.latitude
    myLong = update.message.location.longitude

    keyboard = [[telegram.InlineKeyboardButton("Dart Station", callback_data='dart'),
                 telegram.InlineKeyboardButton("Bike Station", callback_data='bike')]]

    reply_markup = telegram.InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Which tupe of station are you looking for?', reply_markup=reply_markup)

    print(myLat, myLong)

def printIt(bot, update):
    query = update.callback_query
    print(query.data)
    myLat = update.message.location.latitude
    myLong = update.message.location.longitude
    print(myLat,myLong)

def get_location(bot, update):
    isTrain = 'false';
    isBike = 'true'

    print(update.message.location)
    stations = []
    i = 0
    dist = []

    myLat = update.message.location.latitude
    myLong = update.message.location.longitude

    # Poll api again - using the station info endpoint
    # xml -> dict -> json str -> json obj
    if isTrain:
        print('hcfxhjghjfghjgfhjgfhjgfhgjf')
        url = 'http://api.irishrail.ie/realtime/realtime.asmx/getAllStationsXML_WithStationType?StationType=D'
        xml = requests.get(url)
        dict = xmltodict.parse(xml.content)
        jsonstr = json.dumps(dict)
        jsonobj = json.loads(jsonstr)

        for attrs in jsonobj["ArrayOfObjStation"]["objStation"]:
            # add the stationdesc attribute to the string list_of_stations
            x = (attrs['StationDesc'], attrs['StationLatitude'], attrs['StationLongitude'])
            stations.append(x)
            lats = stations[i][1]
            longs = stations[i][2]
            d = gpxpy.geo.haversine_distance(myLat, myLong, float(lats), float(longs)), stations[i][0], stations[i][1], \
                stations[i][2]
            dist.append(d)
            i += 1

    if isBike:
        jsonstr = requests.get('https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=2eb0463a8d6feabf397cf5babdc21d4e764701a9')
        jsonobj = (jsonstr.json())

        for attrs in jsonobj:
            x = (attrs['address'],attrs['position']['lat'],attrs['position']['lng'])
            stations.append(x)
            lats = stations[i][1]
            longs = stations[i][2]
            d = gpxpy.geo.haversine_distance(myLat, myLong, float(lats), float(longs)), stations[i][0], stations[i][1], \
                stations[i][2]
            dist.append(d)
            i += 1





    sortedDist = sorted(dist, key = lambda el: el[0])
    update.message.reply_text('Your closest station is {0}. Tap on the map below for directions.'.format(sortedDist[0][1]))
    bot.sendLocation(update.effective_chat.id, latitude=sortedDist[0][2], longitude=sortedDist[0][3], live_period=600);