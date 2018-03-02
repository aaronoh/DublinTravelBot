import spacy
import os

ner = spacy.load(os.getcwd())

test_text = 'Where is dun laoghaire??'
doc = ner(test_text)
print("Entities in '%s'" % test_text)
for ent in doc.ents:
    print(ent.label_, ent.text)