from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, BaseFilter
import logging,requests, xmltodict, json
import tracery
from tracery.modifiers import base_english


def greeting(bot, update):
    def realGreet(greet):
        rules = {
            'origin': '#hello.capitalize#',
            'hello': ['Hello!', 'Hey!', 'Hi!'],
            'location': ['world', 'solar system', 'galaxy', 'universe']
        }

        grammar = tracery.Grammar(rules)
        grammar.add_modifiers(base_english)
        return grammar.flatten("#origin#")

    x = realGreet('greet')

    greeting_message = "{0} {1}. Welcome to DublinTravelBot. Use /list to view all active stations.\n\n" \
                       "Type 'train StationName Direction' to view live availability information. e.g. Train Glenageary S.\n\n" \
                       "You can use 'next' to conduct further searches on the same station, this will show you the next train that meets your search criteria.\n\n" \
                       "Soutbound destinations include Bray & Greystones, Northbound destinations include Howth & Malahide\n\n" \
                       "Use /showme to get directions to your chosen station.\n\n" \
                       "Use /start to see this information again".format(x,str(update.message.from_user.username))

    update.message.reply_text(greeting_message)
