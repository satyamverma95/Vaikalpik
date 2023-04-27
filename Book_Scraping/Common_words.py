import nltk
import string
from nltk.util import ngrams
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from Book_Scrape import get_book_text
from collections import defaultdict
# define the documents
doc1 = get_book_text('ML.pdf')
doc2 = get_book_text('Prob.pdf')

# clean the documents by removing punctuation, lowercasing, and stop words
stop_words = set(stopwords.words("english"))
def clean_doc(doc):
    doc = doc.translate(str.maketrans("", "", string.punctuation))
    doc = doc.lower()
    doc = word_tokenize(doc)
    doc = [word for word in doc if word not in stop_words]
    return set(doc)

doc1_set = clean_doc(doc1)
doc2_set = clean_doc(doc2)

# find common words
common_words = doc1_set & doc2_set

print("Common words between the documents:", common_words)

# To Find common biagrams

# find bigrams in the documents
def get_bigrams(doc):
    doc = doc.translate(str.maketrans("", "", string.punctuation))
    tokens = word_tokenize(doc)
    stop_words = set(stopwords.words("english"))
    tokens = [token for token in tokens if token not in stop_words]
    # Extract bigrams from the tokenized words
    bigrams = ngrams(tokens, 2)
    return [" ".join(bigram) for bigram in bigrams]

doc1_bigrams = get_bigrams(doc1)
doc2_bigrams = get_bigrams(doc2)

# find common bigrams
common_bigrams = set(doc1_bigrams) & set(doc2_bigrams)


print("Common bigrams between the documents:",common_bigrams)

# To Find common triagrams

def get_triagrams(doc):
    doc = doc.translate(str.maketrans("", "", string.punctuation))
    tokens = word_tokenize(doc)
    stop_words = set(stopwords.words("english"))
    tokens = [token for token in tokens if token not in stop_words]
    # Extract bigrams from the tokenized words
    triagrams = ngrams(tokens, 3)
    return [" ".join(triagram) for triagram in triagrams]

doc1_triagrams = get_triagrams(doc1)
doc2_triagrams = get_triagrams(doc2)

# find common trigrams

common_triagrams = set(doc1_triagrams) & set(doc2_triagrams)

print("Common triagrams between the documents:",common_triagrams)