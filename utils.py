# utils.py

import nltk
from nltk.stem.porter import PorterStemmer

stemmer = PorterStemmer()

def tokenize(sentence):
    return nltk.word_tokenize(sentence)

def stem(word):
    return stemmer.stem(word.lower())

def bag_of_words(sentence, words):
    # Ensure sentence is a string
    if isinstance(sentence, list):
        sentence = ' '.join(sentence)
    sentence_words = [stem(w) for w in tokenize(sentence)]
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
    return bag