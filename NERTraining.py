"""Example of training an additional entity type

This script shows how to add a new entity type to an existing pre-trained NER
model. To keep the example short and simple, only four sentences are provided
as examples. In practice, you'll need many more — a few hundred would be a
good start. You will also likely need to mix in examples of other entity
types, which might be obtained by running the entity recognizer over unlabelled
sentences, and adding their annotations to the training set.

The actual training is performed by looping over the examples, and calling
`nlp.entity.update()`. The `update()` method steps through the words of the
input. At each word, it makes a prediction. It then consults the annotations
provided on the GoldParse instance, to see whether it was right. If it was
wrong, it adjusts its weights so that the correct action will score higher
next time.

After training your model, you can save it to a directory. We recommend
wrapping models as Python packages, for ease of deployment.

For more details, see the documentation:
* Training: https://spacy.io/usage/training
* NER: https://spacy.io/usage/linguistic-features#named-entities

Compatible with: spaCy v2.0.0+
"""
from __future__ import unicode_literals, print_function

import plac
import random
from pathlib import Path
import spacy
import os

# new entity label
LABEL = 'STATION'

# training data
# Note: If you're using an existing model, make sure to mix in examples of
# other entity types that spaCy correctly recognized before. Otherwise, your
# model might learn the new type, but "forget" what it previously knew.
# https://explosion.ai/blog/pseudo-rehearsal-catastrophic-forgetting
TRAIN_DATA = [('malahide staion north', {'entities': [(0, 8, 'STATION')]}),
              ('Show me malahide', {'entities': [(8, 16, 'STATION')]}),
              ('Train from malahide south', {'entities': [(11, 19, 'STATION')]}),
              ('Next train to malahide north', {'entities': [(14, 22, 'STATION')]}),
              ('Where is malahide south?', {'entities': [(9, 17, 'STATION')]}),
              ('train south from malahide?', {'entities': [(17, 25, 'STATION')]}),
              ('going north from malahide?', {'entities': [(17, 25, 'STATION')]}),
              ('train heading north malahide?', {'entities': [(20, 28, 'STATION')]}),
              ('portmarnock staion north', {'entities': [(0, 11, 'STATION')]}),
              ('Show me portmarnock', {'entities': [(8, 19, 'STATION')]}),
              ('Train from portmarnock south', {'entities': [(11, 22, 'STATION')]}),
              ('Next train to portmarnock north', {'entities': [(14, 25, 'STATION')]}),
              ('Where is portmarnock south?', {'entities': [(9, 20, 'STATION')]}),
              ('train south from portmarnock?', {'entities': [(17, 28, 'STATION')]}),
              ('going north from portmarnock?', {'entities': [(17, 28, 'STATION')]}),
              ('train heading north portmarnock?', {'entities': [(20, 31, 'STATION')]}),
              ('clongriffin staion north', {'entities': [(0, 11, 'STATION')]}),
              ('Show me clongriffin', {'entities': [(8, 19, 'STATION')]}),
              ('Train from clongriffin south', {'entities': [(11, 22, 'STATION')]}),
              ('Next train to clongriffin north', {'entities': [(14, 25, 'STATION')]}),
              ('Where is clongriffin south?', {'entities': [(9, 20, 'STATION')]}),
              ('train south from clongriffin?', {'entities': [(17, 28, 'STATION')]}),
              ('going north from clongriffin?', {'entities': [(17, 28, 'STATION')]}),
              ('train heading north clongriffin?', {'entities': [(20, 31, 'STATION')]}),
              ('sutton staion north', {'entities': [(0, 6, 'STATION')]}),
              ('Show me sutton', {'entities': [(8, 14, 'STATION')]}),
              ('Train from sutton south', {'entities': [(11, 17, 'STATION')]}),
              ('Next train to sutton north', {'entities': [(14, 20, 'STATION')]}),
              ('Where is sutton south?', {'entities': [(9, 15, 'STATION')]}),
              ('train south from sutton?', {'entities': [(17, 23, 'STATION')]}),
              ('going north from sutton?', {'entities': [(17, 23, 'STATION')]}),
              ('train heading north sutton?', {'entities': [(20, 26, 'STATION')]}),
              ('bayside staion north', {'entities': [(0, 7, 'STATION')]}),
              ('Show me bayside', {'entities': [(8, 15, 'STATION')]}),
              ('Train from bayside south', {'entities': [(11, 18, 'STATION')]}),
              ('Next train to bayside north', {'entities': [(14, 21, 'STATION')]}),
              ('Where is bayside south?', {'entities': [(9, 16, 'STATION')]}),
              ('train south from bayside?', {'entities': [(17, 24, 'STATION')]}),
              ('going north from bayside?', {'entities': [(17, 24, 'STATION')]}),
              ('train heading north bayside?', {'entities': [(20, 27, 'STATION')]}),
              ('howth junction staion north', {'entities': [(0, 14, 'STATION')]}),
              ('Show me howth junction', {'entities': [(8, 22, 'STATION')]}),
              ('Train from howth junction south', {'entities': [(11, 25, 'STATION')]}),
              ('Next train to howth junction north', {'entities': [(14, 28, 'STATION')]}),
              ('Where is howth junction south?', {'entities': [(9, 23, 'STATION')]}),
              ('train south from howth junction?', {'entities': [(17, 31, 'STATION')]}),
              ('going north from howth junction?', {'entities': [(17, 31, 'STATION')]}),
              ('train heading north howth junction?', {'entities': [(20, 34, 'STATION')]}),
              ('howth staion north', {'entities': [(0, 5, 'STATION')]}),
              ('Show me howth', {'entities': [(8, 13, 'STATION')]}),
              ('Train from howth south', {'entities': [(11, 16, 'STATION')]}),
              ('Next train to howth north', {'entities': [(14, 19, 'STATION')]}),
              ('Where is howth south?', {'entities': [(9, 14, 'STATION')]}),
              ('train south from howth?', {'entities': [(17, 22, 'STATION')]}),
              ('going north from howth?', {'entities': [(17, 22, 'STATION')]}),
              ('train heading north howth?', {'entities': [(20, 25, 'STATION')]}),
              ('kilbarrack staion north', {'entities': [(0, 10, 'STATION')]}),
              ('Show me kilbarrack', {'entities': [(8, 18, 'STATION')]}),
              ('Train from kilbarrack south', {'entities': [(11, 21, 'STATION')]}),
              ('Next train to kilbarrack north', {'entities': [(14, 24, 'STATION')]}),
              ('Where is kilbarrack south?', {'entities': [(9, 19, 'STATION')]}),
              ('train south from kilbarrack?', {'entities': [(17, 27, 'STATION')]}),
              ('going north from kilbarrack?', {'entities': [(17, 27, 'STATION')]}),
              ('train heading north kilbarrack?', {'entities': [(20, 30, 'STATION')]}),
              ('raheny staion north', {'entities': [(0, 6, 'STATION')]}),
              ('Show me raheny', {'entities': [(8, 14, 'STATION')]}),
              ('Train from raheny south', {'entities': [(11, 17, 'STATION')]}),
              ('Next train to raheny north', {'entities': [(14, 20, 'STATION')]}),
              ('Where is raheny south?', {'entities': [(9, 15, 'STATION')]}),
              ('train south from raheny?', {'entities': [(17, 23, 'STATION')]}),
              ('going north from raheny?', {'entities': [(17, 23, 'STATION')]}),
              ('train heading north raheny?', {'entities': [(20, 26, 'STATION')]}),
              ('harmonstown staion north', {'entities': [(0, 11, 'STATION')]}),
              ('Show me harmonstown', {'entities': [(8, 19, 'STATION')]}),
              ('Train from harmonstown south', {'entities': [(11, 22, 'STATION')]}),
              ('Next train to harmonstown north', {'entities': [(14, 25, 'STATION')]}),
              ('Where is harmonstown south?', {'entities': [(9, 20, 'STATION')]}),
              ('train south from harmonstown?', {'entities': [(17, 28, 'STATION')]}),
              ('going north from harmonstown?', {'entities': [(17, 28, 'STATION')]}),
              ('train heading north harmonstown?', {'entities': [(20, 31, 'STATION')]}),
              ('killester staion north', {'entities': [(0, 9, 'STATION')]}),
              ('Show me killester', {'entities': [(8, 17, 'STATION')]}),
              ('Train from killester south', {'entities': [(11, 20, 'STATION')]}),
              ('Next train to killester north', {'entities': [(14, 23, 'STATION')]}),
              ('Where is killester south?', {'entities': [(9, 18, 'STATION')]}),
              ('train south from killester?', {'entities': [(17, 26, 'STATION')]}),
              ('going north from killester?', {'entities': [(17, 26, 'STATION')]}),
              ('train heading north killester?', {'entities': [(20, 29, 'STATION')]}),
              ('clontarf road staion north', {'entities': [(0, 13, 'STATION')]}),
              ('Show me clontarf road', {'entities': [(8, 21, 'STATION')]}),
              ('Train from clontarf road south', {'entities': [(11, 24, 'STATION')]}),
              ('Next train to clontarf road north', {'entities': [(14, 27, 'STATION')]}),
              ('Where is clontarf road south?', {'entities': [(9, 22, 'STATION')]}),
              ('train south from clontarf road?', {'entities': [(17, 30, 'STATION')]}),
              ('going north from clontarf road?', {'entities': [(17, 30, 'STATION')]}),
              ('train heading north clontarf road?', {'entities': [(20, 33, 'STATION')]}),
              ('dublin connolly staion north', {'entities': [(0, 15, 'STATION')]}),
              ('Show me dublin connolly', {'entities': [(8, 23, 'STATION')]}),
              ('Train from dublin connolly south', {'entities': [(11, 26, 'STATION')]}),
              ('Next train to dublin connolly north', {'entities': [(14, 29, 'STATION')]}),
              ('Where is dublin connolly south?', {'entities': [(9, 24, 'STATION')]}),
              ('train south from dublin connolly?', {'entities': [(17, 32, 'STATION')]}),
              ('going north from dublin connolly?', {'entities': [(17, 32, 'STATION')]}),
              ('train heading north dublin connolly?', {'entities': [(20, 35, 'STATION')]}),
              ('tara street staion north', {'entities': [(0, 11, 'STATION')]}),
              ('Show me tara street', {'entities': [(8, 19, 'STATION')]}),
              ('Train from tara street south', {'entities': [(11, 22, 'STATION')]}),
              ('Next train to tara street north', {'entities': [(14, 25, 'STATION')]}),
              ('Where is tara street south?', {'entities': [(9, 20, 'STATION')]}),
              ('train south from tara street?', {'entities': [(17, 28, 'STATION')]}),
              ('going north from tara street?', {'entities': [(17, 28, 'STATION')]}),
              ('train heading north tara street?', {'entities': [(20, 31, 'STATION')]}),
              ('dublin pearse staion north', {'entities': [(0, 13, 'STATION')]}),
              ('Show me dublin pearse', {'entities': [(8, 21, 'STATION')]}),
              ('Train from dublin pearse south', {'entities': [(11, 24, 'STATION')]}),
              ('Next train to dublin pearse north', {'entities': [(14, 27, 'STATION')]}),
              ('Where is dublin pearse south?', {'entities': [(9, 22, 'STATION')]}),
              ('train south from dublin pearse?', {'entities': [(17, 30, 'STATION')]}),
              ('going north from dublin pearse?', {'entities': [(17, 30, 'STATION')]}),
              ('train heading north dublin pearse?', {'entities': [(20, 33, 'STATION')]}),
              ('grand canal dock staion north', {'entities': [(0, 16, 'STATION')]}),
              ('Show me grand canal dock', {'entities': [(8, 24, 'STATION')]}),
              ('Train from grand canal dock south', {'entities': [(11, 27, 'STATION')]}),
              ('Next train to grand canal dock north', {'entities': [(14, 30, 'STATION')]}),
              ('Where is grand canal dock south?', {'entities': [(9, 25, 'STATION')]}),
              ('train south from grand canal dock?', {'entities': [(17, 33, 'STATION')]}),
              ('going north from grand canal dock?', {'entities': [(17, 33, 'STATION')]}),
              ('train heading north grand canal dock?', {'entities': [(20, 36, 'STATION')]}),
              ('lansdowne road staion north', {'entities': [(0, 14, 'STATION')]}),
              ('Show me lansdowne road', {'entities': [(8, 22, 'STATION')]}),
              ('Train from lansdowne road south', {'entities': [(11, 25, 'STATION')]}),
              ('Next train to lansdowne road north', {'entities': [(14, 28, 'STATION')]}),
              ('Where is lansdowne road south?', {'entities': [(9, 23, 'STATION')]}),
              ('train south from lansdowne road?', {'entities': [(17, 31, 'STATION')]}),
              ('going north from lansdowne road?', {'entities': [(17, 31, 'STATION')]}),
              ('train heading north lansdowne road?', {'entities': [(20, 34, 'STATION')]}),
              ('sandymount staion north', {'entities': [(0, 10, 'STATION')]}),
              ('Show me sandymount', {'entities': [(8, 18, 'STATION')]}),
              ('Train from sandymount south', {'entities': [(11, 21, 'STATION')]}),
              ('Next train to sandymount north', {'entities': [(14, 24, 'STATION')]}),
              ('Where is sandymount south?', {'entities': [(9, 19, 'STATION')]}),
              ('train south from sandymount?', {'entities': [(17, 27, 'STATION')]}),
              ('going north from sandymount?', {'entities': [(17, 27, 'STATION')]}),
              ('train heading north sandymount?', {'entities': [(20, 30, 'STATION')]}),
              ('sydney parade staion north', {'entities': [(0, 13, 'STATION')]}),
              ('Show me sydney parade', {'entities': [(8, 21, 'STATION')]}),
              ('Train from sydney parade south', {'entities': [(11, 24, 'STATION')]}),
              ('Next train to sydney parade north', {'entities': [(14, 27, 'STATION')]}),
              ('Where is sydney parade south?', {'entities': [(9, 22, 'STATION')]}),
              ('train south from sydney parade?', {'entities': [(17, 30, 'STATION')]}),
              ('going north from sydney parade?', {'entities': [(17, 30, 'STATION')]}),
              ('train heading north sydney parade?', {'entities': [(20, 33, 'STATION')]}),
              ('booterstown staion north', {'entities': [(0, 11, 'STATION')]}),
              ('Show me booterstown', {'entities': [(8, 19, 'STATION')]}),
              ('Train from booterstown south', {'entities': [(11, 22, 'STATION')]}),
              ('Next train to booterstown north', {'entities': [(14, 25, 'STATION')]}),
              ('Where is booterstown south?', {'entities': [(9, 20, 'STATION')]}),
              ('train south from booterstown?', {'entities': [(17, 28, 'STATION')]}),
              ('going north from booterstown?', {'entities': [(17, 28, 'STATION')]}),
              ('train heading north booterstown?', {'entities': [(20, 31, 'STATION')]}),
              ('blackrock staion north', {'entities': [(0, 9, 'STATION')]}),
              ('Show me blackrock', {'entities': [(8, 17, 'STATION')]}),
              ('Train from blackrock south', {'entities': [(11, 20, 'STATION')]}),
              ('Next train to blackrock north', {'entities': [(14, 23, 'STATION')]}),
              ('Where is blackrock south?', {'entities': [(9, 18, 'STATION')]}),
              ('train south from blackrock?', {'entities': [(17, 26, 'STATION')]}),
              ('going north from blackrock?', {'entities': [(17, 26, 'STATION')]}),
              ('train heading north blackrock?', {'entities': [(20, 29, 'STATION')]}),
              ('seapoint staion north', {'entities': [(0, 8, 'STATION')]}),
              ('Show me seapoint', {'entities': [(8, 16, 'STATION')]}),
              ('Train from seapoint south', {'entities': [(11, 19, 'STATION')]}),
              ('Next train to seapoint north', {'entities': [(14, 22, 'STATION')]}),
              ('Where is seapoint south?', {'entities': [(9, 17, 'STATION')]}),
              ('train south from seapoint?', {'entities': [(17, 25, 'STATION')]}),
              ('going north from seapoint?', {'entities': [(17, 25, 'STATION')]}),
              ('train heading north seapoint?', {'entities': [(20, 28, 'STATION')]}),
              ('salthill staion north', {'entities': [(0, 8, 'STATION')]}),
              ('Show me salthill', {'entities': [(8, 16, 'STATION')]}),
              ('Train from salthill south', {'entities': [(11, 19, 'STATION')]}),
              ('Next train to salthill north', {'entities': [(14, 22, 'STATION')]}),
              ('Where is salthill south?', {'entities': [(9, 17, 'STATION')]}),
              ('train south from salthill?', {'entities': [(17, 25, 'STATION')]}),
              ('going north from salthill?', {'entities': [(17, 25, 'STATION')]}),
              ('train heading north salthill?', {'entities': [(20, 28, 'STATION')]}),
              ('dun laoghaire staion north', {'entities': [(0, 13, 'STATION')]}),
              ('Show me dun laoghaire', {'entities': [(8, 21, 'STATION')]}),
              ('Train from dun laoghaire south', {'entities': [(11, 24, 'STATION')]}),
              ('Next train to dun laoghaire north', {'entities': [(14, 27, 'STATION')]}),
              ('Where is dun laoghaire south?', {'entities': [(9, 22, 'STATION')]}),
              ('train south from dun laoghaire?', {'entities': [(17, 30, 'STATION')]}),
              ('going north from dun laoghaire?', {'entities': [(17, 30, 'STATION')]}),
              ('train heading north dun laoghaire?', {'entities': [(20, 33, 'STATION')]}),
              ('sandycove staion north', {'entities': [(0, 9, 'STATION')]}),
              ('Show me sandycove', {'entities': [(8, 17, 'STATION')]}),
              ('Train from sandycove south', {'entities': [(11, 20, 'STATION')]}),
              ('Next train to sandycove north', {'entities': [(14, 23, 'STATION')]}),
              ('Where is sandycove south?', {'entities': [(9, 18, 'STATION')]}),
              ('train south from sandycove?', {'entities': [(17, 26, 'STATION')]}),
              ('going north from sandycove?', {'entities': [(17, 26, 'STATION')]}),
              ('train heading north sandycove?', {'entities': [(20, 29, 'STATION')]}),
              ('glenageary staion north', {'entities': [(0, 10, 'STATION')]}),
              ('Show me glenageary', {'entities': [(8, 18, 'STATION')]}),
              ('Train from glenageary south', {'entities': [(11, 21, 'STATION')]}),
              ('Next train to glenageary north', {'entities': [(14, 24, 'STATION')]}),
              ('Where is glenageary south?', {'entities': [(9, 19, 'STATION')]}),
              ('train south from glenageary?', {'entities': [(17, 27, 'STATION')]}),
              ('going north from glenageary?', {'entities': [(17, 27, 'STATION')]}),
              ('train heading north glenageary?', {'entities': [(20, 30, 'STATION')]}),
              ('dalkey staion north', {'entities': [(0, 6, 'STATION')]}),
              ('Show me dalkey', {'entities': [(8, 14, 'STATION')]}),
              ('Train from dalkey south', {'entities': [(11, 17, 'STATION')]}),
              ('Next train to dalkey north', {'entities': [(14, 20, 'STATION')]}),
              ('Where is dalkey south?', {'entities': [(9, 15, 'STATION')]}),
              ('train south from dalkey?', {'entities': [(17, 23, 'STATION')]}),
              ('going north from dalkey?', {'entities': [(17, 23, 'STATION')]}),
              ('train heading north dalkey?', {'entities': [(20, 26, 'STATION')]}),
              ('killiney staion north', {'entities': [(0, 8, 'STATION')]}),
              ('Show me killiney', {'entities': [(8, 16, 'STATION')]}),
              ('Train from killiney south', {'entities': [(11, 19, 'STATION')]}),
              ('Next train to killiney north', {'entities': [(14, 22, 'STATION')]}),
              ('Where is killiney south?', {'entities': [(9, 17, 'STATION')]}),
              ('train south from killiney?', {'entities': [(17, 25, 'STATION')]}),
              ('going north from killiney?', {'entities': [(17, 25, 'STATION')]}),
              ('train heading north killiney?', {'entities': [(20, 28, 'STATION')]}),
              ('shankill staion north', {'entities': [(0, 8, 'STATION')]}),
              ('Show me shankill', {'entities': [(8, 16, 'STATION')]}),
              ('Train from shankill south', {'entities': [(11, 19, 'STATION')]}),
              ('Next train to shankill north', {'entities': [(14, 22, 'STATION')]}),
              ('Where is shankill south?', {'entities': [(9, 17, 'STATION')]}),
              ('train south from shankill?', {'entities': [(17, 25, 'STATION')]}),
              ('going north from shankill?', {'entities': [(17, 25, 'STATION')]}),
              ('train heading north shankill?', {'entities': [(20, 28, 'STATION')]}),
              ('bray staion north', {'entities': [(0, 4, 'STATION')]}),
              ('Show me bray', {'entities': [(8, 12, 'STATION')]}),
              ('Train from bray south', {'entities': [(11, 15, 'STATION')]}),
              ('Next train to bray north', {'entities': [(14, 18, 'STATION')]}),
              ('Where is bray south?', {'entities': [(9, 13, 'STATION')]}),
              ('train south from bray?', {'entities': [(17, 21, 'STATION')]}),
              ('going north from bray?', {'entities': [(17, 21, 'STATION')]}),
              ('train heading north bray?', {'entities': [(20, 24, 'STATION')]}),
              ('greystones staion north', {'entities': [(0, 10, 'STATION')]}),
              ('Show me greystones', {'entities': [(8, 18, 'STATION')]}),
              ('Train from greystones south', {'entities': [(11, 21, 'STATION')]}),
              ('Next train to greystones north', {'entities': [(14, 24, 'STATION')]}),
              ('Where is greystones south?', {'entities': [(9, 19, 'STATION')]}),
              ('train south from greystones?', {'entities': [(17, 27, 'STATION')]}),
              ('going north from greystones?', {'entities': [(17, 27, 'STATION')]}),
              ('train heading north greystones?', {'entities': [(20, 30, 'STATION')]}),
              ('kilcoole staion north', {'entities': [(0, 8, 'STATION')]}),
              ('Show me kilcoole', {'entities': [(8, 16, 'STATION')]}),
              ('Train from kilcoole south', {'entities': [(11, 19, 'STATION')]}),
              ('Next train to kilcoole north', {'entities': [(14, 22, 'STATION')]}),
              ('Where is kilcoole south?', {'entities': [(9, 17, 'STATION')]}),
              ('train south from kilcoole?', {'entities': [(17, 25, 'STATION')]}),
              ('going north from kilcoole?', {'entities': [(17, 25, 'STATION')]}),
              ('train heading north kilcoole?', {'entities': [(20, 28, 'STATION')]})]

