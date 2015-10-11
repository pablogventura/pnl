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
        self.tagset = tagset
        self.trans = trans
        self.out = out

    def tagset(self):
        """Returns the set of tags.
        """
        return self.tagset

    def trans_prob(self, tag, prev_tags):
        """Probability of a tag.
        tag -- the tag.
        prev_tags -- tuple with the previous n-1 tags (optional only if n = 1).
        """
        return self.trans[prev_tags][tag]

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
        ys = [tuple(y[i:i+3]) for i in range(len(y)-n+1)]
        p = 1
        for elem in ys:
            p *= self.trans_prob(elem[-1], elem[:2])
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
        ys = [tuple(y[i:i+3]) for i in range(len(y)-n+1)]
        p = 0
        for elem in ys:
            p += log2(self.trans_prob(elem[-1], elem[:2]))
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
        return p+t_prob

    def tag(self, sent):
        """Returns the most probable tagging for a sentence.
         sent -- the sentence.
        """
        tagset = self.tagset
        out = self.out
        ys = []
        for w in sent:
            xs = []
            for t in tagset:
                aux = out[t]
                if w in aux:
                    xs += [(t, aux[w])]
            ys.append(max(xs, key=lambda x: x[1])[0])
        return ys


class ViterbiTagger:

    def __init__(self, hmm):
        """
        hmm -- the HMM.
        """
        pass

    def tag(self, sent):
        """Returns the most probable tagging for a sentence.
        sent -- the sentence.
        """
        pass


class MLHMM(HMM):

    def __init__(self, n, tagged_sents, addone=True):
        """
        n -- order of the model.
        tagged_sents -- training sentences, each one being a list of pairs.
        addone -- whether to use addone smoothing (default: True).
        """
        self.n = n
        self.tw_counts = tw_counts = defaultdict(int)
        self.ngram_counts = ngram_counts = defaultdict(int)
        for sent in tagged_sents:
            for elem in tagged_sents:
                tw_counts[elem] += 1
            for j in range(n+1):
                # move along the sent saving all its j-grams
                for i in range(n-j, len(sent) - j + 1):
                    ngram = tuple(sent[i: i + j])
                    ngram_counts[ngram] += 1

    def tcount(self, tokens):
        """Count for an k-gram for k <= n.
        tokens -- the k-gram tuple.
        """
        return self.ngram_counts[tokens]

    def unknown(self, w):
        """Check if a word is unknown for the model.
        w -- the word.
        """
        """
        Todos los métodos de HMM.
        """
