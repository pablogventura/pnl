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
        if not prev_tags:
            prev_tags = tuple()

        return self.trans[tuple(prev_tags)][tag]

    def out_prob(self, word, tag):
        """Probability of a word given a tag.
        word -- the word.
        tag -- the tag.
        """
        return self.out[tag][word]

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
                # check that we can go from t to word (ie,out_prob(word,t)>0.0)
                if t in hmm.out:
                    if word in hmm.out[t]:
                        prob = hmm.out_prob(word, t)
                        for prev_tags, (log2_prob, tag_sq) in self._pi[k-1].items():
                            # check that we can go from tag t given prev_tags
                            if prev_tags in hmm.trans:
                                if t in hmm.trans[prev_tags]:
                                    trans_p = hmm.trans_prob(t, prev_tags)
                                    # update prev tags
                                    prv_tgs = prev_tags[1:] + (t,)
                                    # compute new log2 prob
                                    l2p = log2_prob + log2(prob) + log2(trans_p)
                                    # is it the max?
                                    if prv_tgs not in self._pi[k] or \
                                       l2p > self._pi[k][prv_tgs][0]:
                                        self._pi[k][prv_tgs] = (l2p, tag_sq + [t])

        max_log2_prob = float('-inf')
        result = None
        for prev, (lp, tag_sent) in self._pi[len(sent)].items():
            # check it's a valid transition
            if prev in hmm.trans:
                if '</s>' in hmm.trans[prev]:
                    # get its probabilty
                    p = hmm.trans_prob('</s>', prev)
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
        self.tag_ngram_counts = tag_ngram_counts = defaultdict(int)
        self.e_counts = e_counts = defaultdict(int)
        self.t_counts = tag_dict = defaultdict(int)
        self.trans = trans = defaultdict(int)
        self.out = out = {}
        self.w_counts = word_dict = defaultdict(int)

        # sents only of tags
        sents_of_tags = []
        for tagged_sent in tagged_sents:
            ys = []
            if n > 1:
                ys = ['<s>'*(n-1)]
            for i in range(len(tagged_sent)):
                # sequence of tags
                wt_tpl = tagged_sent[i]
                e_counts[wt_tpl] += 1
                aux_tag = wt_tpl[1]
                aux_word = wt_tpl[0]
                word_dict[aux_word] += 1
                tag_dict[aux_tag] += 1
                ys.append(aux_tag)
            ys.append('</s>')
            sents_of_tags.append(ys)

        # tags_voc
        self.tag_set = set(tag_dict.keys())
        self.tag_voc_size = len(list(tag_dict.keys()))

        # list of sents, each one beign a list of tags
        for sent in sents_of_tags:
            for i in range(len(sent) - n + 1):
                # ngram of tags
                ngram = tuple(sent[i: i + n])
                tag_ngram_counts[ngram] += 1
                tag_ngram_counts[ngram[:-1]] += 1

        # transition dict
        for v in list(tag_ngram_counts.keys()):
            for tag in self.tag_set.union({'</s>'}):
                if addone:
                    aux_val = (tag_ngram_counts[v+(tag,)]+1) /\
                              (tag_ngram_counts[v]+self.tag_voc_size)
                else:
                    aux_val = tag_ngram_counts[v+(tag,)] / tag_ngram_counts[v]
                if aux_val:
                    if v in trans:
                        trans[v].update({tag: aux_val})
                    else:
                        trans[v] = {tag: aux_val}

        # out prob dict
        for tag in tag_dict.keys():
            for word in word_dict.keys():
                aux_val = e_counts[(word, tag,)] / tag_dict[tag]
                if aux_val:
                    if tag in out:
                        out[tag].update({word: aux_val})
                    else:
                        out[tag] = {word: aux_val}

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
        return w not in self.w_counts

    def out_prob(self, word, tag):
        if not self.unknown(word):
            return self.out[tag][word]
        else:
            return 1 / (len(list(self.word_counts.keys())))
