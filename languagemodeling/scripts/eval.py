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
from nltk.corpus import PlaintextCorpusReader, brown, gutenberg

corpora = {
    'S': PlaintextCorpusReader('../languagemodeling/corpora/', 'test_corpus.txt').sents(),
    'G': gutenberg.sents(),
    'B': brown.sents(),
}
corp = {
    'S': 'Shakespeare',
    'G': 'Gutenberg',
    'B': 'Brown',
}
if __name__ == '__main__':
    opts = docopt(__doc__)

    # parse args
    # load the trained model
    filename = opts['-i']
    model = pickle.load(open(filename, 'rb'))
    c = model.corpus
    test_data = corpora[c]
    if c is not 'S':
        k = len(test_data)
        test_data = test_data[int(k*9/10):]

    print('\nEvaluating on {} corpus...\n'.format(corp[c]))
    print('Model type: NGram Model')
    try:
        print('Smoothing Technique: {}'.format(model.smoothingtechnique))
    except:
        pass
    print('Model Order: {}'.format(model.n))
    param, value = model.get_special_param()
    if param:
        print('Model Special Parameter {}: {}\n'.format(param, value))
    else:
        print('No Special Parameter for this Model / Smoothing Technique')
    print("Perplexity: {}\n".format(model.perplexity(test_data)))
    print("========================================================\n")
