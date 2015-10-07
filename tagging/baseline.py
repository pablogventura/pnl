from collections import defaultdict
import operator


class BaselineTagger:

    def __init__(self, tagged_sents):
        """
        tagged_sents -- training sentences, each one being a list of pairs.
        """
        self.w_counts = defaultdict(int)
        self.t_counts = defaultdict(int)
        self.tag_dict = dict()
        self.word_dict = dict()
        # from stats.py
        for sent in tagged_sents:
            for s in sent:
                word = s[0]
                tag = s[1]
                self.w_counts[word] += 1
                self.t_counts[tag] += 1
                # tags for a word
                if word in self.word_dict:
                    if tag in self.word_dict[word]:
                        self.word_dict[word][tag] += 1
                    else:
                        self.word_dict[word].update({tag: 1})
                else:
                    self.word_dict[word] = {tag: 1}
                # words for a tag
                if tag in self.tag_dict:
                    if word in self.tag_dict[tag]:
                        self.tag_dict[tag][word] += 1
                    else:
                        self.tag_dict[tag].update({word: 1})
                else:
                    self.tag_dict[tag] = {word: 1}
        # words associated to a particular tag
        sorted_tags_words = dict()
        for tag, dict_words in self.tag_dict.items():
            sorted_tags_words[tag] = sorted(list(dict_words.items()), key=lambda x: -x[1])
        self.sorted_tags = sorted(list(self.t_counts.items()), key=lambda x: -x[1])

    def tag(self, sent):
        """Tag a sentence.

        sent -- the sentence.
        """
        return [self.tag_word(w) for w in sent]

    def tag_word(self, w):
        """Tag a word.

        w -- the word.
        """
        # if w it's unknown, return the most frequently tag
        if self.unknown(w):
            return self.sorted_tags[0][0]
        # else, we return the tag most frequently for w
        else:
            aux_dict = self.word_dict[w]
            sorted_x = sorted(aux_dict.items(), key=operator.itemgetter(1), reverse=True)
            return sorted_x[0][0]

    def unknown(self, w):
        """Check if a word is unknown for the model.

        w -- the word.
        """
        return w not in self.w_counts
