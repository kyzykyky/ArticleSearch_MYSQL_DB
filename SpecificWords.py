import pickle
import re


def sozgebolu(text):
    result = re.findall(r'\w+', str.lower(text))
    return result


class Specific_Words:
    word_base = pickle.load(open('word_base.dict', 'rb'))
    abbreviation_base = pickle.load(open('abbreviation_base.dict', 'rb'))
    stop_words_base = sozgebolu(open('stopwords.txt', 'r', encoding="utf8").read())
    negizder_base = sozgebolu(open('negizder.txt', 'r', encoding="utf8").read())


    @staticmethod
    def synonyms_searcher(word):
        synonyms_block = []
        c = False
        for w in Specific_Words.word_base:
            for ww in Specific_Words.word_base[w]:
                if ww == word:  # Mod Req
                    c = True
                    synonyms_block.append(Specific_Words.word_base[w])
        if c:
            return synonyms_block
        return None

    @staticmethod
    def abbreviation_searcher(word):
        abbreviation_block = []
        c = False
        for w in Specific_Words.abbreviation_base:
            for ww in Specific_Words.abbreviation_base[w]:
                if ww.lower() == word or ww.lower() == w.lower():  # Mod Req
                    c = True
                    t = Specific_Words.abbreviation_base[w].copy()
                    t.append(w)
                    abbreviation_block.append(t)
        if c:
            return abbreviation_block
        return None

    @staticmethod
    def if_stop_word(word):
        if word in Specific_Words.stop_words_base:
            return True
        else:
            return False
