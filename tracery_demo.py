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

    greeting_message = "{0} {1}. Welcome to DublinTravelBot. Use /list to view a all active stations, type 'trainStationName Direction' to view live availability information and use" \
               "/showme to get directions to your chosen station.".format(x,str(update.message.from_user.username))

    update.message.reply_text(greeting_message)
