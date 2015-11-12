from nltk.grammar import Nonterminal as N, induce_pcfg
from .cky_parser import CKYParser
from nltk import Tree
from .util import lexicalize, unlexicalize
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
            # unlexicalize
            unlexicalize(t2)
            # binarise productions
            t2.chomsky_normal_form()
            # get rid of unary nonterminal productions
            t2.collapse_unary(collapsePOS=True, collapseRoot=True)
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
        tags = []
        for w, t in tagged_sent:
            tags.append(t)
            sent.append(w)
        # parse by tag
        p, t = self.parser.parse(tags)
        if t is None:
            # Flat tree
            return Tree(self.S, [Tree(tag, [word]) for word, tag in tagged_sent])
        else:
            # return the words to the leaves
            t = lexicalize(t, sent)
            # return the tree to its original structure
            t.un_chomsky_normal_form()
        return t
