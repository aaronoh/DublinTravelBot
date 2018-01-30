import logging,requests, xmltodict, json
import nltk

def showStation(bot, update):
    stations = ['Malahide', 'Portmarnock', 'Clongriffin', 'Sutton', 'Bayside', 'Howth Junction', 'Howth',
                'Kilbarrack', 'Raheny', 'Harmonstown', 'Killester', 'Clontarf Road', 'Dublin Connolly',
                'Tara Street', 'Dublin Pearse', 'Grand Canal Dock', 'Lansdowne Road', 'Sandymount', 'Sydney Parade',
                'Booterstown', 'Blackrock', 'Seapoint', 'Salthill', 'Dun Laoghaire',
                'Sandycove', 'Glenageary', 'Dalkey', 'Killiney', 'Shankill', 'Bray', 'Greystones', 'Kilcoole']

    test = update.message.text.split()
    for station in stations:
        # print(test[3])
        for testitem in test:
            diff = nltk.edit_distance(testitem, station)
            if diff < 3:
                print('Original: {0}  New: {1}'.format(test, station))
                myStation = station
                # Poll api again - using the station info endpoint as this is the only way of getting their lat/long
                # xml -> dict -> json str -> json obj
                url = 'http://api.irishrail.ie/realtime/realtime.asmx/getAllStationsXML_WithStationType?StationType=D'
                xml = requests.get(url)
                dict = xmltodict.parse(xml.content)
                jsonstr = json.dumps(dict)
                jsonobj = json.loads(jsonstr)

                # For every object in the json obj
                for attrs in jsonobj["ArrayOfObjStation"]["objStation"]:
                    # if the station name attribute matches the global var station name
                    if attrs['StationDesc'] == myStation:
                        # lat/long vars = the lat/long attributes associated with that object
                        lat = attrs['StationLatitude']
                        long = attrs['StationLongitude']
                        # Once its' matched one, break out of the for loop
                        break
                    else:
                        print(myStation, attrs)
                # Return a worhtwhile string to the user using the above information
                update.message.reply_text("See map below for directions to the {0} station.".format(myStation))
                # Send a map to the user - retrieve the chat id from the original function call and use the lat/lng vars set above
                bot.sendLocation(update.effective_chat.id, latitude=lat, longitude=long, live_period=600);