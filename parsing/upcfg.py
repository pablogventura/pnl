from collections import defaultdict
from nltk.grammar import Production as P, ProbabilisticProduction as PP,\
    Nonterminal as N, induce_pcfg
from .cky_parser import CKYParser
from nltk.grammar import PCFG
from .util import lexicalize, unlexicalize
from .baselines import Flat
import copy

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
            t2 = copy.deepcopy(tree)
            # binarise productions
            t2.chomsky_normal_form()
            # get rid of unary nonterminal productions
            t2.collapse_unary(collapsePOS=True, collapseRoot=True)
            # unlexicalize
            unlexicalize(t2)
            productions = t2.productions()
            prods += productions

        self.prob_productions = induce_pcfg(start=N(start), productions=prods)

        self.parser = CKYParser(self.prob_productions)
        self.S = start

    def productions(self):
        """Returns the list of UPCFG probabilistic productions.
        """
        return self.prob_productions.productions()

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
