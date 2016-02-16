# https://docs.python.org/3/library/collections.html
from collections import defaultdict
from math import log
from random import random
from nltk.corpus import PlaintextCorpusReader as cr
import ipdb

#sents = cr('corpora/','shakespeare_original.txt').sents()

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
        # ngram condicional probs are based on relative counts
        hits = self.count((tuple(prev_tokens)+(token,)))
        sub_count = self.count(tuple(prev_tokens))

        return hits / float(sub_count)

    def sent_prob(self, sent):
        """Probability of a sentence. Warning: subject to underflow problems.
        sent -- the sentence as a list of tokens.
        """

        prob = 1.0
        sent = ['<s>']*(self.n-1)+sent+['</s>']

        for i in range(self.n-1, len(sent)):
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

        for i in range(self.n-1, len(sent)):
            c_p = self.cond_prob(sent[i], tuple(sent[i-self.n+1:i]))
            # to catch a math error
            if not c_p:
#                import ipdb; ipdb.set_trace()
                return float('-inf')
            prob += log(c_p, 2)

        return prob

    def perplexity(self, sents):
        """ Perplexity of a model.
        sents -- the test corpus as a list of sents
        """
        # total words seen
        M = 0
        for sent in sents:
            M += len(sent)
        # cross-entropy
        print('Computing perplexity on {} sents'.format(len(sents)))
        l = 0
        for j, sent in enumerate(sents):
            l += self.sent_log_prob(sent) / M
        return pow(2, -l)


