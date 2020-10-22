import math
import operator
from utils import save_file, load_file, preprocess
from bs4 import Tag


class InvertedIndex(object):
    def __init__(self, dictionary_filepath=None, postings_list_filepath=None):
        self.postings_list = []
        self.dictionary = {
            "person": {},
            "organization": {},
            "location": {},
            "rest": {},
            "normalization_factor": {},
        }
        self.vocabulary = {"person": {}, "organization": {}, "location": {}, "rest": {}}
        self.collection_size = 0

        if dictionary_filepath:
            self.dictionary = load_file(dictionary_filepath)
        if postings_list_filepath:
            self.postings_list = load_file(postings_list_filepath)

    def assign_postings_list(self):
        index = 0
        for category in ["organization", "person", "location", "rest"]:
            for word in self.vocabulary[category]:
                self.postings_list.append(self.vocabulary[category][word])
                df = self.collection_size / len(self.vocabulary[category][word])
                idf = math.log2(1 + df)
                self.dictionary[category][word] = [df, index]

                for doc_id in self.vocabulary[category][word]:
                    frequency = self.vocabulary[category][word][doc_id]
                    tf = 1 + math.log2(frequency)
                    self.dictionary["normalization_factor"][doc_id] += pow(tf * idf, 2)
                index += 1
        for doc_id in self.dictionary["normalization_factor"]:
            self.dictionary["normalization_factor"][doc_id] = math.sqrt(
                self.dictionary["normalization_factor"][doc_id]
            )

    def add_word_in_vocab(self, word, doc_id, category="rest", add_factor=1):
        if word in self.vocabulary[category]:
            if doc_id in self.vocabulary[category][word]:
                self.vocabulary[category][word][doc_id] += 1
            else:
                self.vocabulary[category][word][doc_id] = 1
        else:
            self.vocabulary[category][word] = {doc_id: 1}

    def add_section(self, section, doc_id, section_id="text"):
        if section is None:
            return
        category = "rest"
        if section_id != "text":
            content = section.string
            if section_id == "dateline":
                content = content.replace("(AP)", "")
                category = "location"
            preprocessed_content = preprocess(content)
            for word in preprocessed_content:
                self.add_word_in_vocab(word, doc_id, category=category)
        else:
            for content in section:
                for part in content:
                    if len(part) > 3:
                        preprocessed_part = preprocess(part)
                        for word in preprocessed_part:
                            self.add_word_in_vocab(word=word, doc_id=doc_id)
                    elif isinstance(part, Tag):
                        preprocessed_word = preprocess(part.string)
                        for word in preprocessed_word:
                            self.add_word_in_vocab(
                                word, doc_id=doc_id, category=part.name
                            )

    def add_doc(self, doc):
        doc_id = doc.docno.string.strip()
        self.add_section(doc.find("dateline"), doc_id, "dateline")
        self.add_section(doc.find("byline"), doc_id, "byline")
        self.add_section(doc.find("head"), doc_id, section_id="head")
        self.add_section(doc.find_all("text"), doc_id)
        self.dictionary["normalization_factor"][doc_id] = 0
        self.collection_size += 1

    def save(self, name="indexfile", path="./"):
        save_file(self.postings_list, path + name + ".idx")
        save_file(self.dictionary, path + name + ".dict")

    def get_possible_documents(self, query):
        document_set = set()
        for word in query:
            tagged_query = False

            if word.startswith("p:"):
                category = "person"
                tagged_query = True

            elif word.startswith("o:"):
                category = "organization"
                tagged_query = True

            elif word.startswith("l:"):
                category = "location"
                tagged_query = True

            elif word.startswith("n:"):
                category = "all"
                tagged_query = True

            if word[-1] != "*":
                if not tagged_query:
                    for key in ["organization", "person", "location", "rest"]:
                        if word in self.dictionary[key]:
                            index = self.dictionary[key][word][1]
                            document_set.update(self.postings_list[index].keys())
                else:
                    if category == "all":
                        for key in ["location", "organization", "person"]:
                            if word in self.dictionary[key]:
                                index = self.dictionary[key][word[2:]][1]
                                document_set.update(self.postings_list[index].keys())
                    else:
                        if word[2:] in self.dictionary[category]:
                            index = self.dictionary[category][word[2:]][1]
                            document_set.update(self.postings_list[index].keys())
            else:
                if not tagged_query:
                    for key in ["organization", "person", "location", "rest"]:
                        for element in self.dictionary[key]:
                            if element.startswith(word[:-1]):
                                index = self.dictionary[key][1]
                                document_set.update(self.postings_list[index].keys())
                else:
                    if category == "all":
                        for key in ["location", "organization", "person"]:
                            for element in self.dictionary[key]:
                                if element.startswith(word[:-1]):
                                    index = self.dictionary[key][1]
                                    document_set.update(
                                        self.postings_list[index].keys()
                                    )
                    else:
                        for element in self.dictionary[category]:
                            if element.startswith(word[2:-1]):
                                index = self.dictionary[category][element][1]
                                document_set.update(self.postings_list[index].keys())
        return document_set

    def get_ranking_list(self, query):
        query = preprocess(query, query=True)
        possible_documents = self.get_possible_documents(query)
        ranking_dict = {}

        for doc in possible_documents:
            weight_sum = 0
            for word in query:
                tagged_query = False
                if word.startswith("l:"):
                    tagged_query = True
                    category = "location"
                    word = word[2:]

                elif word.startswith("o:"):
                    tagged_query = True
                    category = "location"
                    word = word[2:]

                elif word.startswith("p:"):
                    tagged_query = True
                    category = "location"
                    word = word[2:]

                elif word.startswith("n:"):
                    tagged_query = True
                    category = "all"
                    word = word[2:]

                if word[-1] != "*":
                    if not tagged_query:
                        reverse_freq = 0
                        indices = []
                        for key in ["organization", "person", "location", "rest"]:
                            if word in self.dictionary[key]:
                                indices.append(self.dictionary[key][word][1])
                                reverse_freq += 1 / self.dictionary[key][word][0]
                        if reverse_freq == 0:
                            continue

                        frequency = 0
                        for index in indices:
                            if doc in self.postings_list[index]:
                                frequency += self.postings_list[index][doc]

                        if frequency == 0:
                            continue

                        tf = 1 + math.log2(frequency)
                        df = 1 / reverse_freq
                        idf = math.log2(1 + df)
                        weight_sum += tf * idf
                    else:
                        if category == "all":
                            reverse_freq = 0
                            indices = []
                            for key in ["location", "organization", "people"]:
                                if word in self.dictionary[key]:
                                    indices.append(self.dictionary[key][word][1])
                                    reverse_freq += 1 / self.dictionary[key][word][0]

                            if reverse_freq == 0:
                                continue

                            frequency = 0
                            for index in indices:
                                if doc in self.postings_list[index]:
                                    frequency += self.postings_list[index][doc]

                            if frequency == 0:
                                continue

                            tf = 1 + math.log2(frequency)
                            df = 1 / reverse_freq
                            idf = math.log2(1 + df)
                            weight_sum += tf * idf
                        else:
                            df = 0
                            if word in self.dictionary[category]:
                                index = self.dictionary[category][word][1]
                                df = self.dictionary[category][word][0]
                            if df == 0:
                                continue

                            frequency = 0

                            if doc in self.postings_list[index]:
                                frequency = self.postings_list[index][doc]

                            if frequency == 0:
                                continue

                            tf = 1 + math.log2(frequency)
                            idf = math.log2(1 + df)
                            weight_sum += tf * idf

                else:
                    if not tagged_query:
                        word = word[:-1]
                        reverse_freq = 0
                        indices = 0
                        for key in ["organization", "person", "location", "rest"]:
                            for element in self.dictionary[key]:
                                if element.startswith(word):
                                    reverse_freq += 1 / self.dictionary[key][element][0]
                                    index = self.dictionary[key][element][1]
                                    indices.append(index)

                        if reverse_freq == 0:
                            continue

                        frequency = 0
                        for index in indices:
                            if doc in self.postings_list[index]:
                                frequency += self.postings_list[index][doc]

                        if frequency == 0:
                            continue

                        df = 1 / reverse_freq
                        idf = math.log2(1 + df)
                        tf = 1 + math.log2(frequency)
                        weight_sum += tf * idf

                    else:
                        if category == "all":
                            word = word[:-1]
                            reverse_freq = 0
                            indices = 0
                            for key in ["location", "organization", "person"]:
                                for element in self.dictionary[key]:
                                    if element.startswith(word):
                                        reverse_freq += (
                                            1 / self.dictionary[key][element][0]
                                        )
                                        index = self.dictionary[key][element][1]
                                        indices.append(index)

                            if reverse_freq == 0:
                                continue

                            frequency = 0
                            for index in indices:
                                if doc in self.postings_list[index]:
                                    frequency += self.postings_list[index][doc]

                            if frequency == 0:
                                continue

                            df = 1 / reverse_freq
                            idf = math.log2(1 + df)
                            tf = 1 + math.log2(frequency)
                            weight_sum += tf * idf

                        else:
                            word = word[:-1]
                            reverse_freq = 0
                            indices = []
                            for element in self.dictionary[category]:
                                if element.startswith(word):
                                    reverse_freq += 1 / self.dictionary[key][element][0]
                                    index = self.dictionary[key][element][1]
                                    indices.append(index)

                            if reverse_freq == 0:
                                continue

                            frequency = 0
                            for index in indices:
                                if doc in self.postings_list[index]:
                                    frequency += self.postings_list[index][doc]

                            if frequency == 0:
                                continue

                            df = 1 / reverse_freq
                            idf = math.log2(1 + df)
                            tf = 1 + math.log2(frequency)
                            weight_sum += tf * idf

            ranking_dict[doc] = (
                weight_sum / self.dictionary["normalization_factor"][doc]
            )
        sorted_d = sorted(
            ranking_dict.items(), key=operator.itemgetter(1), reverse=True
        )
        return sorted_d
