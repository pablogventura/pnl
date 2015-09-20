from nltk.corpus import PlaintextCorpusReader
import pickle
from ngram import *

sents = PlaintextCorpusReader('corpora/','austen-emma_training_data.txt').sents()
modelo = InterpolatedNGram(3,sents, gamma=4, addone=1)

f = open('archivo','wb')
pickle.dump(modelo,f)
