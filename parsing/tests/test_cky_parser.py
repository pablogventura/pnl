# https://docs.python.org/3/library/unittest.html
from unittest import TestCase
from math import log2

from nltk.tree import Tree
from nltk.grammar import PCFG

from parsing.cky_parser import CKYParser


class TestCKYParser(TestCase):

    def test_parse(self):
        grammar = PCFG.fromstring(
            """
                S -> NP VP              [1.0]
                NP -> Det Noun          [0.6]
                NP -> Noun Adj          [0.4]
                VP -> Verb NP           [1.0]
                Det -> 'el'             [1.0]
                Noun -> 'gato'          [0.9]
                Noun -> 'pescado'       [0.1]
                Verb -> 'come'          [1.0]
                Adj -> 'crudo'          [1.0]
            """)

        parser = CKYParser(grammar)

        lp, t = parser.parse('el gato come pescado crudo'.split())

        # check chart
        pi = {
            (1, 1): {'Det': log2(1.0)},
            (2, 2): {'Noun': log2(0.9)},
            (3, 3): {'Verb': log2(1.0)},
            (4, 4): {'Noun': log2(0.1)},
            (5, 5): {'Adj': log2(1.0)},

            (1, 2): {'NP': log2(0.6 * 1.0 * 0.9)},
            (2, 3): {},
            (3, 4): {},
            (4, 5): {'NP': log2(0.4 * 0.1 * 1.0)},

            (1, 3): {},
            (2, 4): {},
            (3, 5): {'VP': log2(1.0) + log2(1.0) + log2(0.4 * 0.1 * 1.0)},

            (1, 4): {},
            (2, 5): {},

            (1, 5): {'S':
                     log2(1.0) +  # rule S -> NP VP
                     log2(0.6 * 1.0 * 0.9) +  # left part
                     log2(1.0) + log2(1.0) + log2(0.4 * 0.1 * 1.0)},  # right part
        }
        self.assertEqualPi(parser._pi, pi)

        # check partial results
        bp = {
            (1, 1): {'Det': Tree.fromstring("(Det el)")},
            (2, 2): {'Noun': Tree.fromstring("(Noun gato)")},
            (3, 3): {'Verb': Tree.fromstring("(Verb come)")},
            (4, 4): {'Noun': Tree.fromstring("(Noun pescado)")},
            (5, 5): {'Adj': Tree.fromstring("(Adj crudo)")},

            (1, 2): {'NP': Tree.fromstring("(NP (Det el) (Noun gato))")},
            (2, 3): {},
            (3, 4): {},
            (4, 5): {'NP': Tree.fromstring("(NP (Noun pescado) (Adj crudo))")},

            (1, 3): {},
            (2, 4): {},
            (3, 5): {'VP': Tree.fromstring(
                "(VP (Verb come) (NP (Noun pescado) (Adj crudo)))")},

            (1, 4): {},
            (2, 5): {},

            (1, 5): {'S': Tree.fromstring(
                """(S
                    (NP (Det el) (Noun gato))
                    (VP (Verb come) (NP (Noun pescado) (Adj crudo)))
                   )
                """)},
        }
        self.assertEqual(parser._bp, bp)

        # check tree
        t2 = Tree.fromstring(
            """
                (S
                    (NP (Det el) (Noun gato))
                    (VP (Verb come) (NP (Noun pescado) (Adj crudo)))
                )
            """)
        self.assertEqual(t, t2)

        # check log probability
        lp2 = log2(1.0 * 0.6 * 1.0 * 0.9 * 1.0 * 1.0 * 0.4 * 0.1 * 1.0)
        self.assertAlmostEqual(lp, lp2)

    def assertEqualPi(self, pi1, pi2):
        self.assertEqual(set(pi1.keys()), set(pi2.keys()))

        for k in pi1.keys():
            d1, d2 = pi1[k], pi2[k]
            self.assertEqual(d1.keys(), d2.keys(), k)
            for k2 in d1.keys():
                prob1 = d1[k2]
                prob2 = d2[k2]
                self.assertAlmostEqual(prob1, prob2)

    # ambiguous parsing example, taken from nltk webpage
    def test_parse_ambiguous(self):
        grammar = PCFG.fromstring(
            """
            S -> Pn VP [1.0]
            VP -> VP PP [0.9]
            VP -> V NP [0.1]
            PP -> P NP [1.0]
            NP -> Det N [0.9]
            NP -> Det NPP [0.1]
            NPP -> N PP [1.0]

            Pn -> 'I'  [1.0]
            V -> 'rode' [1.0]
            Det -> 'an' [0.2]
            N -> 'elephant' [0.6]
            P -> 'in' [1.0]
            Det -> 'my' [0.8]
            N -> 'pajamas' [0.4]
            """)
        parser = CKYParser(grammar)
        lp, t = parser.parse('I rode an elephant in my pajamas'.split())

        # check tree
        t2 = Tree.fromstring(
            """
            (S
                (Pn I)
                (VP
                    (VP (V rode) (NP (Det an) (N elephant)))
                    (PP (P in) (NP (Det my) (N pajamas)))))
            """)

        self.assertEqual(t, t2)

        # check chart
        pi = {
            (1, 1): {'Pn': log2(1.0)},
            (2, 2): {'V': log2(1.0)},
            (3, 3): {'Det': log2(0.2)},
            (4, 4): {'N': log2(0.6)},
            (5, 5): {'P': log2(1.0)},
            (6, 6): {'Det': log2(0.8)},
            (7, 7): {'N': log2(0.4)},
            (3, 4): {'NP': log2(0.9*0.2*0.6)},
            (2, 4): {'VP': log2(0.1*0.2*0.6*0.9)},
            (6, 7): {'NP': log2(0.9*0.8*0.4)},
            (5, 7): {'PP': log2(1.0*1.0*0.9*0.8*0.4)},
            (3, 7): {'NP': log2(0.9*0.6*0.1*0.2*0.4*0.8)},
            # check
            (4, 7): {'NPP': -2.5328248773859805},
            # (2,4) and (5,7)
            (1, 4): {'S': log2(0.9*0.6*0.1*0.2)},
            (2, 7): {'VP': log2(0.9 * 0.9 * 0.4*0.8*0.1*0.9*0.2*0.6)},
            (1, 7): {'S': log2(1.0*0.9 * 0.9 * 0.4*0.8*0.1*0.9*0.2*0.6)},
            # empty
            (2, 6): {},
            (4, 5): {},
            (5, 6): {},
            (1, 3): {},
            (1, 6): {},
            (2, 5): {},
            (3, 5): {},
            (1, 2): {},
            (4, 6): {},
            (1, 5): {},
            (3, 6): {},
            (2, 3): {},
        }
        self.assertEqualPi(parser._pi, pi)

        # check log probability
        lp2 = log2(1.0 * 0.9 * 0.9 * 0.4 * 0.8 * 0.1 * 0.9 * 0.2 * 0.6)
        self.assertAlmostEqual(lp, lp2)

        # check partial results
        bp = {
            (1, 1): {'Pn': Tree.fromstring("(Pn I)")},
            (2, 2): {'V': Tree.fromstring("(V rode)")},
            (3, 3): {'Det': Tree.fromstring("(Det an)")},
            (4, 4): {'N': Tree.fromstring("(N elephant)")},
            (5, 5): {'P': Tree.fromstring("(P in)")},
            (6, 6): {'Det': Tree.fromstring("(Det my)")},
            (7, 7): {'N': Tree.fromstring("(N pajamas)")},

            (3, 4): {'NP': Tree.fromstring("(NP (Det an) (N elephant))")},
            (6, 7): {'NP': Tree.fromstring("(NP (Det my) (N pajamas))")},

            (2, 4): {'VP': Tree.fromstring("(VP (V rode) (NP (Det an) (N elephant)))")},
            (5, 7): {'PP': Tree.fromstring("(PP (P in) (NP (Det my) (N pajamas)))")},
            (1, 4): {'S': Tree.fromstring("(S (Pn I) (VP (V rode) (NP (Det an) (N elephant))))")},
            (3, 7): {'NP': Tree.fromstring("(NP (Det an) (NPP (N elephant) (PP (P in) (NP (Det my) (N pajamas) ))))")},
            (4, 7): {'NPP': Tree.fromstring("(NPP (N elephant) (PP (P in) (NP (Det my) (N pajamas) )))")},

            (2, 7): {'VP': Tree.fromstring(
                """(VP (VP (V rode) (NP (Det an) (N elephant)))
                (PP (P in) (NP (Det my) (N pajamas))))
                """)},

            (1, 7): {'S': Tree.fromstring(
                """(S
                (Pn I)
                (VP (VP (V rode) (NP (Det an) (N elephant)))
                (PP (P in) (NP (Det my) (N pajamas)))))
                """)},

            # empty ones
            (2, 6): {},
            (4, 5): {},
            (5, 6): {},
            (1, 3): {},
            (1, 6): {},
            (2, 5): {},
            (3, 5): {},
            (1, 2): {},
            (4, 6): {},
            (1, 5): {},
            (3, 6): {},
            (2, 3): {},
            }

        self.assertEqual(parser._bp, bp)
