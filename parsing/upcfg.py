from collections import defaultdict
from nltk.grammar import Production as P, ProbabilisticProduction as PP,\
    Nonterminal as N
from .cky_parser import CKYParser
from nltk.grammar import PCFG
from .util import lexicalize
from .baselines import Flat


class UPCFG:
    """Unlexicalized PCFG.
    """

    def __init__(self, parsed_sents, start='sentence'):
        """
        parsed_sents -- list of training trees.
        """

        # list of all productions in training trees
        prods = []
        for tree in parsed_sents:
            productions = tree.productions()
            for e in productions:
                lhs = e.lhs()
                rhs = e.rhs()
                if e.is_lexical():
                    p = P(lhs, [str(lhs)])
                    prods.append(p)
                else:
                    a1, a2 = rhs
                    prods.append(P(lhs, [a1, a2]))

        self.counts = counts = defaultdict(int)
        for prd in prods:
            lhs = prd.lhs()
            rhs = prd.rhs()
            counts[lhs] += 1
            counts[rhs] += 1

        self.upgfs = []
        for prod in prods:
            l = prod.lhs()
            r = prod.rhs()
            p = counts[r] / counts[l]
            if prod.is_lexical():
                up = PP(l, [r[0]], prob=p)
            else:
                up = PP(l, [r[0], r[1]], prob=p)
            if up not in self.upgfs:
                self.upgfs.append(up)

        self.parser = CKYParser(PCFG(N(start), self.upgfs))
        self.S = start

    def productions(self):
        """Returns the list of UPCFG probabilistic productions.
        """
        return self.upgfs

    def parse(self, tagged_sent):
        """Parse a tagged sentence.
        tagged_sent -- the tagged sentence (a list of pairs (word, tag)).
        """
        sent = []
        tag = []
        for w, t in tagged_sent:
            tag.append(t)
            sent.append(w)

        p, t = self.parser.parse(tag)

        if t is None:
            return Flat(None, self.S).parse(tagged_sent)

        return lexicalize(t, sent)
