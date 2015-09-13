"""Train an n-gram model.

Usage:
  train.py -n <n> -o <file> [-m <model> [-g <gamma> -ad <n>]]
  train.py -h | --help

Options:
  -n <n>        Order of the model.
  -m <model>    Model to use [default: ngram]:
                  ngram: Unsmoothed n-grams.
                  addone: N-grams with add-one smoothing.
                  interpolated: an interpolated model.
  -o <file>     Output model file.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle
from nltk.corpus import PlaintextCorpusReader
from languagemodeling.ngram import NGram, AddOneNGram


if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the data
    sents = PlaintextCorpusReader('../languagemodeling/corpora/','training_corpus.txt').sents()
    # train the model
    n = int(opts['-n'])
    m = str(opts['-m'])
    if m == 'ngram':
        model = NGram(n, sents)
    elif m == 'addone':
        model = AddOneNGram(n, sents)
    else:
        raise ValueError('That model you are looking for, is not implemented yet...')
    # save it
    filename = opts['-o']
    f = open(filename, 'wb')
    pickle.dump(model, f)
    f.close()
