"""Evaulate a language model using the test set.

Usage:
  eval.py -i <file>
  eval.py -h | --help

Options:
  -i <file>     Language model file.
  -h --help     Show this screen.
"""

from docopt import docopt
import pickle

from languagemodeling.kneserney import *
from nltk.corpus import PlaintextCorpusReader, brown


if __name__ == '__main__':
    opts = docopt(__doc__)

    # parse args
    # load the trained model
    filename = opts['-i']
    model = pickle.load(open(filename,'rb'))

    test_data = PlaintextCorpusReader('../languagemodeling/corpora/','test_corpus.txt').sents()

#    k = len(brown.sents())
 #   brown_test_data = brown.sents()[int(k*9/10):]
    try:
        print('Smoothing Technique: {}'.format(model.smoothingtechnique))
    except:
        pass
    print('Model order: {}'.format(model.n))
    try:
        d = model.D
    except:
        d = None
        pass
    print('Model delta: {}'.format(d))



    print("perplexity: ",model.perplexity(test_data))
