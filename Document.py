class Document(object):
	def __init__(self, bs_content):
		self.id = bs_content.docno.string.strip()
		self.vocabulary = {}
		self.add_vocab(bs_content)

	def add_word_to_vocab(self, word):
		word = word.replace(',', '')
		word = word.replace('`', '')
		word = word.replace('.', ' ')
		word = word.replace('-', '')

		if(word.strip() is not ''):
			if(word in self.vocabulary):
				self.vocabulary[word] += 1
			else:
				self.vocabulary[word] = 1

	def add_vocab(self, bs_content):
		if(bs_content.find('dateline') is not None):
			for word in bs_content.dateline.string.split():
				self.add_word_to_vocab(word)

		if(bs_content.find('byline') is not None):
			for word in bs_content.byline.string.split():
				self.add_word_to_vocab(word)

		for text_content in bs_content.find_all('text'):
			for word in text_content.get_text().split():
				self.add_word_to_vocab(word)

