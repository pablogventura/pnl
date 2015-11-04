class CKYParser:
 
    def __init__(self, grammar):
        """
        grammar -- a binarised NLTK PCFG.
        """
        self.productions = grammar.productions()
        # sent
        self.lexicals = [elem for elem in self.productions if elem.is_lexical()]
        self.d = dict()
        for elem in self.lexicals:
            w = elem.rhs()[0]
            pos = str(elem.lhs())
            self.d[(w,pos)] = elem.logprob()

        self.non_lexicals = [elem for elem in self.productions if elem.is_nonlexical()]
        self.q_dict = {}
        for elem in self.non_lexicals:
            self.q_dict[elem.lhs()] = {elem.rhs() : elem.logprob()}
        # set of Non terminals
        self.N = {elem.lhs() for elem in self.non_lexicals}

    def parse(self, sent):
        """Parse a sequence of terminals. 
        sent -- the sequence of terminals.
        """

        self._pi = {}
        # X -> a productions
        lexicals = self.lexicals
        productions = self.productions
        d = self.d
        N = self.N
        n = len(sent)
        lex_set = {str(elem.lhs()) for elem in lexicals}
        q_dict = self.q_dict

        # INIT
        for i in range(1, n + 1):
            self._pi[(i, i)] = {}
            w = sent[i - 1]
            for nt in lex_set:
                if (w, nt) in d:
                    self._pi[(i, i)] = {nt : d[(w, nt)]}

        for k in range(1, n + 1):
            for m in range(1, n + 1):
                if not k == m:
                    self._pi[(k, m)] = {}



        print(self._pi)
        # RECURSIVE CASE
        for l in range(1, n):
            for i in range(1, n - l + 1):
                j = i + l
                for X in N:
                    # all productions to compare
                    prod_xs = [elem for elem in productions if elem.lhs() == X]
                    for prd in prod_xs:
                        Y = prd.rhs()[0]
                        Z = prd.rhs()[1]

                        if X in q_dict:
                            if (Y, Z) in q_dict[X]:
                                aux_q = q_dict[X][(Y, Z)]

                                for s in range(i, j - 2):
                                    ys.append(aux_q + self._pi(i, s, Y) + self._pi(s + 1, j, Z))
                                    print(ys)
                mx = max(ys)
                self._pi[(i, j)] = {X : mx}

        print(self._pi)
