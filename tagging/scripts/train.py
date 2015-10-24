"""Train a sequence tagger.

Usage:
  train.py [-m <model>] [-c <classifier>] [-n <n>] [-a <addone>] -o <file>
  train.py -h | --help

Options:
  -m <model>    Model to use [default: base]:
                  base: Baseline
  -c <classifier> Classifier to use if model is MEMM [default: lr].
  -n <n>        Order [default: 1].
  -a <addone>   Whether to use addone or not [default: 1]
  -o <file>     Output model file.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle
import sys

from corpus.ancora import SimpleAncoraCorpusReader
from tagging.baseline import BaselineTagger
from tagging.hmm import MLHMM
from tagging.memm import MEMM

models = {
    'base': BaselineTagger,
    'mlhmm': MLHMM,
    'memm': MEMM,
}


if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the data
    files = 'CESS-CAST-(A|AA|P)/.*\.tbf\.xml'
    corpus = SimpleAncoraCorpusReader('ancora/ancora-2.0/', files)
    sents = list(corpus.tagged_sents())

    m = str(opts['-m'])
    n = int(opts['-n'])
    c = str(opts['-c'])
    addone_arg = True
    if not opts['-a']:
        addone_arg = False

    if m == 'base':
        modelo = BaselineTagger(sents)
    elif m == 'mlhmm':
        modelo = MLHMM(n=n, tagged_sents=sents, addone=addone_arg)
    elif m == 'memm':
        modelo = MEMM(n=n, tagged_sents=sents, classifier=c)        
    else:
        print('\nThat model you are looking for, is not implemented... Yet...',
              '\n\nThe available models are: {}\n'.format(list(models.keys())))
        sys.exit()

    # save it
    filename = opts['-o']
    f = open(filename, 'wb')
    pickle.dump(modelo, f)
    f.close()
