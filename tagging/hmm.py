from collections import defaultdict
from math import log2
import itertools

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
        print(tag,prev_tags)
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
            p *= self.trans_prob(a,b)
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
            p += log2(self.trans_prob(a,b))
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
        v = ViterbiTagger(self)
        return v.tag(sent)


class ViterbiTagger:

    def __init__(self, hmm):
        """
        hmm -- the HMM.
        """
        self.hmm = hmm
        self.n = hmm.n
        self._pi = {0: {('<s>',)*(self.n-1): (log2(1.0), []), }}

    def tag(self, sent):
        """Returns the most probable tagging for a sentence.
        sent -- the sentence.
        """
        hmm = self.hmm
        n = hmm.n
        tagset = self.hmm.tagset()

        S = {}

        for i in range(1, n):
            # worked on first try, good for me
            S[i-n+1] = {'<s>'}
        S_0 = tagset.union({'<s>'})
        S_1 = tagset
        for j in range(1, len(sent)+1):
            S[j] = tagset

        pi = self._pi
        # possible very INEFFICIENCY
        comb = list(itertools.combinations(S_0,n-1))
        # n = 2
        print(S_0)
        print(S_1)
        print(comb)
        for k in range(1, len(sent)+1):
            for u in S[k-1]:

                for v in S[k]:
                    ys = []
                    for w in S[k-2]:
                        if (w, u) in hmm.trans:
                            # q(v|w,u)
                            if v in hmm.trans[(w, u)]:
                                # e(x_k|v)
                                if sent[k-1] in hmm.out[v]:
                                    # pi(k-1,w,u)
 
                                    if (w, u) in pi[k-1]:
                                        # pi[n][w1,w2] = (prob, tag)
                                        pi_values = pi[k-1][(w, u)]
                                        val = pi_values[0]
                                        tag = pi_values[1]
                                        q = hmm.trans_prob(v, (w, u))
                                        e = hmm.out_prob(sent[k-1], v)
                                        ys.append((val+log2(q)+log2(e), tag))

                    if ys:
                        print(ys)
                        aux_val = ys[0][0]
                        aux_tag = ys[0][1]
                        tag_sq = aux_tag+[v]
                        if k in pi:
                            pi[k].update({(u,v):(aux_val, tag_sq)})
                        else:
                            pi[k] = {(u,v):(aux_val, tag_sq)}
        print(pi)

        y_tags = max(list(pi[len(sent)].values()))[1]

        self._pi = pi
        return y_tags


class MLHMM(HMM):

    def __init__(self, n, tagged_sents, addone=True):
        """
        n -- order of the model.
        tagged_sents -- training sentences, each one being a list of pairs.
        addone -- whether to use addone smoothing (default: True).
        """

        self.n = n
        self.addone = addone
        self.q_num_counts = q_num_counts = defaultdict(int)
        self.q_den_counts = q_den_counts = defaultdict(int)
        self.e_counts = e_counts = defaultdict(int)
        self.t_counts = tag_dict = defaultdict(int)
        self.trans = trans = defaultdict(int)
        self.out = out = defaultdict(int)
        self.w_counts = word_dict = defaultdict(int)

        # sents only of tags
        zs = []
        for tagged_sent in tagged_sents:
            ys = []
            for i in range(len(tagged_sent)):
                # sequence of tags
                aux_tag = tagged_sent[i][1]
                aux_word = tagged_sent[i][0]
                word_dict[aux_word] += 1
                tag_dict[aux_tag] += 1
                ys.append(aux_tag)
            zs.append(ys)
        # tags_voc
        self.tag_set = {'</s>'}.union(set(tag_dict.keys()))

        # list of sents, each one beign a list of tags
        sents_of_tags = list(map((lambda x: x + ['</s>']), zs))
        sents_of_tags = list(map((lambda x: ['<s>']*(n-1) + x), sents_of_tags))




############ FIX INEFFICIENCY


        for sent in sents_of_tags:
            for i in range(len(sent) - n + 1):
                # ngram of tags
                ngram = tuple(sent[i: i + n])
                ############## UGLY A.F.
                q_num_counts[ngram] += 1
                q_den_counts[ngram] += 1
                q_den_counts[ngram[:-1]] += 1

        # transition dict
        for v in q_den_counts.keys():
            for tag in self.tag_set:
                aux_val = q_num_counts[v+(tag,)] /q_den_counts[v]
                if aux_val:
                    if v in trans:
                        trans[v].update({tag:aux_val})
                    else:
                        trans[v] = {tag:aux_val}

        for elem in tagged_sents:
            for tpl in elem:
                e_counts[tpl] += 1

        for tag in tag_dict.keys():
            for word in word_dict.keys():
                aux_val = e_counts[(word,tag,)] / tag_dict[tag]
                if aux_val:
                    if tag in out:
                        out[tag].update({word:aux_val})
                    else:
                        out[tag] = {word:aux_val}

    def tagset(self):
        return self.tag_set

    def tcount(self, tokens):
        """Count for an k-gram for k <= n.
        tokens -- the k-gram tuple.
        """
        return self.q_den_counts[tokens]
    def unknown(self, w):
        """Check if a word is unknown for the model.
        w -- the word.
        """
        return w not in self.w_counts
