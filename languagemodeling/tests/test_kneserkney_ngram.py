# https://docs.python.org/3/library/unittest.html
from unittest import TestCase
from math import log

from languagemodeling.ngram import KneserNeyNGram


class TestNGram(TestCase):

    def setUp(self):
        self.sents = [
            'This is a list containing the tallest buildings in San Francisco :'.split(),
            'The Transamerica Pyramid is the tallest building in San Francisco .'.split(),
            '555 California Street is the 2nd-tallest building in San Francisco .'.split(),
        ]

    def test_count_1gram(self):
        ngram = KneserNeyNGram(n=1, sents=self.sents, D=1)

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
        ngram = KneserNeyNGram(n=2, sents=self.sents, D=1)

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

    def test_N_dot_tokens_dict_2gram(self):
        model = KneserNeyNGram(n=2, sents=self.sents, D=1)
        N_dot_tokens_dict = {
            ('.',): {('Francisco',)},
            ('2nd-tallest',): {('the',)},
            ('555',): {('<s>',)},
            (':',): {('Francisco',)},
            ('</s>',): {('.',), (':',)},
            ('California',): {('555',)},
            ('Francisco',): {('San',)},
            ('Pyramid',): {('Transamerica',)},
            ('San',): {('in',)},
            ('Street',): {('California',)},
            ('The',): {('<s>',)},
            ('This',): {('<s>',)},
            ('Transamerica',): {('The',)},
            ('a',): {('is',)},
            ('building',): {('2nd-tallest',), ('tallest',)},
            ('buildings',): {('tallest',)},
            ('containing',): {('list',)},
            ('in',): {('building',), ('buildings',)},
            ('is',): {('Pyramid',), ('Street',), ('This',)},
            ('list',): {('a',)},
            ('tallest',): {('the',)},
            ('the',): {('containing',), ('is',)}
        }

        for k, v in N_dot_tokens_dict.items():
            self.assertEqual(model._N_dot_tokens_dict[k], v, msg=v)

    def test_N_tokens_dot_dict_2gram(self):
        model = KneserNeyNGram(n=2, sents=self.sents, D=1)
        N_tokens_dot_dict =  {
            ('.',): {('</s>',)},
            ('2nd-tallest',): {('building',)},
            ('555',): {('California',)},
            (':',): {('</s>',)},
            ('<s>',): {('555',), ('The',), ('This',)},
            ('California',): {('Street',)},
            ('Francisco',): {('.',), (':',)},
            ('Pyramid',): {('is',)},
            ('San',): {('Francisco',)},
            ('Street',): {('is',)},
            ('The',): {('Transamerica',)},
            ('This',): {('is',)},
            ('Transamerica',): {('Pyramid',)},
            ('a',): {('list',)},
            ('building',): {('in',)},
            ('buildings',): {('in',)},
            ('containing',): {('the',)},
            ('in',): {('San',)},
            ('is',): {('a',), ('the',)},
            ('list',): {('containing',)},
            ('tallest',): {('building',), ('buildings',)},
            ('the',): {('2nd-tallest',), ('tallest',)}
        }

        for k, v in N_tokens_dot_dict.items():
            self.assertEqual(model._N_tokens_dot_dict[k], v, msg=v)

    def test_norm_2gram(self):
        models = [
            KneserNeyNGram(n=2, sents=self.sents,D=1),
            KneserNeyNGram(n=2, sents=self.sents,),
        ]

        tokens = ['the', ':', 'tallest', 'Francisco', 'This', 
                  '</s>', 'San', 'building', 'The', '2nd-tallest',
                  'in', 'containing', 'Street', '.', 'a', 'buildings',
                  'Pyramid', 'list', 'is', 'Transamerica', 'California', '555']

        prevs = ['the', ':', 'tallest', 'Francisco', 'This', 
                  '<s>', 'San', 'building', 'The', '2nd-tallest',
                  'in', 'containing', 'Street', '.', 'a', 'buildings',
                  'Pyramid', 'list', 'is', 'Transamerica', 'California', '555']

        for model in models:
            for prev in prevs:
                prob_sum = sum(model.cond_prob(token, (prev,)) for token in tokens)
                # prob_sum < 1.0 or almost equal to 1.0:
                self.assertAlmostLessEqual(prob_sum, 1.0, msg=prev)

    def test_count_3gram(self):
        model = KneserNeyNGram(n=3, sents=self.sents, D=1)
        counts = {
            (): 37,
            ('.',): 2,
            ('.', '</s>'): 2,
            ('2nd-tallest',): 1,
            ('2nd-tallest', 'building'): 1,
            ('2nd-tallest', 'building', 'in'): 1,
            ('555',): 1,
            ('555', 'California'): 1,
            ('555', 'California', 'Street'): 1,
            (':',): 1,
            (':', '</s>'): 1,
            ('</s>',): 3,
            ('<s>', '555'): 1,
            ('<s>', '555', 'California'): 1,
            ('<s>', '<s>'): 3,
            ('<s>', '<s>', '555'): 1,
            ('<s>', '<s>', 'The'): 1,
            ('<s>', '<s>', 'This'): 1,
            ('<s>', 'The'): 1,
            ('<s>', 'The', 'Transamerica'): 1,
            ('<s>', 'This'): 1,
            ('<s>', 'This', 'is'): 1,
            ('California',): 1,
            ('California', 'Street'): 1,
            ('California', 'Street', 'is'): 1,
            ('Francisco',): 3,
            ('Francisco', '.'): 2,
            ('Francisco', '.', '</s>'): 2,
            ('Francisco', ':'): 1,
            ('Francisco', ':', '</s>'): 1,
            ('Pyramid',): 1,
            ('Pyramid', 'is'): 1,
            ('Pyramid', 'is', 'the'): 1,
            ('San',): 3,
            ('San', 'Francisco'): 3,
            ('San', 'Francisco', '.'): 2,
            ('San', 'Francisco', ':'): 1,
            ('Street',): 1,
            ('Street', 'is'): 1,
            ('Street', 'is', 'the'): 1,
            ('The',): 1,
            ('The', 'Transamerica'): 1,
            ('The', 'Transamerica', 'Pyramid'): 1,
            ('This',): 1,
            ('This', 'is'): 1,
            ('This', 'is', 'a'): 1,
            ('Transamerica',): 1,
            ('Transamerica', 'Pyramid'): 1,
            ('Transamerica', 'Pyramid', 'is'): 1,
            ('a',): 1,
            ('a', 'list'): 1,
            ('a', 'list', 'containing'): 1,
            ('building',): 2,
            ('building', 'in'): 2,
            ('building', 'in', 'San'): 2,
            ('buildings',): 1,
            ('buildings', 'in'): 1,
            ('buildings', 'in', 'San'): 1,
            ('containing',): 1,
            ('containing', 'the'): 1,
            ('containing', 'the', 'tallest'): 1,
            ('in',): 3,
            ('in', 'San'): 3,
            ('in', 'San', 'Francisco'): 3,
            ('is',): 3,
            ('is', 'a'): 1,
            ('is', 'a', 'list'): 1,
            ('is', 'the'): 2,
            ('is', 'the', '2nd-tallest'): 1,
            ('is', 'the', 'tallest'): 1,
            ('list',): 1,
            ('list', 'containing'): 1,
            ('list', 'containing', 'the'): 1,
            ('tallest',): 2,
            ('tallest', 'building'): 1,
            ('tallest', 'building', 'in'): 1,
            ('tallest', 'buildings'): 1,
            ('tallest', 'buildings', 'in'): 1,
            ('the',): 3,
            ('the', '2nd-tallest'): 1,
            ('the', '2nd-tallest', 'building'): 1,
            ('the', 'tallest'): 2,
            ('the', 'tallest', 'building'): 1,
            ('the', 'tallest', 'buildings'): 1
        }


        for gram, c in counts.items():
            self.assertEqual(model.count(gram), c, msg=gram)

    def test_N_dot_tokens_dot_dict_3gram(self):
        model = KneserNeyNGram(n=3, sents=self.sents, D=1)
        N_dot_tokens_dot_dict = {
            ('.',): {('</s>',), ('Francisco',)},
            ('2nd-tallest',): {('building',), ('the',)},
            ('555',): {('<s>',), ('California',)},
            (':',): {('</s>',), ('Francisco',)},
            ('<s>',): {('555',), ('<s>',), ('The',), ('This',)},
            ('California',): {('555',), ('Street',)},
            ('Francisco',): {('.',), (':',), ('San',)},
            ('Pyramid',): {('Transamerica',), ('is',)},
            ('San',): {('Francisco',), ('in',)},
            ('Street',): {('California',), ('is',)},
            ('The',): {('<s>',), ('Transamerica',)},
            ('This',): {('<s>',), ('is',)},
            ('Transamerica',): {('Pyramid',), ('The',)},
            ('a',): {('is',), ('list',)},
            ('building',): {('2nd-tallest',), ('in',), ('tallest',)},
            ('buildings',): {('in',), ('tallest',)},
            ('containing',): {('list',), ('the',)},
            ('in',): {('San',), ('building',), ('buildings',)},
            ('is',): {('Pyramid',), ('Street',), ('This',), ('a',), ('the',)},
            ('list',): {('a',), ('containing',)},
            ('tallest',): {('building',), ('buildings',), ('the',)},
            ('the',): {('2nd-tallest',),
                       ('containing',),
                       ('is',),
                       ('tallest',)}
        }
        for k, v in N_dot_tokens_dot_dict.items():
            self.assertEqual(model._N_dot_tokens_dot_dict[k], v, msg=v)


    def test_N_tokens_doc_dict_3gram(self):
        model = KneserNeyNGram(n=3, sents=self.sents, D=1)

        N_tokens_dot_dict = {
            ('.',): {('</s>',)},
            ('2nd-tallest',): {('building',)},
            ('2nd-tallest', 'building'): {('in',)},
            ('555',): {('California',)},
            ('555', 'California'): {('Street',)},
            (':',): {('</s>',)},
            ('<s>',): {('555',), ('The',), ('This',)},
            ('<s>', '555'): {('California',)},
            ('<s>', '<s>'): {('555',), ('The',), ('This',)},
            ('<s>', 'The'): {('Transamerica',)},
            ('<s>', 'This'): {('is',)},
            ('California',): {('Street',)},
            ('California', 'Street'): {('is',)},
            ('Francisco',): {('.',), (':',)},
            ('Francisco', '.'): {('</s>',)},
            ('Francisco', ':'): {('</s>',)},
            ('Pyramid',): {('is',)},
            ('Pyramid', 'is'): {('the',)},
            ('San',): {('Francisco',)},
            ('San', 'Francisco'): {('.',), (':',)},
            ('Street',): {('is',)},
            ('Street', 'is'): {('the',)},
            ('The',): {('Transamerica',)},
            ('The', 'Transamerica'): {('Pyramid',)},
            ('This',): {('is',)},
            ('This', 'is'): {('a',)},
            ('Transamerica',): {('Pyramid',)},
            ('Transamerica', 'Pyramid'): {('is',)},
            ('a',): {('list',)},
            ('a', 'list'): {('containing',)},
            ('building',): {('in',)},
            ('building', 'in'): {('San',)},
            ('buildings',): {('in',)},
            ('buildings', 'in'): {('San',)},
            ('containing',): {('the',)},
            ('containing', 'the'): {('tallest',)},
            ('in',): {('San',)},
            ('in', 'San'): {('Francisco',)},
            ('is',): {('a',), ('the',)},
            ('is', 'a'): {('list',)},
            ('is', 'the'): {('2nd-tallest',), ('tallest',)},
            ('list',): {('containing',)},
            ('list', 'containing'): {('the',)},
            ('tallest',): {('building',), ('buildings',)},
            ('tallest', 'building'): {('in',)},
            ('tallest', 'buildings'): {('in',)},
            ('the',): {('2nd-tallest',), ('tallest',)},
            ('the', '2nd-tallest'): {('building',)},
            ('the', 'tallest'): {('building',), ('buildings',)}
        }

        for k, v in N_tokens_dot_dict.items():
            self.assertEqual(model._N_tokens_dot_dict[k], v, msg=v)

    def test_N_dot_tokens_dict_3gram(self):
        model = KneserNeyNGram(n=3, sents=self.sents, D=1)

        N_dot_tokens_dict = {
            ('.',): {('Francisco',)},
            ('.', '</s>'): {('Francisco',)},
            ('2nd-tallest',): {('the',)},
            ('2nd-tallest', 'building'): {('the',)},
            ('555',): {('<s>',)},
            ('555', 'California'): {('<s>',)},
            (':',): {('Francisco',)},
            (':', '</s>'): {('Francisco',)},
            ('</s>',): {('.',), (':',)},
            ('<s>', '555'): {('<s>',)},
            ('<s>', 'The'): {('<s>',)},
            ('<s>', 'This'): {('<s>',)},
            ('California',): {('555',)},
            ('California', 'Street'): {('555',)},
            ('Francisco',): {('San',)},
            ('Francisco', '.'): {('San',)},
            ('Francisco', ':'): {('San',)},
            ('Pyramid',): {('Transamerica',)},
            ('Pyramid', 'is'): {('Transamerica',)},
            ('San',): {('in',)},
            ('San', 'Francisco'): {('in',)},
            ('Street',): {('California',)},
            ('Street', 'is'): {('California',)},
            ('The',): {('<s>',)},
            ('The', 'Transamerica'): {('<s>',)},
            ('This',): {('<s>',)},
            ('This', 'is'): {('<s>',)},
            ('Transamerica',): {('The',)},
            ('Transamerica', 'Pyramid'): {('The',)},
            ('a',): {('is',)},
            ('a', 'list'): {('is',)},
            ('building',): {('2nd-tallest',), ('tallest',)},
            ('building', 'in'): {('2nd-tallest',), ('tallest',)},
            ('buildings',): {('tallest',)},
            ('buildings', 'in'): {('tallest',)},
            ('containing',): {('list',)},
            ('containing', 'the'): {('list',)},
            ('in',): {('building',), ('buildings',)},
            ('in', 'San'): {('building',), ('buildings',)},
            ('is',): {('Pyramid',), ('Street',), ('This',)},
            ('is', 'a'): {('This',)},
            ('is', 'the'): {('Pyramid',), ('Street',)},
            ('list',): {('a',)},
            ('list', 'containing'): {('a',)},
            ('tallest',): {('the',)},
            ('tallest', 'building'): {('the',)},
            ('tallest', 'buildings'): {('the',)},
            ('the',): {('containing',), ('is',)},
            ('the', '2nd-tallest'): {('is',)},
            ('the', 'tallest'): {('containing',), ('is',)}
        }

        for k, v in N_dot_tokens_dict.items():
            self.assertEqual(model._N_dot_tokens_dict[k], v, msg=v)

    def test_norm_3gram(self):
        models = [
            KneserNeyNGram(n=3, sents=self.sents, D=1),
            KneserNeyNGram(n=3, sents=self.sents,),
        ]

        tokens = ['the', ':', 'tallest', 'Francisco', 'This', 
                  'San', 'building', 'The', '2nd-tallest',
                  'in', 'containing', 'Street', '.', 'a', 'buildings',
                  'Pyramid', 'list', 'is', 'Transamerica', 'California', '555']

        prev_tokens = ['the', ':', 'tallest', 'Francisco', 'This', 
                  '<s>', 'San', 'building', 'The', '2nd-tallest',
                  'in', 'containing', 'Street', '.', 'a', 'buildings',
                  'Pyramid', 'list', 'is', 'Transamerica', 'California', '555']


        prevs = [('<s>', '<s>')] + \
            [('<s>', t) for t in prev_tokens] + \
            [(t1, t2) for t1 in prev_tokens for t2 in prev_tokens]

        for model in models:
            for prev in prevs:
                prob_sum = sum(model.cond_prob(token, (prev,)) for token in tokens)
                # prob_sum < 1.0 or almost equal to 1.0:
                self.assertAlmostLessEqual(prob_sum, 1.0, msg=prev)

    def assertAlmostLessEqual(self, a, b, places=7, msg=None):
        self.assertTrue(a < b or round(abs(a - b), places) == 0, msg=msg)
