import nltk
from nltk.tokenize import PunktSentenceTokenizer
from nltk.corpus import twitter_samples, state_union
from nltk.tag import pos_tag_sents
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, BaseFilter
import logging,requests, xmltodict, json
from nltk import sent_tokenize, word_tokenize, pos_tag, ne_chunk

# stations = ['Malahide', 'Portmarnock', 'Clongriffin', 'Sutton', 'Bayside', 'Howth Junction', 'Howth', 'Kilbarrack', 'Raheny', 'Harmonstown', 'Killester', 'Clontarf Road', 'Dublin Connolly',
#             'Tara Street', 'Dublin Pearse', 'Grand Canal Dock', 'Lansdowne Road', 'Sandymount', 'Sydney Parade', 'Booterstown', 'Blackrock', 'Seapoint', 'Salthill', 'Dun Laoghaire',
#             'Sandycove', 'Glenageary', 'Dalkey', 'Killiney', 'Shankill', 'Bray', 'Greystones', 'Kilcoole']
# i=0
# for station in stations:
#
#     diff = nltk.edit_distance("dun laorie", station)
#     if diff < 6:
#         print(station)


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
# #
# train_file = open("NLTK/training.txt")
# train_text = train_file.read()
#
# sample_file = open("NLTK/sample.txt")
# sample_text = sample_file.read()
#  #Split text into sentences
# custom_sent_tokenizer = PunktSentenceTokenizer(train_text)
#  #tokenize slit text
# tokenized = custom_sent_tokenizer.tokenize(sample_text)

# def process_content():
#     try:
#         # for each sentence
#         for i in tokenized:
#             # Tokenization = breaking into words
#             words = nltk.word_tokenize(i)
#             print('Tokenized: ', words)
#             #part-of-speech tagging - e.g JJ = ADJ, NN = Singular Noun, NS = Plural Noun NNP = Proper Noun
#             tagged = nltk.pos_tag(words)
#             print('Tagged: ',tagged)
#             #mach pos tagged data with named entities
#             namedEnt = nltk.ne_chunk(tagged)
#             namedEnt.draw()
#             print(namedEnt)
#     except Exception as e:
#         print(str(e))
#
# process_content()

#https://github.com/arop/ner-re-pt/wiki/NLTK
#http://norvig.com/spell-correct.html
#https://www.digitalocean.com/community/tutorials/how-to-work-with-language-data-in-python-3-using-the-natural-language-toolkit-nltk
#https://pythonprogramming.net/
#http://www.nltk.org/book/ch06.html

#wtf engine, tracery 


# stations = ['malahide', 'portmarnock', 'clongriffin', 'sutton', 'bayside', 'howth junction', 'howth', 'kilbarrack', 'raheny', 'harmonstown', 'killester', 'clontarf road', 'dublin connolly',
#             'tara street', 'dublin pearse', 'grand canal dock', 'lansdowne road', 'sandymount', 'sydney parade', 'booterstown', 'blackrock', 'seapoint', 'salthill', 'dun laoghaire',
#             'sandycove', 'glenageary', 'dalkey', 'killiney', 'shankill', 'bray', 'greystones', 'kilcoole']
#
# test = 'Find a train in grstones'.split()
# for station in stations:
#    # print(test[3])
#     for testitem in test:
#         diff = nltk.edit_distance(testitem, station)
#         if diff < 3:
#             print('Original: {0}  New: {1}'.format(test, station))
#
#         else: print('Done')

def extract_entities(text):
	entities = []
	for sentence in sent_tokenize(text):
	    chunks = ne_chunk(pos_tag(word_tokenize(sentence)))
	    entities.extend([chunk for chunk in chunks if hasattr(chunk, 'label')])
	return entities


if __name__ == '__main__':
	text = "I went to New York to meet John Smith"
	print(extract_entities(text))