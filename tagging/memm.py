from featureforge.vectorizer import Vectorizer
# Maximum entropy classifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from tagging.features import *

# from scikit tutorial
from sklearn.pipeline import Pipeline


class MEMM(object):

    def __init__(self, n, tagged_sents, classifier='lr'):
        """
        n -- order of the model.
        tagged_sents -- list of sentences, each one being a list of pairs.
        """
        self.n = n
        self.voc = set()
        # for tags
        self.ts = []

        # select classifier
        if classifier == 'lr':
            clf = LogisticRegression()
        elif classifier == 'mnb':
            clf = MultinomialNB()
        elif classifier == 'lsvc':
            clf = LinearSVC()
        else:
            raise TypeError('Classifier not found')

        for elem in tagged_sents:
            for w, t in elem:
                self.voc.add(w)
                self.ts.append(t)

        aux_ft_1 = [word_lower, word_isdigit, word_istitle,
                    word_isupper, prev_tags, PrevWord(word_lower)]
        aux_ft_2 = [NPrevTags(i) for i in range(1, n)]
        features = aux_ft_1 + aux_ft_2

        vector = Vectorizer(features)
        vector.fit(self.sents_histories(tagged_sents))
        # from tutorial
        self.text_clf = Pipeline([('vectorizer', vector),
                                  ('classificator', clf), ])

        # train classifier
        self.text_clf.fit(self.sents_histories(tagged_sents),
                          self.sents_tags(tagged_sents))

    def sents_histories(self, tagged_sents):
        """
        Iterator over the histories of a corpus.
        tagged_sents -- the corpus (a list of sentences)
        """
        ys = []
        for sent in tagged_sents:
            for hs in self.sent_histories(sent):
                ys.append(hs)
        return ys

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
            xs = (xs + (tag,))
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
        ys = []
        for elem in tagged_sents:
            for st in self.sent_tags(elem):
                ys.append(st)
        return ys

    def sent_tags(self, tagged_sent):
        """
        Iterator over the tags of a tagged sentence.
        tagged_sent -- the tagged sentence (a list of pairs (word, tag)).
        """
        ys = []
        for w, t in tagged_sent:
            ys.append(t)
        return ys

    def tag(self, sent):
        """Tag a sentence.
        sent -- the sentence.
        """
        n = self.n
        tag_sq = ('<s>',)*(n-1)
        for i in range(len(sent)):
            hs = History(sent, tag_sq, i)
            aux_tag = self.tag_history(hs)
            tag_sq += (aux_tag,)
        return(list(tag_sq[(n-1):]))

    def tag_history(self, h):
        """Tag a history.
        h -- the history.
        """
        # a tag secuence is like a category, so we can predict it
        return self.text_clf.predict([h])[0]

    def unknown(self, w):
        """Check if a word is unknown for the model.
        w -- the word.
        """
        return w not in self.voc
