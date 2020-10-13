import os
import sys
from bs4 import BeautifulSoup
from Document import Document
from InvertedIndex import InvertedIndex
from utils import save_dict


if __name__ == '__main__':
	'''
	Default Values of folder path and index-filename
	'''
	path = '/home/stark/Projects/vector-space-retrieval-system/data/sliced/'
	index_filename = 'indexfile'
	
	if(len(sys.argv) == 3):
		path = sys.argv[1]
		index_filename = sys.argv[2]

	dictionary = {}
	for filename in os.listdir(path):
		file = open(path + filename)
		content = file.readlines()
		content = ''.join(content)
		bs_content = BeautifulSoup(content, 'lxml')
		for doc in bs_content.find_all('doc'):
			document = Document(doc)
			dictionary[document.id] = document.vocabulary
			del document
		file.close()

	idx = InvertedIndex(dictionary)
	
	idx.save(name=index_filename)
	save_dict(dictionary, index_filename + '.dict')
