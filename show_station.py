import logging,requests, xmltodict, json
import nltk

# button_keyboard = [[telegram.KeyboardButton(text="Dart Station", request_location=True)],
#                    [telegram.KeyboardButton(text="Bike Station", request_location=True)]]
#
# reply_markup = telegram.ReplyKeyboardMarkup(button_keyboard, one_time_keyboard=True)
# bot.send_message(chat_id=update.effective_chat.id,
#                  text="Would you mind sharing your location with me so that I can provide you with your nearest station?",
#                  reply_markup=reply_markup)
def showStation(bot, update,userStation):

    # Poll api again - using the station info endpoint as this is the only way of getting their lat/long
    # xml -> dict -> json str -> json obj
    url = 'http://api.irishrail.ie/realtime/realtime.asmx/getAllStationsXML_WithStationType?StationType=D'
    xml = requests.get(url)
    dict = xmltodict.parse(xml.content)
    jsonstr = json.dumps(dict)
    jsonobj = json.loads(jsonstr)

    found=''

    # For every object in the json obj
    for attrs in jsonobj["ArrayOfObjStation"]["objStation"]:
        # if the station name attribute matches the global var station name
        if attrs['StationDesc'] == userStation.title():
            found = 'true'
            # lat/long vars = the lat/long attributes associated with that object
            lat = attrs['StationLatitude']
            long = attrs['StationLongitude']
            # Once its' matched one, break out of the for loop
            break
        else:
            print(userStation, attrs)

    if found:
        # Return a worhtwhile string to the user using the above information
        update.message.reply_text("See map below for directions to the {0} station.".format(userStation))
        # Send a map to the user - retrieve the chat id from the original function call and use the lat/lng vars set above
        bot.sendLocation(update.effective_chat.id, latitude=lat, longitude=long, live_period=600);
    else:
        update.message.reply_text('Please specify a station name.')