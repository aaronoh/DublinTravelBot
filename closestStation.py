import logging,requests, xmltodict, json
import gpxpy.geo
import telegram


def find(bot, update):
    location_keyboard = [[telegram.KeyboardButton(text="Share Location!", request_location=True)]]
    reply_markup = telegram.ReplyKeyboardMarkup(location_keyboard)
    bot.send_message(chat_id=update.effective_chat.id,
    text = "Would you mind sharing your location with me so that I can provide you with your nearest station?",
    reply_markup = reply_markup)

def get_location(bot, update):
    print(update.message.location)
    stations = []
    # Poll api again - using the station info endpoint
    # xml -> dict -> json str -> json obj
    url = 'http://api.irishrail.ie/realtime/realtime.asmx/getAllStationsXML_WithStationType?StationType=D'
    xml = requests.get(url)
    dict = xmltodict.parse(xml.content)
    jsonstr = json.dumps(dict)
    jsonobj = json.loads(jsonstr)
    myLat = update.message.location.latitude
    myLong = update.message.location.longitude
    i = 0
    dist = []

    for attrs in jsonobj["ArrayOfObjStation"]["objStation"]:
        # add the stationdesc attribute to the string list_of_stations
        x=(attrs['StationDesc'], attrs['StationLatitude'], attrs['StationLongitude'])
        stations.append(x)
        lats = stations[i][1]
        longs = stations[i][2]
        d = gpxpy.geo.haversine_distance(myLat, myLong, float(lats), float(longs)), stations[i][0], stations[i][1], stations[i][2]
        dist.append(d)
        i += 1

    sortedDist = sorted(dist, key = lambda el: el[0])
    update.message.reply_text('Your closest station is {0}. Tap on the map below for directions.'.format(sortedDist[0][1]))
    bot.sendLocation(update.effective_chat.id, latitude=sortedDist[0][2], longitude=sortedDist[0][3], live_period=600);