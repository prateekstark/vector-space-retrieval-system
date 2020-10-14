import math
import operator
from utils import preprocess, load_dict


class Search(object):
	def __init__(self, dictionary_filepath, inverted_index_filepath):
		self.dictionary = load_dict(dictionary_filepath)
		self.inverted_index = load_dict(inverted_index_filepath)
		self.collection_size = len(self.dictionary)

	def get_possible_documents(self, query):
		document_set = set()
		for word in query:
			if(word[-1] != '*'):
				if(word in self.inverted_index):
					document_set.update(self.inverted_index[word])
			else:
				for key in self.inverted_index:
					if(key.startswith(word[:-1])):
						document_set.update(self.inverted_index[key])
		return document_set

	def get_ranking_list(self, query):
		query = preprocess(query, query=True)
		possible_documents = self.get_possible_documents(query)
		ranking_dict = {}
		for doc in possible_documents:
			weight_sum = 0
			for word in query:
				if(word[-1] != '*'):
					frequency = 0
					if(word in self.dictionary[doc]):
						frequency = self.dictionary[doc][word]
					if(frequency == 0):
						continue
					tf = 1 + math.log2(frequency)
					df = self.collection_size / len(self.inverted_index[word])
					idf = math.log2(1 + df)
					weight_sum += tf * idf
				else:
					word = word[:-1]
					appeared_doc = 0
					for key in self.inverted_index:
						if(key.startswith(word)):
							appeared_doc += len(self.inverted_index[key])
					if(appeared_doc == 0):
						continue
		
					df = self.collection_size / appeared_doc
					idf = math.log2(1 + df)

					frequency = 0
					for key in self.dictionary[doc]:
						if(key.startswith(word)):
							frequency += self.dictionary[doc][key]
					if(frequency == 0):
						continue
					else:
						tf = 1 + math.log2(frequency)
					weight_sum += tf * idf
			ranking_dict[doc] = weight_sum
		sorted_d = sorted(ranking_dict.items(), key=operator.itemgetter(1), reverse=True)
		return sorted_d
