from collections import namedtuple

from featureforge.feature import Feature


# sent -- the whole sentence.
# prev_tags -- a tuple with the n previous tags.
# i -- the position to be tagged.
History = namedtuple('History', 'sent prev_tags i')


def word_lower(h):
    """Feature: current lowercased word.
    h -- a history.
    """
    sent, i = h.sent, h.i
    return sent[i].lower()

def word_istitle(h):
    """Feature: current word is a title.
    h -- a history.
    """
    sent, i = h.sent, h.i
    return sent[i].istitle()

def word_isupper(h):
    """Feature: current word is capitalized.
    h -- a history.
    """
    sent, i = h.sent, h.i
    return sent[i].isupper()

def word_isdigit(h):
    """Feature: current word is a number.
    h -- a history.
    """
    sent, i = h.sent, h.i
    return sent[i].isdigit()

def prev_tags(h):
    """Return the previous tag.
    """
    return h.prev_tags

class NPrevTags(Feature):
 
    def __init__(self, n):
        """Feature: n previous tags tuple.
 
        n -- number of previous tags to consider.
        """
        self.n = n
        # from tutorial
        self._name = 'Previous n tags'

    def _evaluate(self, h):
        """n previous tags tuple.
 
        h -- a history.
        """
        n = self.n
        return h.prev_tags[-n:]
        
class PrevWord(Feature):
 
    def __init__(self, f):
        """Feature: the feature f applied to the previous word.
        f -- the feature.
        """
        self.feature = f

    def _evaluate(self, h):
        """Apply the feature to the previous word in the history. 
        h -- the history.
        """
        # the feature to apply
        feature = self.feature
        sent, i, prev_tags = h.sent, h.i, h.prev_tags
        # create new history,
        new_h = History(sent, prev_tags, i-1)
        # Begining of sentence
        if not i:
            return 'BOS'
        else:
            return str(feature(new_h))
