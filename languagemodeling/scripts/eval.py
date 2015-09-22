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
from languagemodeling.ngram import NGram, AddOneNGram, InterpolatedNGram, BackOffNGram
from nltk.corpus import PlaintextCorpusReader


if __name__ == '__main__':
    opts = docopt(__doc__)

    # parse args
    # load the trained model
    filename = opts['-i']
    model = pickle.load(open(filename,'rb'))

    test_data = PlaintextCorpusReader('../languagemodeling/corpora/','test_corpus.txt').sents()[:100]

    print("perplexity: ",model.perplexity(test_data))
