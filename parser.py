import os
from bs4 import BeautifulSoup
from Document import Document
from InvertedIndex import InvertedIndex


if __name__ == '__main__':
	dictionary = {}
	path = '/home/stark/Projects/vector-space-retrieval-model/data/TaggedTrainingAP/'
	for filename in os.listdir(path):
		with open(path + filename) as file:
			print(filename)
			content = file.readlines()
			content = ''.join(content)
			bs_content = BeautifulSoup(content, 'lxml')
			for doc in bs_content.find_all('doc'):
				document = Document(doc)
				dictionary[document.id] = document.vocabulary

	idx = InvertedIndex(dictionary)
	idx.save()
	
	dict_output = open('indexfile.dict', 'wb')
	dict_output.write(bytes(str(dictionary).encode('utf-8')))
	dict_output.close()

