from utils import save_dict, load_dict


class InvertedIndex(object):
	def __init__(self, document_list=None):
		self.vocabulary = {}
		if(document_list is not None):
			self.add_docs(document_list)

	def add_docs(self, document_list):
		for doc_id in document_list:
			for word in document_list[doc_id]:
				if(word in self.vocabulary):
					self.vocabulary[word].append(doc_id)
				else:
					self.vocabulary[word] = [doc_id]

	def save(self, name='indexfile', path='./'):
		save_dict(self.vocabulary, path + name + '.idx')

	def load(self, name='indexfile', path='./'):
		self.vocabulary = load_dict(path + name + '.idx')