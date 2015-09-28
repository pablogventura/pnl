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
import time
if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the data
    corpus = SimpleAncoraCorpusReader('ancora/ancora-2.0/')
    sents = corpus.tagged_sents()
    w_counts = defaultdict(int)
    t_counts = defaultdict(int)
    tag_dict = dict()
    a = time.time()

    for sent in sents:
        for s in sent:
            word = s[0]
            tag = s[1]
            w_counts[word] += 1
            if tag in tag_dict:
                if word in tag_dict[tag]:
                    tag_dict[tag][word] += 1
                else:
                    tag_dict[tag].update({word:1})
            else:
                tag_dict[tag] = {word: 1}

    # compute the statistics
    print('sents: {}'.format(len(sents)))
    print('word counts: {}'.format(sum(w_counts.values())))
    print('vocabulary size: {}'.format(len(w_counts)))
    print('tag vocabulary size: {}'.format(len(tag_dict)))
    print('time: {}'.format(time.time()-a))
