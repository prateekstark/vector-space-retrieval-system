from utils import preprocess
from bs4 import Tag

class Document(object):
    def __init__(self, bs_content):
        self.id = bs_content.docno.string.strip()
        self.vocabulary = {}
        self.add_vocab(bs_content)

    def add_word_to_vocab(self, word):
        if word in self.vocabulary:
            self.vocabulary[word] += 1
        else:
            self.vocabulary[word] = 1

    def add_vocab(self, bs_content):
        if bs_content.find("dateline") is not None:
            preprocessed_dateline = preprocess(bs_content.dateline.string)
            for word in preprocessed_dateline:
                self.add_word_to_vocab(word)

        if bs_content.find("byline") is not None:
            preprocessed_byline = preprocess(bs_content.byline.string)
            for word in preprocessed_byline:
                self.add_word_to_vocab(word)

        if bs_content.find("head") is not None:
            preprocessed_headline = preprocess(bs_content.head.string)
            for word in preprocessed_headline:
                self.add_word_to_vocab(word)

        for text_content in bs_content.find_all("text"):
            preprocessed_text = preprocess(text_content.get_text())
            for word in preprocessed_text:
                self.add_word_to_vocab(word)