class KneserNeyBaseNGram(NGram):
    def __init__(self, sents, n, D=None):

        self.n = n
        self.D = D
        # N1+(·w_<i+1>)
        self._N_dot_tokens_dict = N_dot_tokens = defaultdict(set)
        # N1+(w^<n-1> ·)
        self._N_tokens_dot_dict = N_tokens_dot = defaultdict(set)
        self._N_dot_tokens_dot_dict = N_dot_tokens_dot = defaultdict(set)
        self.counts = counts = defaultdict(int)
        vocabulary = []

        sents = list(map(lambda x: ['<s>']*(n-1) + x + ['</s>'], sents))

        if D is None:
            total_sents = len(sents)
            k = int(total_sents*9/10)
            training_sents = sents[:k]
            held_out_sents = sents[k:]
            training_sents = list(map(lambda x: ['<s>']*(n-1) + x + ['</s>'], training_sents))
            for sent in training_sents:
                for j in range(n+1):
                    for i in range(n-j, len(sent) - j + 1):
                        ngram = tuple(sent[i: i + j])
                        counts[ngram] += 1
                        if ngram:
                            if len(ngram) == 1:
                                vocabulary.append(ngram[0])
                            else:
                                right_token, left_token, right_kgram, left_kgram, middle_kgram =\
                                    ngram[-1:], ngram[:1], ngram[1:], ngram[:-1], ngram[1:-1]
                                N_dot_tokens[right_kgram].add(left_token)
                                N_tokens_dot[left_kgram].add(right_token)
                                if middle_kgram:
                                    N_dot_tokens_dot[middle_kgram].add(right_token)
                                    N_dot_tokens_dot[middle_kgram].add(left_token)
            if n -1:
                counts[('<s>',)*(n-1)] = len(sents)
            self.vocab = set(vocabulary)
            aux=0
            for w in self.vocab:
                aux += len(self._N_dot_tokens_dict[(w,)])
            self._N_dot_dot_attr = aux
            D_candidates = [i*0.12 for i in range(1,9)]
            xs = []
            for D in D_candidates:
                self.D = D
                aux_perplexity = self.perplexity(held_out_sents)
                xs.append( (D, aux_perplexity) )
            xs.sort(key=lambda x: x[1])
            self.D = xs[0][0]
            with open('kneserney_' + str(n) + '_parameters','a') as f:
                f.write('Order: {}\n'.format(self.n))
                f.write('D: {}\n'.format(self.D))
                f.write('Perplexity observed: {}\n'.format(xs[0][1]))
                f.write('-------------------------------\n')
            f.close()

        # discount value D provided
        else:
            for sent in sents:
                for j in range(n+1):
                    # all k-grams for 0 <= k <= n
                    for i in range(n-j, len(sent) - j + 1):
                        ngram = tuple(sent[i: i + j])
                        counts[ngram] += 1
                        if ngram:
                            if len(ngram) == 1:
                                vocabulary.append(ngram[0])
                            else:
                                # e.g., ngram = (1,2,3,4,5,6,7,8)
                                # right_token = (8,)
                                # left_token = (1,)
                                # right_kgram = (2,3,4,5,6,7,8)
                                # left_kgram = (1,2,3,4,5,6,7)
                                # middle_kgram = (2,3,4,5,6,7)
                                right_token, left_token, right_kgram, left_kgram, middle_kgram =\
                                    ngram[-1:], ngram[:1], ngram[1:], ngram[:-1], ngram[1:-1]
                                N_dot_tokens[right_kgram].add(left_token)
                                N_tokens_dot[left_kgram].add(right_token)
                                if middle_kgram:
                                    N_dot_tokens_dot[middle_kgram].add(right_token)
                                    N_dot_tokens_dot[middle_kgram].add(left_token)
            if n-1:
                counts[('<s>',)*(n-1)] = len(sents)
            self.vocab = set(vocabulary)

            aux=0
            for w in self.vocab:
                aux += len(self._N_dot_tokens_dict[(w,)])
            self._N_dot_dot_attr = aux

            xs = [k for k, v in counts.items() if v == 1 and n == len(k)]
            ys = [k for k, v in counts.items() if v == 2 and n == len(k)]
            n1 = len(xs)
            n2 = len(ys)
            self.D = n1 / (n1 + 2 * n2)

    def V(self):
        """
        returns the size of the vocabulary
        """
        return len(self.vocab)

    def N_dot_dot(self):
        """
        Returns the sum of N_dot_token(w) for all w in the vocabulary
        """
        return self._N_dot_dot_attr

    def N_tokens_dot(self, tokens):
        """
        Returns the count of unique words in which count(prev_tokens+word) > 0
        i.e., how many different ngrams it completes

        prev_token -- a tuple of strings
        """
        if type(tokens) is not tuple:
            raise TypeError('`tokens` has to be a tuple of strings')
        return len(self._N_tokens_dot_dict[tokens])

    def N_dot_tokens(self, tokens):
        """
        Returns the count of unique ngrams it completes

        tokens -- a tuple of strings
        """
        if type(tokens) is not tuple:
            raise TypeError('`tokens` has to be a tuple of strings')
        return len(self._N_dot_tokens_dict[tokens])

    def N_dot_tokens_dot(self, tokens):
        """
        Returns the count of unique ngrams it completes

        tokens -- a tuple of strings
        """
        if type(tokens) is not tuple:
            raise TypeError('`tokens` has to be a tuple of strings')
        return len(self._N_dot_tokens_dot_dict[tokens])

# Attemp 4, from
# https://west.uni-koblenz.de/sites/default/files/BachelorArbeit_MartinKoerner.pdf

class KneserNeyNGram(KneserNeyBaseNGram):
    def __init__(self, sents, n, D=None):
        super (KneserNeyNGram, self).__init__(sents=sents, n=n, D=D)

    def cond_prob(self, token, prev_tokens=tuple()):
        n = self.n
        # two cases:
        # 1) n == 1
        # 2) n > 1:
           # 2.1) k == 1
           # 2.2) 1 < k < n
           # 2.3) k == n

        # case 1)
        # heuristic
        # return (count(word) + 1) / (count() + |V|)
        if not prev_tokens and n == 1:
            return (self.count((token,)) +1 ) / (self.count(()) + self.V()*1)

        # case 2.1)
        # lowest ngram
        if not prev_tokens and n > 1:
            aux1 = self.N_dot_tokens((token,))
            aux2 = self.N_dot_dot()
            return (aux1 + 1 )/ (aux2 + self.V())

        # highest ngram
        if len(prev_tokens) == n-1:
            c = self.count(prev_tokens) + 1
            if c:
                t1 = max(self.count(prev_tokens+(token,)) - self.D, 0) / c
                t2 = self.D * max(self.N_tokens_dot(prev_tokens), 1) / c
                t3 = self.cond_prob(token, prev_tokens[1:])
                v = t1 + t2 * t3
 #               if not v:
