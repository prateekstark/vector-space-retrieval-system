from utils import preprocess, load_dict
import math
import operator


class Search(object):
	def __init__(self, dictionary_filepath, inverted_index_filepath):
		self.dictionary = load_dict(dictionary_filepath)
		self.inverted_index = load_dict(inverted_index_filepath)
		self.collection_size = len(self.dictionary)

	def get_possible_documents(self, query):
		document_set = set()
		for word in query:
			if(word in self.inverted_index):
				document_set.update(self.inverted_index[word])
		return document_set

	def get_ranking_list(self, query):
		query = preprocess(query)
		possible_documents = self.get_possible_documents(query)
		
		ranking_dict = {}

		for doc in possible_documents:
			weight_sum = 0
			for word in query:
				tf = 0
				if(word in self.dictionary[doc]):
					frequency = self.dictionary[doc][word]
					tf = 1 + math.log2(frequency)
				if(tf == 0):
					continue
				else:
					df = self.collection_size / len(self.inverted_index[word])
					idf = math.log2(1 + df)
				weight_sum += tf * idf
			ranking_dict[doc] = weight_sum
		sorted_d = sorted(ranking_dict.items(), key=operator.itemgetter(1), reverse=True)
		print(sorted_d)

if __name__ == '__main__':
	search = Search('./indexfile.dict', './indexfile.idx')
	query = "Vietnam has internal divisons."
	search.get_ranking_list(query)