STRAIN_DATA = [('bray staion', {'entities': [(0, 4, 'STATION')]}),
               ('Show me bray', {'entities': [(8, 12, 'STATION')]}),
               ('Train from bray', {'entities': [(11, 15, 'STATION')]}),
               ('Next train bray', {'entities': [(11, 15, 'STATION')]}),
               ('Where is bray?', {'entities': [(9, 13, 'STATION')]})]


@plac.annotations(
    model=("Model name. Defaults to blank 'en' model.", "option", "m", str),
    new_model_name=("New model name for model meta.", "option", "nm", str),
    output_dir=("Optional output directory", "option", "o", Path),
    n_iter=("Number of training iterations", "option", "n", int))
def main(model=None, new_model_name='animal', output_dir=None, n_iter=20):
    """Set up the pipeline and entity recognizer, and train the new entity."""
    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank('en')  # create blank Language class
        print("Created blank 'en' model")

    # Add entity recognizer to model if it's not in the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner)
    # otherwise, get it, so we can add labels to it
    else:
        ner = nlp.get_pipe('ner')

    ner.add_label(LABEL)  # add new entity label to entity recognizer

    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):  # only train NER
        optimizer = nlp.begin_training()
        for itn in range(n_iter):
            random.shuffle(TRAIN_DATA)
            losses = {}
            for text, annotations in TRAIN_DATA:
                nlp.update([text], [annotations], sgd=optimizer, drop=0.35,
                           losses=losses)
            print(losses)

    # test the trained model
    test_text = 'Where is glenageary??'
    doc = nlp(test_text)
    print("Entities in '%s'" % test_text)
    for ent in doc.ents:
        print(ent.label_, ent.text)

        # save model to output directory
        # print(Path(output_dir))
        output_dir = os.getcwd()
        nlp.to_disk(output_dir)
        print('DONE')
        #     output_dir = Path(output_dir)
        #     if not output_dir.exists():
        #         output_dir.mkdir()
        #     nlp.meta['name'] = new_model_name  # rename model
        #     nlp.to_disk(output_dir)
        #     print("Saved model to", output_dir)
        #
        #     # test the saved model
        #     print("Loading from", output_dir)
        #     nlp2 = spacy.load(output_dir)
        #     doc2 = nlp2(test_text)
        #     for ent in doc2.ents:
        #         print(ent.label_, ent.text)


if __name__ == '__main__':
    plac.call(main)
