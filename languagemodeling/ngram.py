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

    # Obsolete now
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
        if not sub_count:
            print("Hey, you!\r\n")
            print(self.n, self.counts)
            print("\r\n sub count for ngram \r\n", prev_tokens)

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
        if not sub_count:
            print("\r\n sub count for addonengram \r\n", prev_tokens)
        return (hits+1) / (float(sub_count)+len(self.voc))

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

        prob = 0.0
        sent = ['<s>']*(self.n-1)+sent+['</s>']

        for i in range(self.n-1, len(sent)-self.n+1):

            prob += log(self.cond_prob(sent[i], tuple(sent[i-self.n+1:i])),2)

        return prob

    def V(self):
        """Size of the vocabulary.
        """
        return len(self.voc)


class InterpolatedNGram(object):

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

        if not gamma == None:

            # create the models
            if addone:
                self.models_dict = {i:AddOneNGram(i, sents) for i in range(2,n+1)}
            else:
                self.models_dict = {i:NGram(i, sents) for i in range(2,n+1)}
            # models_list holds n models, being the first, a AddOneNGram of order 1
            self.models_dict[1]=AddOneNGram(1, sents)
            for j in range(1,n+1):
                print("printing models\r\n")
                print(j,self.models_dict[j].counts)
        # if no gamma given, estimate it from held out data
        # let's search for gamma !
        else:
            total_sents = len(sents)
            aux = round(total_sents * 90 / 100)
            # 90 per cent por training
            train_sents = sents[:aux]
            # 10 per cent for perplexity
            held_out_sents = sents[-total_sents+aux:]

            # create the models
            if addone:
                self.models_dict = {i:AddOneNGram(i,train_sents) for i in range(2,n+1)}
            else:
                self.models_dict = {i:NGram(i,train_sents) for i in range(2,n+1)}
            # models_list holds n models, being the first, a AddOneNGram of order 1
            self.models_dict[1]=AddOneNGram(1, train_sents)


            gamma_list = [i*500 for i in range(1,11)]
            gamma_perx_list = []
            # for each gamma candidate, we compute
            # its perplexity against the
            # held out data
            for aux_gamma in gamma_list:

                M = 0
                for sent in held_out_sents:
                    M += len(sent)
                    l = 0.0

                for sent in held_out_sents:
                    l+=self.sent_log_prob(sent)
                perx = pow(2,-l)
                gamma_perx_list.append((aux_gamma, perx))

            gamma_perx_list.sort(key=lambda x:x[1])

            gamma = gamma_perx_list[0][0]
        self.counts = counts = defaultdict(int)

        sents = list(map((lambda x: ['<s>']*(n-1) + x), sents))
        sents = list(map((lambda x: x + ['</s>']), sents))


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

        models = self.models_dict
        n = self.n
        gamma = self.gamma
        # if gamma given

        lambdas = []
        for i in range(0, n-1):
            # list of lambdas, first corresponded with higher ngram model
            # i.e., lambdas[0] is for the n-gram model, lambdas[1] for n-1)-gram model
            # and so on...
            lambdas.append((1-sum(lambdas[:i])) * models[n-i].count(tuple(prev_tokens[i:n-1])) / \
                           (models[n-i].count(tuple(prev_tokens[i:n-1])) + gamma))
        lambdas.append(1-sum(lambdas))

        xs = []
        for i in range(0,n):
            q = models[n-i].cond_prob(token, prev_tokens)
            xs.append(lambdas[i]*q)

        return sum(xs)


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
