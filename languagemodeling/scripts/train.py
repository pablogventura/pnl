"""Train an n-gram model.

Usage:
  train.py -n <n> -o <file> [-m <model>] [-d <float>] [-g <float>] [--addone <int>]
  train.py -h | --help

Options:
  -n <n>        Order of the model.
  -m <model>    Model to use [default: ngram]:
                  ngram: Unsmoothed n-grams.
  -d <float>    Discount value (0 <= d <= 1) [default: 0.1].
  -o <file>     Output model file.
  -g <float>    Gamma Parameter for Jelinek Mercer [default: 0].
  --addone <int> Whether to use addone in Jelinek Mercer or not [default: 0].
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle
from nltk.corpus import PlaintextCorpusReader, brown
from languagemodeling.ngram import NGram, KneserNeyNGram
from languagemodeling.oldngram import BackOffNGram, AddOneNGram 
from languagemodeling.kneserney import *
from languagemodeling.smoothing import AdditiveSmoothingNGram , GoodTuringNGram , JelinekMercerNGram 
import sys


if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the data
    sents = PlaintextCorpusReader('../languagemodeling/corpora/','training_corpus.txt').sents()
#    k = len(brown.sents())
 #   brown_training_data = brown.sents()[:int(k*9/10)]
    n = int(opts['-n'])
    m = opts['-m']
    models = {'ngram': NGram,
              'as': AdditiveSmoothingNGram,
              'gt': GoodTuringNGram,
              'jm': JelinekMercerNGram,
  #            'kn1': KN1,
 #             'kn2': KN2,
#              'kn3': KN3,
              'kn4': KN4,
          }
    addone = bool(opts['--addone'])
    gamma = int(opts['-g'])
    # set parameters
    d = float(opts['-d'])
    # create the model
    if m == 'ngram':
        model = NGram(n, sents=brown_training_data)
    elif m == 'ao':
        model = AddOneNGram(n=n, sents=brown_training_data,)
    elif m == 'as':
        model = AdditiveSmoothingNGram(n=n, sents=brown_training_data, delta=d)
    elif m == 'gt':
        model = GoodTuringNGram(n=n, sents=brown_training_data)
    elif m == 'jm':
        model = JelinekMercerNGram(n=n, sents=brown_training_data, gamma=gamma, addone=addone)
    elif m.startswith('kn'):
        model = models[m](sents, n=n, )
    else:
        print('\nThat model you are looking for, is not implemented... Yet...',
              '\nThe available models are:\n')
        for k,v in models.items():
            print('%r => %s' % (k, str(v)))
        sys.exit()
    # save it
    filename = opts['-o']
    f = open(filename, 'wb')
    pickle.dump(model, f)
    f.close()
