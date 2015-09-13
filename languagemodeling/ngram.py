# https://docs.python.org/3/library/collections.html
from collections import defaultdict
from math import log
from random import random
import operator

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

    # obsolete now...
    def prob(self, token, prev_tokens=None):
        n = self.n
        if not prev_tokens:
            prev_tokens = []
        assert len(prev_tokens) == n - 1

        tokens = prev_tokens + [token]
        aux_count = self.counts[tuple(tokens)]
        return aux_count / float(self.counts[tuple(prev_tokens)])

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

        prob = 0
        sent = ['<s>']*(self.n-1)+sent+['</s>']

        for i in range(self.n-1, len(sent)-self.n+1):
            c_p = self.cond_prob(sent[i], tuple(sent[i-self.n+1:i]))
            if not c_p:
                return float('-inf')
            prob += log(c_p,2)

        return prob

    def perplexity(self, sents):
        """ Perplexity of a model.
        sents -- the test corpus as a list of sents
        """

        M = 0
        for sent in sents:
            M += len(sent)

        l = 0.0

        for sent in sents:
            l += self.sent_log_prob(sent) / M

        return pow(2,-l)

class AddOneNGram(NGram):

    def __init__(self, n, sents):
        NGram.__init__(self, n, sents)
        self.voc = set()

        sents = list(map((lambda x: x + ['</s>']), sents))
        for s in sents:
            self.voc = self.voc.union(set(s))

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


class InterpolatedNGram(AddOneNGram):

    def __init__(self, n, sents, gamma=None, addone=True):
        """
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        gamma -- interpolation hyper-parameter (if not given, estimate using
            held-out data).
        addone -- whether to use addone smoothing (default: True).
        """
        self.n = n
        self.sents = sents
        self.gamma = gamma
        self.addone = addone
        self.voc = set(['</s>'])
        self.counts = counts = defaultdict(int)
        self.lambda_list = []
        self.gamma_flag = True

        for s in sents:
            self.voc = self.voc.union(set(s))


        if gamma == None:
            self.gamma_flag = False

        # if not gamma given
        if gamma == None:
            total_sents = len(sents)
            aux = int(total_sents * 90 / 100)
            # 90 per cent por training
            train_sents = sents[:aux]
            # 10 per cent for perplexity (held out data)
            held_out_sents = sents[-total_sents+aux:]

            train_sents = list(map((lambda x: ['<s>']*(n-1) + x), train_sents))
            train_sents = list(map((lambda x: x + ['</s>']), train_sents))
            print(train_sents)
            for sent in train_sents:
                for i in range(len(sent) - n + 1):
                    ngram = tuple(sent[i: i + n])
                    for k in range(0, n+1):
                        counts[ngram[:k]] += 1
            counts[('</s>',)]=len(train_sents)
            self.held_out_sents = counts
            print(counts)
            # search for the gamma that gives best perplexity (the lower, the better)
            gamma_candidates = [i*250 for i in range(1,15)]
            # xs is a list with (gamma, perplexity)
            xs = []
            for aux_gamma in gamma_candidates:
                self.gamma = aux_gamma
                self.sents = train_sents
                aux_perx = self.perplexity(held_out_sents)
                xs.append( (aux_gamma, aux_perx) )
            xs.sort(key=lambda x: x[1])
            self.gamma = xs[0][0]

        # now that we found gamma, we initialize

        self.counts = counts = defaultdict(int)
        sents = list(map((lambda x: ['<s>']*(n-1) + x), sents))
        sents = list(map((lambda x: x + ['</s>']), sents))

        for sent in sents:
            for i in range(len(sent) - n + 1):
                ngram = tuple(sent[i: i + n])
                # for each ngram, count its smaller parts, from right to left
                # eg, (u,v,w) saves: (u,v,w),(u,v),(w) and ()
                for k in range(0, n+1):
                    counts[ngram[:k]] += 1
                    # since the unigram ('</s>',), doesn't forms part of a greater k-gram
                    # we have to add it by hand
                counts[('</s>',)]=len(sents)


    def count(self, token):

        if self.gamma_flag:
            return self.counts[token]
        else:
            return self.held_out_sents[token]

    def cond_prob(self, token, prev_tokens=None):
        """Conditional probability of a token.
        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """

        addone = self.addone
        n = self.n
        gamma = self.gamma
        #
        if not prev_tokens:
            prev_tokens = []
            assert len(prev_tokens) == n - 1


        lambdas = []
        for i in range(0, n-1):
            # 1 - sum(previous lambdas)
            aux_lambda = 1 - sum(lambdas[:i])
            # counts
            counts_top = self.count(tuple(prev_tokens[i:n-1]))
            # counts plus gamma
            counts_w_gamma = self.count(tuple(prev_tokens[i:n-1])) + gamma
            # with fritas
            lambdas.append(aux_lambda * counts_top / counts_w_gamma)
        lambdas.append(1-sum(lambdas))


        ML_probs = dict()
        for i in range(0,n):
            if addone:

                hits = self.count((tuple(prev_tokens[i:])+(token,)))
                sub_count = self.count(tuple(prev_tokens[i:]))
                if not sub_count:
                    result = 0
                else:
                    result = (hits+1) / (float(sub_count)+len(self.voc))
            else:

                hits = self.count((tuple(prev_tokens[i:])+(token,)))
                sub_count = self.count(tuple(prev_tokens[i:]))
                if not sub_count:
                    result = 0
                else:
                    result = hits / float(sub_count)
            
            ML_probs[i+1] = result

        prob = 0

        for j in range(0,n):
            prob += ML_probs[j+1]*lambdas[j]
        return prob


class NGramGenerator(object):

    def __init__(self, model):
        """
        model -- n-gram model.
        """
        self.n = model.n
        self.probs = probs = dict()
        self.sorted_probs = dict()
        # pre, list of sentences with length n-1 (of a n-gram model)
        pre = [elem for elem in model.counts.keys() if not len(elem) == model.n]
        # suf, list of sentences with length n (of a n-gram model)
        suf = [elem for elem in model.counts.keys() if len(elem) == model.n]

        # FIX ME ASAP!!!!!
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
