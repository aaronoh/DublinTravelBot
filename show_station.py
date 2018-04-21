import logging,requests, xmltodict, json
import nltk


def showStation(bot, update,userStation):

    # Poll api again - using the station info endpoint as this is the only way of getting their lat/long
    # xml -> dict -> json str -> json obj
    url = 'http://api.irishrail.ie/realtime/realtime.asmx/getAllStationsXML_WithStationType?StationType=D'
    xml = requests.get(url)
    dict = xmltodict.parse(xml.content)
    jsonstr = json.dumps(dict)
    jsonobj = json.loads(jsonstr)

    found=''

    url = 'https://tracker.dashbot.io/track?platform=generic&v=9.4.0-rest&type=incoming&apiKey=GNBzfWCO7HSzfsLvNqImagfhBES8d7a1ZLlQQW59'
    headers = {'Content-Type': 'application/json'}
    analytics = '{{"text": "{2}", "userId": "{0}", "platformJson":{{"userName": "{1}","Action": "Show train station"}}}}'.format(
        update.effective_chat.id, update.message.from_user.username, update.message.text)
    requests.post(url, headers=headers, data=analytics)

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
        msg = "See map below for directions to the {0} station.".format(userStation)
        update.message.reply_text(msg)
        # Send a map to the user - retrieve the chat id from the original function call and use the lat/lng vars set above
        bot.sendLocation(update.effective_chat.id, latitude=lat, longitude=long, live_period=600);
        url = 'https://tracker.dashbot.io/track?platform=generic&v=9.4.0-rest&type=outgoing&apiKey=GNBzfWCO7HSzfsLvNqImagfhBES8d7a1ZLlQQW59'
        headers = {'Content-Type': 'application/json'}
        analytics = '{{"text": "{0}", "userId": "DublinTravelBot", "platformJson":{{"userName": "DublinTravelBot",' \
                    '"Action": "Show train station"}}}}'.format(msg)
        requests.post(url, headers=headers, data=analytics)

    else:
        update.message.reply_text('Please specify a station name.')