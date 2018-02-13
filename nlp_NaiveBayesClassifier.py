import nltk
from nltk.tokenize import word_tokenize
import spacy
import os
from telegram.ext import Updater
import logging,requests, xmltodict, json
from get_train import getTrain
from show_Station import showStation
from closestStation import get_location, find


def classify_message(bot,update):

    station_components = ['malahide', 'portmarnock', 'clongriffin', 'sutton', 'bayside','howth', 'junction',
                'kilbarrack', 'raheny', 'harmonstown', 'killester', 'clontarf', 'road', 'connolly',
                'street', 'dublin', 'pearse', 'grand', 'canal', 'dock', 'lansdowne', 'sandymount', 'sydney', 'parade',
                'booterstown', 'blackrock', 'seapoint', 'salthill', 'laoghaire',
                'sandycove', 'glenageary', 'dalkey', 'killiney', 'shankill', 'bray', 'greystones', 'kilcoole']

    #input sentences with sentiment tags
    trainingData = [('train', 'train'),
    ('next train in', 'train'),
    ('When is the next train', 'train'),
    ('How long until the next train', 'train'),
    ("Where is the next train", 'train'),
    ('dart', 'train'),
    ('next dart in', 'train'),
    ('When is the next dart', 'train'),
    ('train to', 'train'),
    ('dart to', 'train'),
    ('How long until the next dart', 'train'),
    ("Where is the next dart", 'train'),
    ("Show me where that station is", 'map'),
    ("Directions to station", 'map'),
    ("What dart station", 'map'),
    ("Wheres station", 'map'),
    ("Wheres bray", 'map'),
    ("Wheres the station", 'map'),
    ("Wheres", 'map'),
    ('map', 'map'),
    ("Wheres is my closest station", 'closest'),
    ("Which is the closest staion", 'closest'),
    ("Wheres is the nearest station", 'closest'),
    ("Which station should I use", 'closest'),
    ("closest", 'closest'),
    ("nearest", 'closest')
    ]

    test = [('when will the train be here', 'train'),
            ('where is the train', 'train'),
            ('where is the station','map'),
            ('Is there a dart due', 'train')]

    all_training_words = set(word.lower() for passage in trainingData for word in word_tokenize(passage[0]))
    training = [({word: (word in word_tokenize(x[0])) for word in all_training_words}, x[1]) for x in trainingData]
    classifier = nltk.NaiveBayesClassifier.train(training)
    #classifier.show_most_informative_features()
    test_features = [({word: (word in word_tokenize(x[0])) for word in all_training_words}, x[1]) for x in test]

    test_sentence = update.message.text
    test_sent_features = {word.lower(): (word in word_tokenize(test_sentence.lower())) for word in all_training_words}

    print('*******************************')
    distList = classifier.prob_classify(test_sent_features)
    print(distList)
    print(distList.samples())
    print('Map Prob: ', distList.prob('map') *100, '%')
    print('Train Prob: ', distList.prob('train')*100, '%')
    print('Closest Prob: ', distList.prob('closest') * 100, '%')
    print('Classified as: ',classifier.classify(test_sent_features))
    print('Accuracy', nltk.classify.accuracy(classifier, test_features) * 100)
    print('*******************************')

    #NER
    NERStation = ''
    ner = spacy.load(os.getcwd())
    doc = ner(test_sentence)
    print("Entities in '%s'" % test_sentence)
    #for each entity in the doc
    for ent in doc.ents:
        #print them, set them to the val of NER station
        print(ent.text)
        NERStation = (ent.text)

    print(NERStation)
    if NERStation == '':
        update.message.reply_text("Sorry! I couldn't identify the station you're looking for. Please try again, use /list if you're unsure of the station name.")
        return

    else:
        comps = []
        #for each 'component' in the station components array
        for components in  station_components:
            #for each word in the split sentence constructed above
            for word in NERStation.split():
                #'diff' = the levenstein dist. between the two words
                diff = nltk.edit_distance(word, components)
                #if that diff is less than 3
                if diff < 3:
                    #print it out, add the spell corrected component to an array
                    print('Original: {0}  New: {1}'.format(NERStation.split(), components))
                    comps.append(components)
                    print(comps)
        #convert comps to a sting seperated by spaces -> ner+spell corrected name
        userStation = " ".join(comps)

        if (classifier.classify(test_sent_features) == 'map' and distList.prob('map') *100 > 80):
           showStation(bot, update, userStation)

        elif (classifier.classify(test_sent_features) == 'train' and distList.prob('train')*100 > 80):
            getTrain(bot, update, userStation)

        elif (classifier.classify(test_sent_features) == 'closest' and distList.prob('closest') * 100 > 80):
            find(bot, update)
        else:
            update.message.reply_text("Sorry! I'm not sure what you're looking for. Would you mind rephrasing your question? If you need help try /start :)")




