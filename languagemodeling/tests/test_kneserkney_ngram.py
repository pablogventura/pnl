# https://docs.python.org/3/library/unittest.html
from unittest import TestCase
from math import log

from languagemodeling.kneserney import KN4 as KneserNeyNGram


class TestNGram(TestCase):

    def setUp(self):
        self.sents = [
            'This is a list containing the tallest buildings in San Francisco :'.split(),
            'The Transamerica Pyramid is the tallest building in San Francisco .'.split(),
            '555 California Street is the 2nd-tallest building in San Francisco .'.split(),
        ]

    def test_count_1gram(self):
        ngram = KneserNeyNGram(n=1, sents=self.sents)

        counts = {
            (): 37,
            ('.',): 2,
            ('2nd-tallest',): 1,
            ('555',): 1,
            (':',): 1,
            ('</s>',): 3,
            ('a',): 1,
            ('building',): 2,
            ('buildings',): 1,
            ('California',): 1,
            ('containing',): 1,
            ('Francisco',): 3,
            ('in',): 3,
            ('is',): 3,
            ('list',): 1,
            ('Pyramid',): 1,
            ('San',): 3,
            ('Street',): 1,
            ('tallest',): 2,
            ('the',): 3,
            ('The',): 1,
            ('This',): 1,
            ('Transamerica',): 1,
        }

        for gram, c in counts.items():
            self.assertEqual(ngram.count(gram), c, msg=gram)

    def test_count_2gram(self):
        ngram = KneserNeyNGram(n=2, sents=self.sents)

        counts = {
            ('.',): 2,
            ('.', '</s>'): 2,
            ('2nd-tallest',): 1,
            ('2nd-tallest', 'building'): 1,
            ('555',): 1,
            ('555', 'California'): 1,
            (':',): 1,
            (':', '</s>'): 1,
            ('<s>',): 3,
            ('<s>', '555'): 1,
            ('<s>', 'The'): 1,
            ('<s>', 'This'): 1,
            ('a',): 1,
            ('a', 'list'): 1,
            ('building',): 2,
            ('building', 'in'): 2,
            ('buildings',): 1,
            ('buildings', 'in'): 1,
            ('California',): 1,
            ('California', 'Street'): 1,
            ('containing',): 1,
            ('containing', 'the'): 1,
            ('Francisco',): 3,
            ('Francisco', '.'): 2,
            ('Francisco', ':'): 1,
            ('in',): 3,
            ('in', 'San'): 3,
            ('is',): 3,
            ('is', 'a'): 1,
            ('is', 'the'): 2,
            ('list',): 1,
            ('list', 'containing'): 1,
            ('Pyramid',): 1,
            ('Pyramid', 'is'): 1,
            ('San',): 3,
            ('San', 'Francisco'): 3,
            ('Street',): 1,
            ('Street', 'is'): 1,
            ('tallest',): 2,
            ('tallest', 'building'): 1,
            ('tallest', 'buildings'): 1,
            ('The',): 1,
            ('the',): 3,
            ('the', '2nd-tallest'): 1,
            ('the', 'tallest'): 2,
            ('The', 'Transamerica'): 1,
            ('This',): 1,
            ('This', 'is'): 1,
            ('Transamerica',): 1,
            ('Transamerica', 'Pyramid'): 1,
        }

        for gram, c in counts.items():
            self.assertEqual(ngram.count(gram), c, msg=gram)
"""
    def test_cond_prob_1gram(self):
        ngram = NGram(1, self.sents)

        probs = {
            'pescado': 1 / 12.0,
            'come': 2 / 12.0,
            'salame': 0.0,
        }
        for token, p in probs.items():
            self.assertEqual(ngram.cond_prob(token), p)

    def test_cond_prob_2gram(self):
        ngram = NGram(2, self.sents)

        probs = {
            ('pescado', 'come'): 0.5,
            ('salmón', 'come'): 0.5,
            ('salame', 'come'): 0.0,
        }
        for (token, prev), p in probs.items():
            self.assertEqual(ngram.cond_prob(token, [prev]), p)

    def test_sent_prob_1gram(self):
        ngram = NGram(1, self.sents)

        sents = {
            # 'come', '.' and '</s>' have prob 1/6, the rest have 1/12.
            'el gato come pescado .': (1 / 6.0)**3 * (1 / 12.0)**3,
            'la gata come salmón .': (1 / 6.0)**3 * (1 / 12.0)**3,
            'el gato come salame .': 0.0,  # 'salame' unseen
            'la la la': (1 / 6.0)**1 * (1 / 12.0)**3,
        }
        for sent, prob in sents.items():
            self.assertAlmostEqual(ngram.sent_prob(sent.split()), prob, msg=sent)

    def test_sent_prob_2gram(self):
        ngram = NGram(2, self.sents)

        sents = {
            # after '<s>': 'el' and 'la' have prob 0.5.
            # after 'come': 'pescado' and 'salmón' have prob 0.5.
            'el gato come pescado .': 0.5 * 0.5,
            'la gata come salmón .': 0.5 * 0.5,
            'el gato come salmón .': 0.5 * 0.5,
            'la gata come pescado .': 0.5 * 0.5,
            'el gato come salame .': 0.0,  # 'salame' unseen
            'la la la': 0.0,  # 'la' after 'la' unseen
        }
        for sent, prob in sents.items():
            self.assertAlmostEqual(ngram.sent_prob(sent.split()), prob, msg=sent)

    def test_sent_log_prob_1gram(self):
        ngram = NGram(1, self.sents)

        log2 = lambda x: log(x, 2)
        sents = {
            # 'come', '.' and '</s>' have prob 1/6, the rest have 1/12.
            'el gato come pescado .': 3 * log2(1 / 6.0) + 3 * log2(1 / 12.0),
            'la gata come salmón .': 3 * log2(1 / 6.0) + 3 * log2(1 / 12.0),
            'el gato come salame .': float('-inf'),  # 'salame' unseen
            'la la la': log2(1 / 6.0) + 3 * log2(1 / 12.0),
        }
        for sent, prob in sents.items():
            self.assertAlmostEqual(ngram.sent_log_prob(sent.split()), prob, msg=sent)

    def test_sent_log_prob_2gram(self):
        ngram = NGram(2, self.sents)

        log2 = lambda x: log(x, 2)
        sents = {
            # after '<s>': 'el' and 'la' have prob 0.5.
            # after 'come': 'pescado' and 'salmón' have prob 0.5.
            'el gato come pescado .': 2 * log2(0.5),
            'la gata come salmón .': 2 * log2(0.5),
            'el gato come salmón .': 2 * log2(0.5),
            'la gata come pescado .': 2 * log2(0.5),
            'el gato come salame .': float('-inf'),  # 'salame' unseen
            'la la la': float('-inf'),  # 'la' after 'la' unseen
        }
        for sent, prob in sents.items():
            self.assertAlmostEqual(ngram.sent_log_prob(sent.split()), prob, msg=sent)
"""
