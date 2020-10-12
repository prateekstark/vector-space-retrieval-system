class InvertedIndex(object):
	def __init__(self, document_list):
		self.vocabulary = {}
		self.add_docs(document_list)

	def add_docs(self, document_list):
		for doc_id in document_list:
			for word in document_list[doc_id]:
				if(word in self.vocabulary):
					self.vocabulary[word].append(doc_id)
				else:
					self.vocabulary[word] = [doc_id]

	def save(self, name='indexfile', path='./'):
		inv_indx_output = open(path + name + '.idx', 'wb')
		inv_indx_output.write(bytes(str(idx.vocabulary).encode('utf-8')))
		inv_indx_output.close()

