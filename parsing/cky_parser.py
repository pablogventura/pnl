class CKYParser:
 
    def __init__(self, grammar):
        """
        grammar -- a binarised NLTK PCFG.
        """
        self.productions = grammar.productions()

        self.q_dict = {}
        for elem in self.productions:
            lhs = elem.lhs()
            rhs = elem.rhs()
            lp = elem.logprob()
            if lhs in self.q_dict:
                self.q_dict[lhs].update({rhs : lp})
            else:
                self.q_dict[elem.lhs()] = {elem.rhs() : elem.logprob()}

        # set of Non terminals
        self.lex_N = {elem.lhs() for elem in self.productions if elem.is_lexical()}
        self.non_lex_N = {elem.lhs() for elem in self.productions if elem.is_nonlexical()}

    def parse(self, sent):
        """Parse a sequence of terminals. 
        sent -- the sequence of terminals.
        """

        productions = self.productions
        q_dict = self.q_dict
        lex_N = self.lex_N
        non_lex_N = self.non_lex_N

        n = len(sent)
        self._pi = {}

        # INIT
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if j > i:
                    self._pi[(i, j)] = {}

        for i in range(1, n + 1):
            w = sent[i - 1]
            for nt in lex_N:
                if (w,) in q_dict[nt]:
                    lp = q_dict[nt][(w,)]
                    self._pi[(i, i)] = {nt : lp}

        # RECURSIVE CASE
        for l in range(1, n):
            for i in range(1, n - l + 1):
                j = i + l
                for X in non_lex_N:
                    # all productions to compare
                    prod_xs = [elem for elem in productions if elem.lhs() == X]
                    for prd in prod_xs:
                        Y = prd.rhs()[0]
                        Z = prd.rhs()[1]
                        aux_q = q_dict[X][(Y, Z)]
                        ys = []
                        for s in range(i, j):
                            if Y in self._pi[(i, s)]:
                                if Z in self._pi[(s + 1, j)]:
                                    ys.append((X, (aux_q + self._pi[(i, s,)][Y] + self._pi[(s + 1, j,)][Z])))
                        if ys:
                            max_tpl = max(ys)
                            nt = max_tpl[0]
                            lp = max_tpl[1]
                            self._pi[(i, j)] = {nt : lp}
                            print('')
                            print(self._pi)
                            print('')
