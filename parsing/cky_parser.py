from nltk import Tree
from collections import defaultdict

class CKYParser:

    def __init__(self, grammar,):
        """
        grammar -- a binarised NLTK PCFG.
        """
        self.productions = grammar.productions()
        self.prods = defaultdict(list)
        self.q = {}
        self.start = grammar.start().symbol()

        self.lex_N = {str(elem.lhs()) for elem in self.productions
                      if elem.is_lexical()}

        # inverse dict: for a production X -> Y Z [prob],
        # we save (Y, Z) as a key and (X, prob) as a value
        for p in self.productions:
            t = (str(p.lhs()), p.logprob())
            self.prods[tuple(str(t) for t in p.rhs())].append(t)
        # dict of productions
        for prod in self.productions:
            lhs = str(prod.lhs())
            rhs = tuple(list(map(str, prod.rhs())))
            lp = prod.logprob()
            if lhs in self.q:
                self.q[lhs].update({rhs: lp})
            else:
                self.q[lhs] = {rhs: lp}

    def parse(self, sent):
        """Parse a sequence of terminals.
        sent -- the sequence of terminals.
        """

        q = self.q
        lex_N = self.lex_N
        S = self.start

        n = len(sent)
        self._pi = {}
        self._bp = {}

        # INIT
        # X -> Y Z productions
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                self._pi[(i, j)] = {}
                self._bp[(i, j)] = {}

        # X -> a productions
        for i in range(1, n + 1):
            w = sent[i - 1]
            for nt in lex_N:
                if (w,) in q[nt]:
                    lp = q[nt][(w,)]
                    # for ambiguous productions in case a word has to POS tags
                    # (check if really necessary)
                    if (i, i) in self._pi:
                        self._pi[(i, i)].update({nt: lp})
                        self._bp[(i, i)].update({nt: Tree(nt, [w])})
                    else:
                        self._pi[(i, i)] = {nt: lp}
                        self._bp[(i, i)] = {nt: Tree(nt, [w])}

        # RECURSIVE CASE
        for l in range(1, n):
            for i in range(1, n - l + 1):
                j = i + l
                for s in range(i, j):
                    # once s is fixed, ask for the possible partitions
                    # and its probabilities
                    for (Y, Y_lp) in self._pi[(i, s)].items():
                        for (Z, Z_lp) in self._pi[(s + 1, j)].items():
                            # ask if there exists a non terminal X such
                            # X -> Y Z is a valid production
                            if (Y, Z) in self.prods:
                                for (X, X_lp) in self.prods[(Y, Z)]:
                                    new_lp = Y_lp + Z_lp + X_lp
                                    # max prob and arg max
                                    if new_lp > \
                                       self._pi[(i, j)].get(X, float('-inf')):
                                        self._pi[(i, j)][X] = new_lp
                                        l_tree_bp = self._bp[(i, s)][Y]
                                        r_tree_bp = self._bp[(s + 1, j)][Z]
                                        self._bp[(i, j)][X] = Tree(X, [l_tree_bp, r_tree_bp])

        if S not in self._pi[(1, n)]:
            return(None, None)

        return (self._pi[(1, n)][S], self._bp[1, n][S])
