import nltk
from nltk.tokenize import PunktSentenceTokenizer
from nltk.corpus import twitter_samples, state_union
from nltk.tag import pos_tag_sents
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, BaseFilter
import logging,requests, xmltodict, json

stations = ['Malahide', 'Portmarnock', 'Clongriffin', 'Sutton', 'Bayside', 'Howth Junction', 'Howth', 'Kilbarrack', 'Raheny', 'Harmonstown', 'Killester', 'Clontarf Road', 'Dublin Connolly',
            'Tara Street', 'Dublin Pearse', 'Grand Canal Dock', 'Lansdowne Road', 'Sandymount', 'Sydney Parade', 'Booterstown', 'Blackrock', 'Seapoint', 'Salthill', 'Dun Laoghaire',
            'Sandycove', 'Glenageary', 'Dalkey', 'Killiney', 'Shankill', 'Bray', 'Greystones', 'Kilcoole']
i=0
for station in stations:

    diff = nltk.edit_distance("dun laorie", station)
    if diff < 6:
        print(station)


# tweets = twitter_samples.strings('positive_tweets.json')
#
# tweets_tokens = twitter_samples.tokenized('positive_tweets.json')
#
# #Will tag the tokenized tweets - tuple
# tweets_tagged = pos_tag_sents(tweets_tokens)
#
# # JJ = ADJ, NN = Singular Noun, NS = Plural Noun
# JJ_count = 0
# NN_count = 0
#
#
# #loop through every tweet
# for tweet in tweets_tagged:
#     #loop through each token pair within each tweet
#     for pair in tweet:
#         #Count the number of ADJ, Singular and plura nouns
#         tag = pair[1]
#         if tag == 'JJ':
#             JJ_count += 1
#         elif tag == 'NN':
#             NN_count += 1
#
# #print('Tweet ', tweets[1])
# #print('Tokenized Tweet ', tweets_tokens[1])
# #print('Tagged Tweet ',tweets_tagged[1])
# #print('Total number of adjectives = ', JJ_count)
# #print('Total number of singular nouns = ', NN_count)
#
#
#
# train_text = state_union.raw("2005-GWBush.txt")
# sample_text = state_union.raw("2006-GWBush.txt")
# #Split text into sentences
# custom_sent_tokenizer = PunktSentenceTokenizer(train_text)
# #tokenize slit text
# tokenized = custom_sent_tokenizer.tokenize(sample_text)

def process_content():
    try:
        # for each sentence
        for i in tokenized:
            # Tokenization = breaking into words
            words = nltk.word_tokenize(i)
            print('Tokenized: ', words)
            #part-of-speech tagging - e.g JJ = ADJ, NN = Singular Noun, NS = Plural Noun NNP = Proper Noun
            tagged = nltk.pos_tag(words)
            print('Tagged: ',tagged)
            #mach pos tagged data with named entities 
            namedEnt = nltk.ne_chunk(tagged)
            namedEnt.draw()
            print(namedEnt)
    except Exception as e:
        print(str(e))


#process_content()

#https://github.com/arop/ner-re-pt/wiki/NLTK
#http://norvig.com/spell-correct.html
#https://www.digitalocean.com/community/tutorials/how-to-work-with-language-data-in-python-3-using-the-natural-language-toolkit-nltk
#https://pythonprogramming.net/
#http://www.nltk.org/book/ch06.html

#wtf engine, tracery 

