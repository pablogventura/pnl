"""Train an n-gram model.

Usage:
  train.py -n <n> -o <file> [-m <model>] [-b <n>] [-g <n>] [-a <n>]
  train.py -h | --help

Options:
  -n <n>        Order of the model.
  -m <model>    Model to use [default: ngram]:
                  ngram: Unsmoothed n-grams.
                  addone: N-grams with add-one smoothing.
                  interpolated: an interpolated model.
                  backoff: a backoff with discounting model
  -g <n>           The gamma parameter for the interpolated model [default: 0].
  -a <n>           For using addone within the model [default: 1].
  -b <n>           The beta parameter for the backoff model [default: 0].
  -o <file>     Output model file.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle
from nltk.corpus import PlaintextCorpusReader
from languagemodeling.ngram import NGram, AddOneNGram, InterpolatedNGram, BackOffNGram


if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the data
    sents = PlaintextCorpusReader('../languagemodeling/corpora/','austen-emma_training_data.txt').sents()[:400]
    # train the model
    addone_flag = int(opts['-a'])
    n = int(opts['-n'])
    m = str(opts['-m'])
    gamma_val = int(opts['-g'])
    beta_val = int(opts['-b'])



    if m == 'ngram':
        model = NGram(n, sents)
    elif m == 'addone':
        model = AddOneNGram(n, sents)
    elif m == 'interpolated':
        model = InterpolatedNGram(n, sents, gamma=gamma_val, addone=addone_flag)
    elif m == 'backoff':
        model = BackOffNGram(n, sents, beta=beta_val, addone=addone_flag)
    else:
        raise ValueError('That model you are looking for, is not implemented yet...')
    # save it
    filename = opts['-o']
    f = open(filename, 'wb')

    pickle.dump(model, f)
    f.close()
