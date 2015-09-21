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

        return (hits+1) / (float(sub_count)+self.V())

    def V(self):
        """Size of the vocabulary.
        """
        return len(self.voc)


class InterpolatedNGram(NGram):

    def __init__(self, n, sents, gamma=None, addone=True):
        """
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        gamma -- interpolation hyper-parameter (if not given, estimate using
            held-out data).
        addone -- whether to use addone smoothing (default: True).
        """
        self.n = n

        self.gamma = gamma
        self.addone = addone
        self.voc = {'</s>'}
        self.counts = counts = defaultdict(int)
        self.lambda_list = []
        self.gamma_flag = True

        for s in sents:
            self.voc = self.voc.union(set(s))


        if gamma == 0 or gamma == None:
            self.gamma_flag = False

        # if not gamma given
        if not self.gamma_flag:
            total_sents = len(sents)
            aux = int(total_sents * 90 / 100)
            # 90 per cent por training
            train_sents = sents[:aux]
            # 10 per cent for perplexity (held out data)
            held_out_sents = sents[-total_sents+aux:]

            train_sents = list(map((lambda x: ['<s>']*(n-1) + x), train_sents))
            train_sents = list(map((lambda x: x + ['</s>']), train_sents))

            for sent in train_sents:
                for i in range(len(sent) - n + 1):
                    ngram = tuple(sent[i: i + n])
                    for k in range(0, n+1):
                        counts[ngram[:k]] += 1
            counts[('</s>',)]=len(train_sents)
            self.tocounts=counts

            # search for the gamma that gives best perplexity (the lower, the better)
            gamma_candidates = [i*300 for i in range(1,6)]
            # xs is a list with (gamma, perplexity)
            xs = []
            for aux_gamma in gamma_candidates:
                self.gamma = aux_gamma
                sents = train_sents
                aux_perx = self.perplexity(held_out_sents)
                xs.append( (aux_gamma, aux_perx) )
            print(xs)
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
        # ML_probs dict starts in 1
        for j in range(0,n):
            prob += ML_probs[j+1]*lambdas[j]
        return prob


    def V(self):
        """Size of the vocabulary.
        """
        return len(self.voc)



class BackOffNGram(NGram):

    def __init__(self, n, sents, beta=None, addone=True):
        """
        Back-off NGram model with discounting as described by Michael Collins.
 
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        beta -- discounting hyper-parameter (if not given, estimate using
            held-out data).
        addone -- whether to use addone smoothing (default: True).
        """
        self.n = n
        self.beta = beta
        self.beta_flag = True
        self.addone = addone
        self.voc = set()
        self.counts = counts = defaultdict(int)

        if beta == None:
            self.beta_flag = False

        # if no beta given, we compute it
        if not self.beta_flag:
            total_sents = len(sents)
            aux = int(total_sents * 90 / 100)
            # 90 per cent por training
            train_sents = sents[:aux]
            # 10 per cent for perplexity (held out data)
            held_out_sents = sents[-total_sents+aux:]

            train_sents = list(map((lambda x: ['<s>']*(n-1) + x), train_sents))
            train_sents = list(map((lambda x: x + ['</s>']), train_sents))

            for sent in train_sents:
                for i in range(len(sent) - n + 1):
                    ngram = tuple(sent[i: i + n])
                    for k in range(0, n+1):
                        counts[ngram[:k]] += 1
            counts[('</s>',)]=len(train_sents)
            self.tocounts = counts
            # search for the gamma that gives best perplexity (the lower, the better)
            beta_candidates = [round(i*0.1) for i in range(1,10)]
            # xs is a list with (beta, perplexity)
            xs = []
            for aux_beta in beta_candidates:
                self.beta = aux_beta
                self.sents = train_sents
                aux_perx = self.perplexity(held_out_sents)
                xs.append( (aux_beta, aux_perx) )
            xs.sort(key=lambda x: x[1])
            self.beta = xs[0][0]

        # now that we found beta, we initialize

        sents = list(map((lambda x: x + ['</s>']), sents))

        for s in sents:
            self.voc = self.voc.union(set(s))

        sents = list(map((lambda x: ['<s>']*(n-1) + x), sents))
        self.counts = counts = defaultdict(int)

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

    def count_star(self, tokens):
        """
        Discounting counts for counts > 0
        """
        return self.counts[tokens] - self.beta


    def A(self, tokens):
        """Set of words with counts > 0 for a k-gram with 0 < k < n.
 
        tokens -- the k-gram tuple.
        """

        if not tokens:
            tokens = []
        return {elem for elem in self.voc if self.count(tuple(tokens)+(elem,))}

    def B(self, tokens):
        """Set of words with counts = 0 for a k-gram with 0 < k < n.

        tokens -- the k-gram tuple.
        """
        return self.voc - self.A(tokens)

    def alpha(self, tokens):
        """Missing probability mass for a k-gram with 0 < k < n.
 
        tokens -- the k-gram tuple.
        """
        if not tokens:
            tokens = tuple()
        sum = 0
        A_set = self.A(tokens)

        for elem in A_set:
            sum += self.count_star(tuple(tokens)+(elem,)) / self.count(tuple(tokens))

        return 1 - sum


    def cond_prob(self, token, prev_tokens=None):
        """Conditional probability of a token.
        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """

        addone = self.addone
        n = self.n
        alpha = self.alpha(prev_tokens)
        if not prev_tokens:
            prev_tokens = []
        A_set = self.A(prev_tokens)
        B_set = self.B(prev_tokens)
        # if we can apply discountings
        # unigram case
        if not prev_tokens:
            result = self.count((token,)) / self.count(())
        # bigram (and recursive) case

        if len(prev_tokens)==1:

            if token in A_set:

                result = self.count_star(tuple(prev_tokens)+(token,)) / self.count(tuple(prev_tokens))
            
            else:
                # normalization factor (denominator)
                norm = 0
                for elem in B_set:

                    norm_hits = self.count((elem,))
                    norm_count = self.count(())
                    if addone:
                        norm_result = (norm_hits + 1 ) / (norm_count + self.V())
                    else:
                        norm_result = norm_hits / norm_count
                    norm += norm_result


                # numerator
                hits = self.count((token,))
                sub_count = self.count(())
                if addone:
                    numerator_result = (hits+1) / (sub_count+self.V())
                else:
                    numerator_result = hits / sub_count

                result = alpha * numerator_result / norm
                
        # recursive case for bigrams
        if len(prev_tokens) > 1:

            # recursive call

            q_D = self.cond_prob(token, prev_tokens[1:])
            denom_factor = self.denom(prev_tokens)
            if denom_factor:
                result = alpha * q_D / denom_factor
            else:

                result = 0
        return result


    def denom(self, tokens):
        """Normalization factor for a k-gram with 0 < k < n.
 
        tokens -- the k-gram tuple.
        """
        B_set = self.B(tokens)
        sum = 0

        for elem in B_set:
            sum += self.cond_prob(elem,tokens[1:])

        return sum

    def V(self):
        """Size of the vocabulary.
        """
        return len(self.voc)


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
