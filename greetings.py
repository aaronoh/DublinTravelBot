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

    greeting_message = "{0} {1}. Welcome to DublinTravelBot. The easiest way to interact with me is to just talk! I'll do my best to understand you.\n\n" \
                       "If you'd prefer to use commands:\n\n"\
                       "Use /list or /listbikes to view all active stations.\n\n"\
                       "Type 'train StationName Direction' to view live availability information. e.g. Train Glenageary S.\n\n" \
                       "Soutbound destinations include Bray & Greystones, Northbound destinations include Howth & Malahide\n\n" \
                       "Type 'dbikes StationName' to view live availability information. e.g. dbikes Herbert place.\n\n" \
                       "Use /find to get directions to your closest station.\n\n" \
                       "Use /start to see this information again".format(x,str(update.message.from_user.username))

    update.message.reply_text(greeting_message)
