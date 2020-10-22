import string
import pickle
import nltk
from nltk.stem import SnowballStemmer


def preprocess(text, query=False):
    """
    Preprocessing Steps:
            1) Convert to lower case.
            2) Remove Punctuations
            3) Tokenize text
            4) Remove Stop Words
            5) Stemming
            6) Add Lemmatization
    """
    text = text.lower()
    punctuations = string.punctuation
    if query:
        punctuations = punctuations.replace("*", "")
        punctuations = punctuations.replace(":", "")
    text_p = "".join([char if char not in punctuations else ' ' for char in text])    
    """
	For more optimal preprocessing we can compare python.split() vs nltk.tokenize.
	"""
    words = text_p.split()
    porter = SnowballStemmer("english")
    stemmed = [porter.stem(word) for word in words]
    return stemmed


def save_file(dict_object, path):
    dict_output = open(path, "wb")
    pickle.dump(dict_object, dict_output, pickle.HIGHEST_PROTOCOL)
    dict_output.close()


def load_file(path):
    dict_file = open(path, "rb")
    dict_object = pickle.load(dict_file)
    dict_file.close()
    return dict_object
