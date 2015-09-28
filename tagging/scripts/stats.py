"""Print corpus statistics.

Usage:
  stats.py
  stats.py -h | --help

Options:
  -h --help     Show this screen.
"""
from docopt import docopt

from corpus.ancora import SimpleAncoraCorpusReader
from collections import defaultdict

if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the data
    corpus = SimpleAncoraCorpusReader('ancora/ancora-2.0/')
    sents = corpus.tagged_sents()
    w_counts = defaultdict(int)
    tag_counts = defaultic(set)
    for sent in sents:
        for s in sent:
            w_counts[s[0]] += 1
            tag_counts = 
    # vocabulary
    voc = set(counts.keys())
    # vocabulary of tags
    # compute the statistics
    print('sents: {}'.format(len(sents)))
