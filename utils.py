import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import string
import pickle


def preprocess(text):
	'''
	Preprocessing Steps:
		1) Convert to lower case.
		2) Remove Punctuations
		3) Tokenize text
		4) Remove Stop Words
		5) Stemming
	'''
	text = text.lower()
	text_p = "".join([char for char in text if char not in string.punctuation])
	words = nltk.word_tokenize(text_p)
	filter_stop_words = [word for word in words if word not in stopwords.words('english')]
	porter = PorterStemmer()
	stemmed = [porter.stem(word) for word in filter_stop_words]
	return stemmed

def save_dict(dict_object, path):
	dict_output = open(path, 'wb')
	pickle.dump(dict_object, dict_output, pickle.HIGHEST_PROTOCOL)
	dict_output.close()

def load_dict(path):
	dict_file = open(path, 'rb')
	dict_object = pickle.load(dict_file)
	dict_file.close()
	return dict_object
