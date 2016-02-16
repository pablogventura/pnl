"""Train an n-gram model.

Usage:
  train.py -n <n> -o <file> [-m <model>] [-D <float>] [-g <float>] [--addone <int>] [-b <float>] [-c <str>]
  train.py -h | --help

Options:
  -n <n>        Order of the model.
  -m <model>    Model to use [default: ngram]:
                  ngram: Unsmoothed n-grams.
                  addone: N-grams with add-one smoothing.
                  interpolated: an interpolated model.
                  backoff: a backoff with discounting model
  --addone <int>    Whether to use addone in BackOff or not [default: 1].
  -D <float>    Discount value (0 <= d <= 1) [default: 0.0].
  -b <float>           The beta parameter for the backoff model [default: 0].
  -o <file>     Output model file.
  -g <float>    Gamma Parameter for Interpolated Model [default: 0].
  -c <str>      Choose corpus. S for Shakespeare, B for Brown, G for Gutenberg [default: S].
  -h --help     Show this screen.
"""
from languagemodeling.ngram import NGram, AddOneNGram, InterpolatedNGram, BackOffNGram, KneserNeyNGram
from nltk.corpus import PlaintextCorpusReader, brown, gutenberg
from docopt import docopt
import pickle
import sys

corpora = {
    'S': PlaintextCorpusReader('../languagemodeling/corpora/', 'training_corpus.txt').sents(),
    'B': brown.sents(),
    'G': gutenberg.sents(),
}
corp = {
    'S': 'Shakespeare',
    'G': 'Gutenberg',
    'B': 'Brown',
}
m_dict = {
    'ngram': 'NGram',
    'kz': 'BackOffNGram',
    'in': 'InterpolatedNGram',
    'ao': 'AddOneNGram',
    'kn': 'KneserNeyNGram',
}
if __name__ == '__main__':
    opts = docopt(__doc__)
    # load the data
    corpus = str(opts['-c'])
    sents = corpora[corpus]
    if corpus is not 'S':
        k = len(sents)
        sents = sents[:int(k*9/10)]
    # Parse args
    n = int(opts['-n'])
    m = opts['-m']
    beta = float(opts['-b'])
    models = {
        'ngram': NGram,
        'kz': BackOffNGram,
        'in': InterpolatedNGram,
        'ao': AddOneNGram,
        'kn': KneserNeyNGram,
    }
    addone = bool(opts['--addone'])
    gamma = int(opts['-g'])
    if not gamma:
        gamma = None
    # set parameters
    D = float(opts['-D'])
    if not D:
        D = None
    if not beta:
        beta = None
    # create the model
    if m not in models:
        print('\nThat Model you are looking for, is not implemented... Yet...',
              '\nThe available Models are:\n')
        for k, v in m_dict.items():
            print('%r => %s' % (k, str(v)))
        sys.exit()

    print('\nTraining {} Model of Order {}, on {} Corpus...\n'.format(m_dict[m], n, corp[corpus]))

    if m == 'ngram':
        model = NGram(n, sents=sents, corpus=corpus)
    elif m == 'ao':
        model = AddOneNGram(n=n, sents=sents, corpus=corpus)
    elif m == 'in':
        model = InterpolatedNGram(n=n, sents=sents, gamma=gamma, addone=addone, corpus=corpus)
    elif m == 'kz':
        model = BackOffNGram(n=n, sents=sents, beta=beta, addone=addone, corpus=corpus)
    elif m == 'kn':
        model = KneserNeyNGram(sents, n=n, D=D, corpus=corpus)

    # save it
    filename = opts['-o']
    f = open(filename, 'wb')
    pickle.dump(model, f)
    f.close()
