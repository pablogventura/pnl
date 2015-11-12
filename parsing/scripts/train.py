"""Train a parser.

Usage:
  train.py [-m <model>] [-H <int>] -o <file>
  train.py -h | --help

Options:
  -m <model>    Model to use [default: flat]:
                  flat: Flat trees
                  rbranch: Right branching trees
                  lbranch: Left branching trees
  -H <int>      Horizontal Markovization order [default: -1].
  -o <file>     Output model file.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle

from corpus.ancora import SimpleAncoraCorpusReader

from parsing.baselines import Flat, RBranch, LBranch
from parsing.upcfg import UPCFG

models = {
    'flat': Flat,
    'rbranch': RBranch,
    'lbranch': LBranch,
    'upcfg': UPCFG,
}


if __name__ == '__main__':
    opts = docopt(__doc__)

    print('Loading corpus...')
    files = 'CESS-CAST-(A|AA|P)/.*\.tbf\.xml'
    corpus = SimpleAncoraCorpusReader('ancora/ancora-2.0/', files)

    print('Training model...')
    mopt = opts['-m']
    if mopt in models:
        if mopt == 'upcfg':
            H = int(opts['-H'])
            if H == -1:
                H = None
                model = models[opts['-m']](corpus.parsed_sents(),horzMarkov=H)
        else:
            model = models[opts['-m']](corpus.parsed_sents())

    else:
        print('\nThat model you are looking for, is not implemented... Yet...',
              '\n\nThe available models are: {}\n'.format(list(models.keys())))
        sys.exit()
    print('Saving...')
    filename = opts['-o']
    f = open(filename, 'wb')
    pickle.dump(model, f)
    f.close()
