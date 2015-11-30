from collections import defaultdict
from math import log2


class HMM:

    def __init__(self, n, tagset, trans, out):
        """
        n -- n-gram size.
        tagset -- set of tags.
        trans -- transition probabilities dictionary.
        out -- output probabilities dictionary.
        """
        self.n = n
        self.tag_set = tagset
        self.trans = trans
        self.out = out

    def tagset(self):
        """Returns the set of tags.
        """
        return self.tag_set

    def trans_prob(self, tag, prev_tags):
        """Probability of a tag.
        tag -- the tag.
        prev_tags -- tuple with the previous n-1 tags (optional only if n = 1).
        """
        result = 0
        if not prev_tags:
            prev_tags = tuple()
        if tuple(prev_tags) in self.trans:
            if tag in self.trans[tuple(prev_tags)]:
                result = self.trans[tuple(prev_tags)][tag]
        return result

    def out_prob(self, word, tag):
        """Probability of a word given a tag.
        word -- the word.
        tag -- the tag.
        """
        if word in self.out[tag]:
            return self.out[tag][word]
        else:
            return 0

    def tag_prob(self, y):
        """
        Probability of a tagging.
        Warning: subject to underflow problems.
        y -- tagging.
        """
        n = self.n

        y = ['<s>']*(n-1)+y+['</s>']

        # ngrams
        ys = [(y[i:i+n]) for i in range(len(y)-n+1)]

        p = 1
        for elem in ys:
            a = elem[-1]
            b = elem[:-1]
            p *= self.trans_prob(a, b)
        return p

    def prob(self, x, y):
        """
        Joint probability of a sentence and its tagging.
        Warning: subject to underflow problems.
        x -- sentence.
        y -- tagging.
        """
        t_prob = self.tag_prob(y)
        xy = list(zip(x, y))
        p = 1
        for elem in xy:
            p *= self.out_prob(elem[0], elem[1])
        return p*t_prob

    def tag_log_prob(self, y):
        """
        Log-probability of a tagging.
        y -- tagging.
        """

        n = self.n
        y = ['<s>']*(n-1)+y+['</s>']

        # ngrams
        ys = [(y[i:i+n]) for i in range(len(y)-n+1)]

        p = 0
        for elem in ys:
            a = elem[-1]
            b = elem[:-1]
            p += log2(self.trans_prob(a, b))
        return p

    def log_prob(self, x, y):
        """
        Joint log-probability of a sentence and its tagging.
        x -- sentence.
        y -- tagging.
        """
        t_prob = self.tag_log_prob(y)
        xy = list(zip(x, y))
        p = 0
        for elem in xy:
            p += log2(self.out_prob(elem[0], elem[1]))
        return p + t_prob

    def tag(self, sent):
        """Returns the most probable tagging for a sentence.
         sent -- the sentence.
        """
        v = ViterbiTagger(self)
        return v.tag(sent)


class ViterbiTagger:

    def __init__(self, hmm):
        """
        hmm -- the HMM.
        """
        self.hmm = hmm

    def tag(self, sent):
        """Returns the most probable tagging for a sentence.
        sent -- the sentence.
        """
        hmm = self.hmm
        n = hmm.n
        tagset = self.hmm.tagset()

        self._pi = {0: {(('<s>',) * (n - 1)): (0, [])}}

        for k in range(1, len(sent)+1):
            self._pi[k] = {}
            word = sent[k-1]

            for t in tagset:
                prob = self.hmm.out_prob(word, t)
                if prob:
                    for prev_tags, (log2_prob, tag_sq) in self._pi[k-1].items():
                        trans_p = hmm.trans_prob(t, prev_tags)
                        if trans_p:
                            # update prev tags
                            prv_tgs = (prev_tags + (t,))[1:]
                            # compute new log2 prob
                            l2p = log2_prob + log2(prob) + log2(trans_p)
                            # is it the max?
                            if prv_tgs not in self._pi[k] or \
                               l2p > self._pi[k][prv_tgs][0]:
                                self._pi[k][prv_tgs] = (l2p, tag_sq + [t])

        max_log2_prob = float('-inf')
        result = None
        for prev, (lp, tag_sent) in self._pi[len(sent)].items():
            p = hmm.trans_prob('</s>', prev)
            if p:
                new_lp = lp + log2(p)
                # update tag_sent candidate and actual max log2 prob
                if new_lp > max_log2_prob:
                    max_log2_prob = new_lp
                    result = tag_sent

        return result


class MLHMM(HMM):

    def __init__(self, n, tagged_sents, addone=True):
        """
        n -- order of the model.
        tagged_sents -- training sentences, each one being a list of pairs.
        addone -- whether to use addone smoothing (default: True).
        """
        self.n = n
        self.addone = addone
        self.e_counts = e_counts = defaultdict(int)
        self.trans = {}
        self.voc_size = 0
        self.tag_ngram_counts = tag_ngram_counts = defaultdict(int)
        self.tag_counts = tag_counts = defaultdict(int)
        self.out = out = defaultdict(int)
        self.word_list = set()

        for tagged_sent in tagged_sents:

            ys = []
            if n > 1:
                ys = ['<s>']*(n-1)
            for pair in tagged_sent:
                e_counts[pair] += 1
                word = pair[0]
                tag = pair[1]
                tag_counts[tag] += 1
                if not out[tag]:
                    out[tag] = defaultdict(int)
                out[tag][word] += 1
                self.word_list.add(word)
                ys.append(tag)
            ys.append('</s>')
            self.voc_size = len(self.word_list)
            for j in range(len(ys) - n + 1):
                ngram = tuple(ys[j: j + n])
                tag_ngram_counts[ngram] += 1
                tag_ngram_counts[ngram[:-1]] += 1
                if ngram[:-1] in self.trans:
                    self.trans[ngram[:-1]].update({ngram[-1]})
                else:
                    self.trans[ngram[:-1]] = {ngram[-1]}

            self.tag_set = set(tag_counts.keys())

    def tagset(self):
        return self.tag_set

    def tcount(self, tokens):
        """Count for an k-gram for k <= n.
        tokens -- the k-gram tuple.
        """
        return self.tag_ngram_counts[tokens]

    def unknown(self, w):
        """Check if a word is unknown for the model.
        w -- the word.
        """
        return w not in self.word_list

    def out_prob(self, word, tag):

        if self.unknown(word):
            return 1 / self.voc_size
        else:
            if word in self.out[tag]:
                n_counts = self.e_counts[(word, tag)]
                d_counts = self.tag_counts[tag]
                return n_counts / d_counts
            else:
                return 0

    def trans_prob(self, tag, prev_tags):
        """Probability of a tag.
        tag -- the tag.
        prev_tags -- tuple with the previous n-1 tags (optional only if n = 1).
        """
        if not prev_tags:
            prev_tags = tuple()
        addone = self.addone

        num_counts = self.tag_ngram_counts[tuple(prev_tags)+(tag,)]
        den_counts = self.tag_ngram_counts[tuple(prev_tags)]

        if addone:
            S = len(self.tag_set)
            return (num_counts + 1) / (den_counts + S)
        else:
            return num_counts / den_counts
