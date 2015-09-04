"""Generate sentences from an n-gram model.

Usage:
  generate.py -i <file> -n <n>
  generate.py -h | --help

Options:
  -i <file>     Language model file.
  -n <n>        Number of sentences to generate.
  -h --help     Show this screen.
"""

from docopt import docopt
import pickle

from nltk.corpus import PlaintextCorpusReader

from languagemodeling.ngram import NGramGenerator


if __name__ == '__main__':
    opts = docopt(__doc__)

    # parse args
    n = int(opt['-n'])

    # load the trained model
    filename = opts['-o']
    trained_model = pickcle.load(open('filename','rb'))

    tr_model = NGramGenerator(trained_model)

    print("\r\nGenerando sentencias a partir de un modelo de %s-grama(s)"%n,"\r\n") 
    for i in range(n):
        tr_model.generate_sent()
    
