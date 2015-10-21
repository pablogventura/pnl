"""Train a sequence tagger.

Usage:
  train.py [-m <model>] [-n <n>] [-a <addone>] -o <file>
  train.py -h | --help

Options:
  -m <model>    Model to use [default: base]:
                  base: Baseline
  -n <n>        Order.
  -a <addone>   Whether to use addone or not [default: 1]
  -o <file>     Output model file.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle

from corpus.ancora import SimpleAncoraCorpusReader
from tagging.baseline import BaselineTagger
from tagging.hmm import MLHMM, HMM

models = {
    'base': BaselineTagger,
}


if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the data
    files = 'CESS-CAST-(A|AA|P)/.*\.tbf\.xml'
    corpus = SimpleAncoraCorpusReader('ancora/ancora-2.0/', files)
    sents = list(corpus.tagged_sents())

    # set parameters
    n = int(opts['-n'])

    m = opts['-m']
    addone_param = True

    if not int(opts['-a']):
        addone_param = False

    if m == 'BaselineTagger':
        modelo = BaselineTagger(sents)
    elif m == 'MLHMM':
        modelo = MLHMM(n=n, tagged_sents=sents, addone=addone_param)
    else:
        raise ValueError('That model you are looking for, is not implemented yet...')

    # save it
    filename = opts['-o']
    f = open(filename, 'wb')
    pickle.dump(modelo, f)
    f.close()
