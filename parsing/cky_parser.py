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

        non_lx = [e for e in self.productions if e.is_nonlexical()]
        lx = [e for e in self.productions if e.is_lexical()]

        # dict of X -> a productions with its probabilities
        self.q_non_lx_dict = {}
        for elem in non_lx:
            lhs = str(elem.lhs())
            rhs = (str(elem.rhs()[0]), str(elem.rhs()[1]))
            lp = elem.logprob()
            if lhs in self.q_non_lx_dict:
                self.q_non_lx_dict[lhs].update({rhs: lp})
            else:
                self.q_non_lx_dict[lhs] = {rhs: lp}

        # dict of X -> Y Z productions with its probabilities
        self.q_lx_dict = {}
        for elem in lx:
            lhs = str(elem.lhs())
            rhs = elem.rhs()
            lp = elem.logprob()
            if lhs in self.q_lx_dict:
                self.q_lx_dict[lhs].update({rhs: lp})
            else:
                self.q_lx_dict[lhs] = {rhs: lp}

    def parse(self, sent):
        """Parse a sequence of terminals.
        sent -- the sequence of terminals.
        """

        productions = self.productions
        q_lx_dict = self.q_lx_dict
        q_non_lx_dict = self.q_non_lx_dict
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
                if (w,) in q_lx_dict[nt]:
                    lp = q_lx_dict[nt][(w,)]
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
                    for prd in prod_xs:
                        Y = str(prd.rhs()[0])
                        Z = str(prd.rhs()[1])
                        aux_lp = q_non_lx_dict[X][(Y, Z)]
                        ys = []
                        for s in range(i, j):
                            if Y in self._pi[(i, s)]:
                                if Z in self._pi[(s + 1, j)]:
                                    ys.append(
                                        (X, Y, Z, s,
                                         (aux_lp +
                                          self._pi[(i, s,)][Y] +
                                          self._pi[(s + 1, j,)][Z]))
                                    )
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

        return (self._pi[(1, n)]['S'], self._bp[1, n]['S'])
