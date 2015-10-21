"""Evaulate a tagger.

Usage:
  eval.py -i <file>
  eval.py -h | --help

Options:
  -i <file>     Tagging model file.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle
import sys

from corpus.ancora import SimpleAncoraCorpusReader


def progress(msg, width=None):
    """Ouput the progress of something on the same line."""
    if not width:
        width = len(msg)
    print('\b' * width + msg, end='')
    sys.stdout.flush()


if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the model
    filename = opts['-i']
    f = open(filename, 'rb')
    model = pickle.load(f)
    f.close()

    # load the data
    files = '3LB-CAST/.*\.tbf\.xml'
    corpus = SimpleAncoraCorpusReader('ancora/ancora-2.0/', files)
    sents = list(corpus.tagged_sents())

    # tag
    hits, total, unk_words, unk_hits, k_words, knw_hits = 0, 0, 0, 0, 0, 0
    n = len(sents)
    for i, sent in enumerate(sents):
        word_sent, gold_tag_sent = zip(*sent)
        model_tag_sent = model.tag(word_sent)
        print(model_tag_sent, gold_tag_sent, i)
        assert len(model_tag_sent) == len(gold_tag_sent), i
        for elem in sent:
            w = elem[0]
            t = elem[1]
            t_word = model.tag_word(w)
            if model.unknown(w):
                unk_words += 1
                if t_word == t:
                    unk_hits += 1
            else:
                k_words += 1
                if t_word == t:
                    knw_hits += 1
        # global score
        hits_sent = [m == g for m, g in zip(model_tag_sent, gold_tag_sent)]
        hits += sum(hits_sent)
        total += len(sent)
        acc = float(hits) / total

        progress('{:3.1f}% ({:2.2f}%)'.format(float(i) * 100 / n, acc * 100))
    print('')
    acc = float(hits) / total
    acc_unk = unk_hits / unk_words
    acc_knw = knw_hits / k_words
    print('Accuracy: {:2.2f}%'.format(acc * 100))
    print('Accuracy in unknown words: {:2.2f}%'.format(acc_unk * 100))
    print('Accuracy in known words: {:2.2f}%'.format(acc_knw * 100))
