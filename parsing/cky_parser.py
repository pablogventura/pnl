from nltk import Tree


class CKYParser:

    def __init__(self, grammar):
        """
        grammar -- a binarised NLTK PCFG.
        """
        self.productions = grammar.productions()
        self.lex_N = {str(elem.lhs()) for elem in self.productions
                      if elem.is_lexical()}
        self.non_lex_N = {str(elem.lhs()) for elem in self.productions
                          if elem.is_nonlexical()}

        # dict of productions
        self.q = {}
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

        productions = self.productions
        q = self.q
        lex_N = self.lex_N
        non_lex_N = self.non_lex_N

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
                for X in non_lex_N:
                    # all productions to compare
                    prod_xs = [elem for elem in productions
                               if str(elem.lhs()) == X]
                    ys = []
                    for prd in prod_xs:
                        Y = str(prd.rhs()[0])
                        Z = str(prd.rhs()[1])
                        aux_lp = prd.logprob()
                        for s in range(i, j):
                            if Y in self._pi[(i, s)]:
                                if Z in self._pi[(s + 1, j)]:
                                    Y_lp = self._pi[(i, s,)][Y]
                                    Z_lp = self._pi[(s + 1, j,)][Z]
                                    new_lp = aux_lp + Y_lp + Z_lp
                                    ys.append((X, Y, Z, s, new_lp))
                        if ys:
                            max_tpl = max(ys, key=lambda x: x[-1])
                            nt = max_tpl[0]
                            lp = max_tpl[-1]
                            self._pi[(i, j)] = {nt: lp}
                            # backpointer
                            aux_nt_Y = max_tpl[1]
                            aux_nt_Z = max_tpl[2]
                            s = max_tpl[3]
                            l_tree = self._bp[(i, s)][aux_nt_Y]
                            r_tree = self._bp[(s + 1, j)][aux_nt_Z]
                            self._bp[(i, j)] = {nt: Tree(nt, [l_tree, r_tree])}

        if 'S' not in self._pi[(1, n)]:
            return(None, None)

        return (self._pi[(1, n)]['S'], self._bp[1, n]['S'])
