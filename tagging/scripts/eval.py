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
import time

from corpus.ancora import SimpleAncoraCorpusReader
from collections import defaultdict


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
    print('Loading the data\n')
    a0 = time.time()
    # load the data
    files = '3LB-CAST/.*\.tbf\.xml'
    corpus = SimpleAncoraCorpusReader('ancora/ancora-2.0/', files)
    sents = list(corpus.tagged_sents())
    tagset = set()
    a1 = time.time()
    print('Data loaded. Time: {}\n'.format(a1-a0))
    print('Evaluating model: {}\n'.format(filename))
    # tag
    cnf_matrix = defaultdict(int)
    hits, total, unk_words, unk_hits, knw_words, knw_hits = 0, 0, 0, 0, 0, 0
    n = len(sents)
    for i, sent in enumerate(sents):
        word_sent, gold_tag_sent = zip(*sent)
        model_tag_sent = model.tag(word_sent)

        assert len(model_tag_sent) == len(gold_tag_sent), i

        for j in range(len(word_sent)):
            gold_t = gold_tag_sent[j]
            model_t = model_tag_sent[j]
            word = word_sent[j]
            known_word_flag = not model.unknown(word)
            hit_tag_flag = gold_t == model_t
            tagset.add(model_t)
            if known_word_flag:
                knw_words += 1
                if hit_tag_flag:
                    knw_hits += 1
            else:
                unk_words += 1
                if hit_tag_flag:
                    unk_hits += 1

            if not hit_tag_flag:
                cnf_matrix[(model_t, gold_t)] += 1

        # global score
        hits_sent = [m == g for m, g in zip(model_tag_sent, gold_tag_sent)]
        hits += sum(hits_sent)
        total += len(sent)
        acc = float(hits) / total

        progress('{:3.1f}% ({:2.2f}%)'.format(float(i) * 100 / n, acc * 100))
    print('')
    acc = float(hits) / total
    acc_unk = unk_hits / unk_words
    acc_knw = knw_hits / knw_words
    errs = total - unk_hits - knw_hits

    print('Accuracy: {:2.2f}%'.format(acc * 100))
    print('Accuracy in unknown words: {:2.2f}%'.format(acc_unk * 100))
    print('Accuracy in known words: {:2.2f}%'.format(acc_knw * 100))
    a2 = time.time()
    print('Evaluation finished. Time: {}\n'.format(round((a2-a1) / 60, 2)))

    # normalize
    for k, v in cnf_matrix.items():
        cnf_matrix[k] = v / errs
    # complete matrix with elements without errors
#    for t1 in tagset:
#        for t2 in tagset:
#            if not (t1, t2) in cnf_matrix:
#                cnf_matrix[(t1, t2)] = -1

    print("\nConfusion matrix elements:\n")
    print("\npair `(x, y)` means: tagged `x` when should have been tagged with `y`")
    print("\n(if a pair `(x, y)` it's not a matrix's element, means that\n",
          "a word `w` has never been tagged with `x` when it ",
          "should be tagged with `y`\n",
          "ie, the word `w` was tagged with `y` or `x` == `y`)\n")

    xs = []
    for elem in cnf_matrix.items():
        xs.append(elem)
    xs.sort()
    for k, v in xs:
        print (k, ':', v)
