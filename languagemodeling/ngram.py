# https://docs.python.org/3/library/collections.html
from collections import defaultdict
from math import log2
from random import random
import operator
from time import time

class NGram(object):

    def __init__(self, n, sents):
        """
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        """
        assert n > 0
        self.n = n
        self.counts = counts = defaultdict(int)

        sents = list(map((lambda x: ['<s>']*(n-1) + x), sents))
        sents = list(map((lambda x: x + ['</s>']), sents))

        for sent in sents:
            for i in range(len(sent) - n + 1):
                ngram = tuple(sent[i: i + n])
                counts[ngram] += 1
                counts[ngram[:-1]] += 1

    # Obsolete now
    def prob(self, token, prev_tokens=None):
        n = self.n
        if not prev_tokens:
            prev_tokens = []
        assert len(prev_tokens) == n - 1

        tokens = prev_tokens + [token]
        aux_count = self.counts[tuple(tokens)]
        return aux_count / float(self.counts[tuple(prev_tokens)])


# ##TODO###
    def count(self, tokens):
        """Count for an n-gram or (n-1)-gram.
        tokens -- the n-gram or (n-1)-gram tuple.
        """
        return self.counts[tokens]

    def cond_prob(self, token, prev_tokens=None):
        """Conditional probability of a token.
        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """

        if not prev_tokens:
            assert self.n == 1
            prev_tokens = tuple()

        hits = self.count((tuple(prev_tokens)+(token,)))
        sub_count = self.count(tuple(prev_tokens))

        return hits / float(sub_count)

    def sent_prob(self, sent):
        """Probability of a sentence. Warning: subject to underflow problems.
        sent -- the sentence as a list of tokens.
        """

        prob = 1.0
        sent = ['<s>']*(self.n-1)+sent+['</s>']

        for i in range(self.n-1, len(sent)-self.n+1):
            prob *= self.cond_prob(sent[i], tuple(sent[i-self.n+1:i]))
            if not prob:
                break

        return prob

    def sent_log_prob(self, sent):
        """Log-probability of a sentence.
        sent -- the sentence as a list of tokens.
        """

        prob = self.sent_prob(sent)
        if not prob:
            return float('-inf')
        return log2(prob)


class NGramGenerator(object):

    def __init__(self, model):
        """
        model -- n-gram model.
        """
        self.n = model.n
        self.probs = probs = dict()
        self.sorted_probs = dict()

        pre = [elem for elem in model.counts.keys() if not len(elem) == model.n]
        suf = [elem for elem in model.counts.keys() if len(elem) == model.n]
        # revisar, super ineficiente
        for prefix in pre:
            probs[prefix] = {sufix[-1]:model.cond_prob(sufix[-1],prefix) for sufix in suf if prefix==sufix[:-1]}


        aux1 = list(probs.keys())
        sp = [list(probs[x].items()) for x in aux1]

        self.sorted_probs = {aux1[i]:sorted(sp[i],key=lambda x: (-x[1], x[0])) for i in range(len(sp))}



    def generate_sent(self):
        """Randomly generate a sentence."""

        sent = ('<s>',)*(self.n-1)
        if self.n == 1:
            sent = ()
        while not '</s>' in sent:
            sent += (self.generate_token(sent[-self.n+1:]),)
        return sent[self.n-1:-1]

    def generate_token(self, prev_tokens=None):
        """Randomly generate a token, given prev_tokens.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """

        if self.n ==1:
            prev_tokens = tuple()
        p = random()
        res = ''
        choices = self.sorted_probs[prev_tokens]

        acc = choices[0][1]
        for i in range(0,len(choices)):

            if p < acc:
                res = choices[i][0]
                break
            else:
                acc += choices[i][1]
        return res



class AddOneNGram(object):

    def __init__(self, n, sents):
        """
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        """
 
        assert n > 0
        self.n = n
        self.counts = counts = defaultdict(int)
        self.voc = set()

        sents = list(map((lambda x: x + ['</s>']), sents))

        for s in sents:
            self.voc = self.voc.union(set(s))


        sents = list(map((lambda x: ['<s>']*(n-1) + x), sents))

        for sent in sents:
            for i in range(len(sent) - n + 1):
                ngram = tuple(sent[i: i + n])
                counts[ngram] += 1
                counts[ngram[:-1]] += 1

    def count(self, tokens):
        """Count for an n-gram or (n-1)-gram.
 
        tokens -- the n-gram or (n-1)-gram tuple.
        """
        return self.counts[tokens]

    def cond_prob(self, token, prev_tokens=None):
        """Conditional probability of a token.
 
        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        if not prev_tokens:
            assert self.n == 1
            prev_tokens = tuple()

        hits = self.count((tuple(prev_tokens)+(token,)))
        sub_count = self.count(tuple(prev_tokens))

        return (hits+1) / (float(sub_count)+len(self.voc))
 


    def V(self):
        """Size of the vocabulary.
        """
        return len(self.voc)