#                    import ipdb;ipdb.set_trace()
                return t1 + t2 * t3
            else:
                return 0

        else:
  #          aux = 0
 #           for word in self.vocab:
#                aux += self.N_dot_tokens(prev_tokens+(word,))
            aux = max(self.N_dot_tokens_dot(prev_tokens),1)

            if aux:
                t1 = max(self.N_dot_tokens(prev_tokens+(token,)) - self.D, 0) / aux
                t2 = self.D * max(self.N_tokens_dot(prev_tokens),1) / aux
                t3 = self.cond_prob(token, prev_tokens[1:])
                return t1 + t2 * t3
            else:
                return 0





"""
########################################################################################################################
########################################################################################################################

# Attempt 1, from
# http://es.slideshare.net/mkrnr/introduction-to-kneserney-smoothing-on-top-of-generalized-language-models-for-next-word-prediction
class KN1(KN):
    def __init__(self, sents, n=3, D=0.5):
        super(KN1, self).__init__(sents, n, D)

    def cond_prob(self, token, prev_tokens=None):

        h_counts = self.count(prev_tokens+(token,))
        l_counts = self.count(prev_tokens)

        if not l_counts:
            return 0
            return (self.count((token,))+1) / (len(self.vocab()) + self.count(()))

        val1 = max( h_counts - self.D, 0) / l_counts

        val2 = self.D  / l_counts
        
        val3 = len(self.N_words_dot[prev_tokens])

        recursive_val = self.pknr(token,prev_tokens[1:])

        return val1 + val2 * val3 * recursive_val



    def pknr(self, token, prev_tokens):

        s = 0
        for word in self.vocab:
            s+=len(self.N_dot_words[prev_tokens+(word,)])

        if not prev_tokens:
#x            return (self.count((token,))+1) / (len(self.vocab()) + self.count(()))

            aux = len(self.N_dot_words[(token,)])
            return aux / s

        val1 = max(len(self.N_dot_words[prev_tokens+(token,)]) - self.D,0) / s

        val2 = self.D / s

        val3 = len(self.N_words_dot[prev_tokens])

        rec_val = self.pknr(token, prev_tokens[1:])

        return val1 + val2 * val3 * rec_val


# Attemp 2, from
# http://nlp.stanford.edu/~wcmac/papers/20050421-smoothing-tutorial.pdf

class KN2(KN):
    def __init__(self, sents, n=3, D=0.5):
        super(KN2, self).__init__(sents, n=n, D=D)


    def cond_prob(self, token, prev_tokens=tuple()):
        # unigrams
        if not prev_tokens:
            n1pls_dot_wrd = len(self.N_dot_words[(token,)])
            # heuristic...?
            return (n1pls_dot_wrd + 1) / self.aux1

        low_counts = self.count(prev_tokens)
        if not low_counts:
            low_counts = len(self.vocab)

        t1 = max(self.count(prev_tokens+(token,))-self.D,0) / low_counts
        t2 = self.D / low_counts
        t3 = len(self.N_words_dot[prev_tokens])
        # recursion
        t4 = self.cond_prob(token, prev_tokens[1:])
        return t1 + t2 * t3 * t4


# Attempt 3, from
# http://www.foldl.me/2014/kneser-ney-smoothing/
# Bigram only

class KN3(KN):
    def __init__(self, sents, n=3, D=0.5):
        super(KN3, self).__init__(sents=sents, n=n, D=D)

    def cond_prob(self, token, prev_tokens=tuple()):
        #n-1 gram counts
        lc = self.count(prev_tokens)
        result = self.D / len(self.vocab)
        if lc:
            t1 = max(self.count(prev_tokens+(token,))-self.D,0) / lc
            # normalizing constant
            lambda_ = self.get_lambda(prev_tokens)
            aux_0 = len(self.N_dot_words[(token,)])
            aux_1 = self.aux1
            result = t1 + lambda_ * aux_0 / aux_1
        return result

    def get_lambda(self, prev_tokens):
        c = self.count(prev_tokens)
        result = self.D / len(self.vocab)
        if c:
            result = len(self.N_words_dot[prev_tokens]) * self.D / c
        return result

########################################################################################################################
########################################################################################################################
"""
