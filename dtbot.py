from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, BaseFilter
import logging
import requests, xmltodict, json

i = 0


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
    xml = requests.get('http://api.irishrail.ie/realtime/realtime.asmx/getStationDataByCodeXML?StationCode=SMONT')
    dict = xmltodict.parse(xml.content)
    jsonstr = json.dumps(dict)
    jsonobj = json.loads(jsonstr)

    dueIn = (jsonobj["ArrayOfObjStationData"]["objStationData"][1]["Duein"])
    stationName = (jsonobj["ArrayOfObjStationData"]["objStationData"][1]["Stationfullname"])
    destination = (jsonobj["ArrayOfObjStationData"]["objStationData"][1]["Destination"])
    update.message.reply_text(jsonobj["ArrayOfObjStationData"]["objStationData"][1])
    update.message.reply_text("The next train to service the " + stationName + " station is heading for " + destination + ", it's due in " + dueIn + " minutes.")

    global i
    i += 1
    print("This has been called" , i , "times.")



def showme(bot, update):
    update.message.reply_text('Your train is due in 10 mintues.')
    update.message.reply_text('Click on the map below for directions.')
    bot.sendLocation(166047440, latitude=53.328958, longitude=-6.219859);


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