from nltk.tag.stanford import NERTagger
import os
java_path = "/Java/jdk1.8.0_45/bin/java.exe"
os.environ['JAVAHOME'] = java_path
st = NERTagger('../ner-model.ser.gz','../stanford-ner.jar')
tagging = st.tag(text.split())