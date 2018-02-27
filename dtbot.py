from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, BaseFilter,CallbackQueryHandler
import telegram
import logging,requests, xmltodict, json
from greetings import greeting
from classify_ner import classify_message
import nltk
from closest_station import find, get_location
from closest_station import printIt, station_type
from get_bike import getBike


#Keep track of calls
i = 0
#Global var for station name - used by train and showme
myStation = "";

#Keep track of station pos
trains = []

#Array of station names for spell check
stations = ['malahide', 'portmarnock', 'clongriffin', 'sutton', 'bayside', 'howth junction', 'howth', 'kilbarrack', 'raheny', 'harmonstown', 'killester', 'clontarf road', 'dublin connolly',
            'tara street', 'dublin pearse', 'grand canal dock', 'lansdowne road', 'sandymount', 'sydney parade', 'booterstown', 'blackrock', 'seapoint', 'salthill', 'dun laoghaire',
            'sandycove', 'glenageary', 'dalkey', 'killiney', 'shankill', 'bray', 'greystones', 'kilcoole']

#Filter messages for 'train'
class FilterTrain(BaseFilter):
    def filter(self, message):
        return 'trains' in message.text.lower()

        #return 'train' in message.text.lower()
        #any(text.lower() in message.text.lower() for text in ('Foo', 'Bar'))

class FilterNext(BaseFilter):
    def filter(self, message):
        return 'next one' in message.text.lower()

class FilterBike(BaseFilter):
    def filter(self, message):
        return 'dbikes' in message.text.lower()

# Initialize filter class.
filter_train = FilterTrain()
filter_bike = FilterBike()
filter_next = FilterNext()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Pull stations from api, parse into json, construct string of relevant info, return to user
def train(bot, update):
    #reset the 'nextTrain' global var to 0
    global i
    i = 0
    #This works assuming the user inputs 'Train StationName Direction'
    #Splitting message into elements - message assumes 'train - stationName - Direction' format, meaning [1] would be the station name & [2] the direction.
    #If/else - really messy way of dealing with multiple word station names
    msg = update.message.text.split()
    if msg[1].lower() == 'dun' or msg[1].lower() == 'dublin' or msg[1].lower() == 'clontarf'  or msg[1].lower() == 'tara':
        sname = msg[1] + " " + msg[2]
        direction = msg[3]

    elif msg[1].lower() == 'grand':
        sname = msg[1] + " " + msg[2] + " " + msg[3]
        direction = msg[4]

    else:
        sname = msg[1]
        direction =  msg[2]

    #for each station in the stations array defined above, get the  Levenshtein edit-distance between the users entry and the recorded station names
    #if that difference is less than 4 characters, reassign - else leave it as it is (for now)

    #var used to verify that the station could be found using Levenshtein edit-distance
    newStationName = ""
    for station in stations:
        diff = nltk.edit_distance(sname, station)
        if diff < 4:
            print('************************************************')
            print('Original: {0}  New: {1}'.format(sname, station))
            print('{0} typed {1}'.format(str(update.message.from_user.username), str(update.message.text)))
            print('************************************************')
            newStationName = station

        else:
            print('Difference between {0} and {1} is: {2}'.format(newStationName, station, diff))

    #if the station isnt found using Levenshtein edit-distance, notify the user that the station could not be found:
    if newStationName =="":
        print('Station not found')
        update.message.reply_text('The {0} station could not be found. Please use /list to view a list of active stations.'.format(sname))
        return


    #Attributes are case sensitive - account for that
    if direction == "northbound" or direction.lower() == "north" or direction.lower() == "n":
            direction = "Northbound"

    if direction == "southbound" or direction.lower() == "south" or direction.lower() == "s":
            direction = "Southbound"

    url = 'http://api.irishrail.ie/realtime/realtime.asmx/getStationDataByNameXML?StationDesc={0}'.format(newStationName)
    #xml -> dict -> json str -> json obj
    xml = requests.get(url)
    dict = xmltodict.parse(xml.content)
    jsonstr = json.dumps(dict)
    jsonobj = json.loads(jsonstr)

    #global array, set to empty at each call (new search)
    global trains
    trains = []

    try:
        # For every object in the json obj
        for attrs in jsonobj["ArrayOfObjStationData"]["objStationData"]:
            #if the direction matches the requested direction
            if attrs['Direction'] == direction:
                #add the trains to an array
                trains.append(attrs)

        # Pull out specific elements of the first element in the array - reqorked to use this array to allow the user to search for additional trains servicing the same station
        #e.g Train due in 2 mins, user may be more interested in the next train - Show them [1] instead of [0]
        dueIn = (trains[0]['Duein'])
        stationName = (trains[0]["Stationfullname"])
        destination = (trains[0]["Destination"])
        dir = (trains[0]["Direction"])

        # Return worthwhile string to user
        update.message.reply_text("The next {0} train to service the {1} station is heading for {2}, it's due in {3} minutes.".format(dir,stationName,destination,dueIn))

        # Setting global var station name to the name of the station just searched for
        global myStation
        global myDirection
        myDirection= dir
        myStation = (jsonobj["ArrayOfObjStationData"]["objStationData"][1]["Stationfullname"])


        if not trains:
            print(trains)
            update.message.reply_text(
                "There are no trains travelling {0} due at the {1} station within the next 90 minutes, or the {1} station cannot be found. Please try again later. ".format(
                    direction, sname))
            return;


    except:
        update.message.reply_text("There are no trains travelling {0} due at the {1} station within the next 90 minutes, or the {1} station cannot be found. Please try again later. ".format(direction, sname))
        return;




