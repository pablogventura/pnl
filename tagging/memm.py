from featureforge.vectorizer import Vectorizer
# Maximum entropy classifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from tagging.features import *


class MEMM(object):

    def __init__(self, n, tagged_sents):
        """
        n -- order of the model.
        tagged_sents -- list of sentences, each one being a list of pairs.
        """
        self.n = n
        self.voc = set()

        self.ts = []
        self.ws = []
        for elem in tagged_sents:
            # for words
            xs = []
            # for tags
            ys = []
            if n > 1:
                ys = [('<s>',)*(n-1)]
            for w, t in elem:
                self.voc.add(w)
                xs.append(w)
                ys.append((t,))
            self.ws.append(xs)
            self.ts.append(ys)

    def sents_histories(self, tagged_sents):
        """
        Iterator over the histories of a corpus.
        tagged_sents -- the corpus (a list of sentences)
        """

    def sent_histories(self, tagged_sent):
        """
        Iterator over the histories of a tagged sentence.
        tagged_sent -- the tagged sentence (a list of pairs (word, tag)).
        """
        n = self.n

        xs = tuple()
        histories = []
        if n > 1:
            xs = (('<s>',)*(n-1))
        ys = []
        for elem in tagged_sent:
            tag = elem[1]
            word = elem[0]
            xs = xs + (tag,)
            ys.append(word)
        taggram_xs = []

        for j in range(len(xs) - n + 1):
            taggram = xs[j: j + n-1]
            taggram_xs.append(taggram)

        for i in range(len(taggram_xs)):
            histories.append(History(ys, taggram_xs[i], i))

        return histories

    def sents_tags(self, tagged_sents):
        """
        Iterator over the tags of a corpus.
        tagged_sents -- the corpus (a list of sentences)
        """

    def sent_tags(self, tagged_sent):
        """
        Iterator over the tags of a tagged sentence.
        tagged_sent -- the tagged sentence (a list of pairs (word, tag)).
        """
        
    def tag(self, sent):
        """Tag a sentence.
 
        sent -- the sentence.
        """
 
    def tag_history(self, h):
        """Tag a history.
        h -- the history.
        """
 
    def unknown(self, w):
        """Check if a word is unknown for the model.
 
        w -- the word.
        """
        return w not in self.voc
