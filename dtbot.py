from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, BaseFilter
import logging
import requests, xmltodict, json
from pprint import pprint

i = 0
myStation = "";


class FilterTrain(BaseFilter):
    def filter(self, message):
        return 'train' in message.text.lower()
        #any(text.lower() in message.text.lower() for text in ('Foo', 'Bar'))

# Remember to initialize the class.
filter_train = FilterTrain()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def train(bot, update):
    #This works assuming the user inputs 'Train StationName'
    msg = update.message.text.split()
    if msg[1].lower() == 'dun' or msg[1].lower() == 'dublin' or msg[1].lower() == 'clontarf'  or msg[1].lower() == 'tara':
        sname = msg[1] + " " + msg[2]

    else:
        sname = msg[1]


    url = 'http://api.irishrail.ie/realtime/realtime.asmx/getStationDataByNameXML?StationDesc={0}'.format(sname)
    print(url)
    xml = requests.get(url)
    dict = xmltodict.parse(xml.content)
    jsonstr = json.dumps(dict)
    jsonobj = json.loads(jsonstr)
    dueIn = (jsonobj["ArrayOfObjStationData"]["objStationData"][0]["Duein"])
    stationName = (jsonobj["ArrayOfObjStationData"]["objStationData"][0]["Stationfullname"])
    destination = (jsonobj["ArrayOfObjStationData"]["objStationData"][0]["Destination"])
    #update.message.reply_text(jsonobj["ArrayOfObjStationData"]["objStationData"][1])
    update.message.reply_text("The next train to service the {0} station is heading for {1}, it's due in {2} minutes.".format(stationName, destination, dueIn))

    print(update.message.text)

    global i
    i += 1
    print("This has been called" , i , "times.")

    global myStation
    myStation= (jsonobj["ArrayOfObjStationData"]["objStationData"][1]["Stationfullname"])



def showme(bot, update):
    #getting lat/long
    global myStation

    url = 'http://api.irishrail.ie/realtime/realtime.asmx/getAllStationsXML_WithStationType?StationType=D'
    xml = requests.get(url)
    dict = xmltodict.parse(xml.content)
    jsonstr = json.dumps(dict)
    jsonobj = json.loads(jsonstr)

    x = jsonobj["ArrayOfObjStation"]["objStation"][0]

    for attrs in jsonobj["ArrayOfObjStation"]["objStation"]:
        if attrs['StationDesc'] == myStation:
            print ( "This is the shit:  {0}".format(attrs))
            lat = attrs['StationLatitude']
            long = attrs['StationLongitude']
            break

    update.message.reply_text("See map below for directions to the {0} station".format(myStation, ))
    #id = effective_chat

    bot.sendLocation(update.effective_chat.id, latitude=lat, longitude=long);


def thanks(bot, update):
    update.message.reply_text("You're Welcome! Let me know if you need anything else.")


def echo(bot, update):
    update.message.reply_text(update.message.text)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass in bot's token.
    updater = Updater("460295615:AAEUzHYLg9s1f6YNr1Ng2s5dKMv27lZZcWE")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(MessageHandler(filter_train, train))
    dp.add_handler(CommandHandler("showme", showme))
    dp.add_handler(CommandHandler("Thanks", thanks))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))
    


    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()