def nextTrain(bot, update):
    #i used to keep track of train pos being searched, incremented each time this function is called and reset when a new search is made
    global i
    global direction
    i += 1
    #pull out specific eleemnts of the array, using i as the index
    try:
        dueIn = (trains[i]['Duein'])
        stationName = (trains[i]["Stationfullname"])
        destination = (trains[i]["Destination"])
        dir = (trains[i]["Direction"])
        # Return worthwhile string to user
        update.message.reply_text("A {0} train will service the {1} station in {2} minutes it's heading for {3}. {4} train(s) will service the station before this.".format(dir,stationName,dueIn,destination,i))

    except:
        update.message.reply_text('There are no further {0} trains servicing the {1} station within the next 90 minutes. Please try again later.'.format(myDirection, myStation))
def showme(bot, update):
    #retrieves global station name
    global myStation

    #Poll api again - using the station info endpoint as this is the only way of getting their lat/long
    # xml -> dict -> json str -> json obj
    url = 'http://api.irishrail.ie/realtime/realtime.asmx/getAllStationsXML_WithStationType?StationType=D'
    xml = requests.get(url)
    dict = xmltodict.parse(xml.content)
    jsonstr = json.dumps(dict)
    jsonobj = json.loads(jsonstr)

    # For every object in the json obj
    for attrs in jsonobj["ArrayOfObjStation"]["objStation"]:
        #if the station name attribute matches the global var station name
        if attrs['StationDesc'] == myStation:
            #lat/long vars = the lat/long attributes associated with that object
            lat = attrs['StationLatitude']
            long = attrs['StationLongitude']
            #Once its' matched one, break out of the for loop
            break
    #Return a worhtwhile string to the user using the above information
    update.message.reply_text("See map below for directions to the {0} station.".format(myStation))

    #Send a map to the user - retrieve the chat id from the original function call and use the lat/lng vars set above
    bot.sendLocation(update.effective_chat.id, latitude=lat, longitude=long, live_period=600);

def liststations(bot, update):
    # Poll api again - using the station info endpoint
    # xml -> dict -> json str -> json obj
    url = 'http://api.irishrail.ie/realtime/realtime.asmx/getAllStationsXML_WithStationType?StationType=D'
    xml = requests.get(url)
    dict = xmltodict.parse(xml.content)
    jsonstr = json.dumps(dict)
    jsonobj = json.loads(jsonstr)
    list_of_stations = ""
    # For every object in the json obj
    for attrs in jsonobj["ArrayOfObjStation"]["objStation"]:
        # add the stationdesc attribute to the string list_of_stations
        list_of_stations += (attrs['StationDesc'] + ", ")
    # Return a worhtwhile string to the user using the above information
    update.message.reply_text("Here is a list of all stations currently operating DART services: {0}.\n\nTo view live availability information for any of these stops simply type 'Train', the name of the station and the direction. For example,  Train Sandymount n".format(list_of_stations))

def listbikes(bot, update):
    jsonstr = requests.get(
        'https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=2eb0463a8d6feabf397cf5babdc21d4e764701a9')
    data = (jsonstr.json())
    i = 0
    stations = []
    for d in data:
        stations.append(data[i]['address'])
        i = i + 1

    update.message.reply_text(
        "Here is a list of all stations currently operating DublinBike services: {0}.\n\nTo view live availability information for any of these stops simply type 'dBikes', and the name of the station".format(stations))




def echo(bot, update):
    update.message.reply_text("Oops, I don't understand your message!\n\nSearch by typing train followed by the name of your station and the direction of travel (north or south).\n\nFor example: train bray south\n\nIf you need any help use /start or /list. ")
    print('************************************************')
    print('{0} typed {1}'.format(str(update.message.from_user.username), str(update.message.text)))
    print('************************************************')


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))



def main():
    # Create EventHandler, pass in api key.
    updater = Updater("460295615:AAEUzHYLg9s1f6YNr1Ng2s5dKMv27lZZcWE")
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    # when a message contains a defined command (/showm -> run the showme function)
    dp.add_handler(CommandHandler("showme", showme))
    dp.add_handler(CommandHandler("list", liststations))
    dp.add_handler(CommandHandler("listbikes", listbikes))
    dp.add_handler(CommandHandler("start", greeting))
    dp.add_handler(CommandHandler("find", find))


    # when a message triggers the filter_train, run the train function
    dp.add_handler(MessageHandler(Filters.location,station_type))
    dp.add_handler(MessageHandler(filter_train, train))
    dp.add_handler(MessageHandler(filter_bike, getBike))
    dp.add_handler(MessageHandler(filter_next, nextTrain))
    # test handler - when a message that contains text is received - trigger the echo function
    dp.add_handler(MessageHandler(Filters.text, classify_message))

    dp.add_handler(CallbackQueryHandler(printIt))

    

    #add error handler
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()