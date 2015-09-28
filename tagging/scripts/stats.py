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
    tag_counts = dict()
    a = time.time()
    for sent in sents:
        for s in sent:
            aux_word = s[0]
            tag = s[1]
            w_counts[aux_word] += 1
            if tag in tag_counts:
                if aux_word in tag_counts[tag]:
                    aux = tag_counts[aux_tag]
                    tag_counts[tag] = {aux_word: list(aux.values())[0]+1}
                else:
                    sw = tag_counts[tag]
                    tag_counts[tag] = {aux_word: 1}
                    tag_counts[tag].update(sw)
            else:
                tag_counts[tag] = {aux_word: 1}

    # compute the statistics
    print('sents: {}'.format(len(sents)))
    print('word counts: {}'.format(sum(w_counts.values())))
    print('vocabulary size: {}'.format(len(w_counts)))
    print('tag vocabulary size: {}'.format(len(tag_counts)))
    print('time: {}'.format(time.time()-a))
    s = 0
    for elem in list(tag_counts.values()):
        s += sum(list(elem.values()))
    print('cosa: {}'.format(s))
    print('pepe: {}'.format(len(pepe)))
