import nltk
from nltk.tokenize import word_tokenize
import spacy
import os
from telegram.ext import Updater
import logging,requests, xmltodict, json
from get_train import getTrain
from show_Station import showStation


def classify_message(bot,update):
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
    ('map', 'map')]

    test = [('when will the train be here', 'train'),
            ('where is the train', 'train'),
            ('where is the station','map'),
            ('Is there a dart due', 'train')]
    global myStation

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
    print('Classified as: ',classifier.classify(test_sent_features))
    print('Accuracy', nltk.classify.accuracy(classifier, test_features) * 100)
    print('*******************************')

    ner = spacy.load(os.getcwd())
    doc = ner(test_sentence)
    print("Entities in '%s'" % test_sentence)
    for ent in doc.ents:
        print(ent.text)
        station = (ent.text)

    if (classifier.classify(test_sent_features) == 'map' and distList.prob('map') *100 > 80):
       showStation(bot, update)
    elif (classifier.classify(test_sent_features) == 'train' and distList.prob('train')*100 > 80):
        getTrain(bot, update,station)

    else:
        update.message.reply_text("Sorry! I'm not sure what you're looking for. Would you mind rephrasing your question? If you need help try /start :)")




