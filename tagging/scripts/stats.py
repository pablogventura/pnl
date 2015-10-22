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

    sents = list(corpus.tagged_sents())

    w_counts = defaultdict(int)
    t_counts = defaultdict(int)
    tag_dict = dict()
    # to check tags ambiguity
    word_dict = dict()

    for sent in sents:
        for s in sent:
            word = s[0]
            tag = s[1]
            w_counts[word] += 1
            t_counts[tag] += 1
            # for tags ambiguity
            if word in word_dict:
                if tag in word_dict[word]:
                    word_dict[word][tag] += 1
                else:
                    word_dict[word].update({tag: 1})
            else:
                word_dict[word] = {tag: 1}
            # words associated to a particular tag
            if tag in tag_dict:
                if word in tag_dict[tag]:
                    tag_dict[tag][word] += 1
                else:
                    tag_dict[tag].update({word: 1})
            else:
                tag_dict[tag] = {word: 1}
    # words associated to a particular tag
    sorted_tags_words = dict()
    for tag, dict_words in tag_dict.items():
        sorted_tags_words[tag] = sorted(list(dict_words.items()),
                                        key=lambda x: -x[1])
    sorted_tags = sorted(list(t_counts.items()), key=lambda x: -x[1])
    # tags associated to a particualr word
    sorted_words_tags = dict()
    for word, dict_tags in word_dict.items():
        sorted_words_tags[word] = sorted(list(dict_tags.items()),
                                         key=lambda x: -x[1])
    sorted_words = sorted(list(w_counts.items()), key=lambda x: -x[1])

    # compute the statistics
    wrd_cnt = sum(w_counts.values())
    print('sents: {}'.format(len(sents)))
    print('word counts: {}'.format(wrd_cnt))
    print('vocabulary size: {}'.format(len(w_counts)))
    print('tag vocabulary size: {}'.format(len(tag_dict)))

    print('\r\nlos 10 tags más frecuentes: ')
    for i in range(10):
        tag_tpl = sorted_tags[i]
        tag = tag_tpl[0]
        tag_frq = tag_tpl[1]
        tag_prc = tag_frq / wrd_cnt
        print('\r\nen el puesto número {0}, el tag `{1}` aparece un total de {2} veces; \
        \ncon un porcentaje total de {3}. Sus lemas más frecuentes son:\r\n'.
              format(i + 1, tag, tag_frq, round(100*tag_prc, 3)))
        tagged_words = sorted_tags_words[tag][:5]
        for tw in tagged_words:
            print('el lema `{0}`, con una frecuencia de {1}'.format(tw[0], tw[1]))

    for m in range(1, 10):
        # in each step, xs is a list with all the keys that have 'm' tags
        xs = [elem for elem in w_counts.keys() if len(sorted_words_tags[elem]) == m]
        # fr_xs is a list with tuple (total quantity of a given word w, w)
        fr_xs = [(w_counts[w], w) for w in xs]
        fr_xs.sort(key=lambda x: -x[0])

        aux = min(5, len(xs))
        if aux:
            acc = 0
            for w in fr_xs:
                acc += w[0]
            print('\r\ncon {} tag(s) hay {} lemas; los más frecuentes son:\r\n'.format(m, len(xs)))
            for j in range(0, aux):
                occr = fr_xs[j][0]
                w = fr_xs[j][1]
                print('el lema `{}`, con {} ocurrencias y un porcentaje de {}'.
                      format(w, occr, round(occr*100/acc, 4)))
        else:
            print('\r\nno hay lemas con {} tags'.format(m))
