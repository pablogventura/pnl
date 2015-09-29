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
            t_counts[tag] += 1
            if tag in tag_dict:
                if word in tag_dict[tag]:
                    tag_dict[tag][word] += 1
                else:
                    tag_dict[tag].update({word:1})
            else:
                tag_dict[tag] = {word: 1}
    sorted_tags_words = dict()
    for tag,dict_words in tag_dict.items():
        sorted_tags_words[tag] = sorted(list(dict_words.items()),key=lambda x:-x[1])


    sorted_tags = sorted(list(t_counts.items()),key=lambda x:-x[1])
    # compute the statistics
    wrd_cnt = sum(w_counts.values())
    print('sents: {}'.format(len(sents)))
    print('word counts: {}'.format(wrd_cnt))
    print('vocabulary size: {}'.format(len(w_counts)))
    print('tag vocabulary size: {}'.format(len(tag_dict)))
    print('time: {}'.format(time.time()-a))

    print('\r\nlos 10 tags más frecuentes: ')
    for i in range(10):
        tag_tpl = sorted_tags[i]
        tag = tag_tpl[0]
        tag_frq = tag_tpl[1]
        tag_prc = tag_frq / wrd_cnt
        print('\r\nen el puesto número {0}, el tag `{1}` aparece un total de {2} veces; con un porcentaje total de {3}.\r\n'.format(i+1,tag,tag_frq,round(tag_prc,4)))
        tagged_words = sorted_tags_words[tag][:5]
        print('las 5 palabras más frecuentes con la etiqueta `{0}`\r\n'.format(tag))
        for tw in tagged_words:
            print('la palabra `{0}` con una frecuencia de {1}'.format(tw[0],tw[1]))
