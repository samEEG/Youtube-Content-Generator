# Natural Language Processing

# Importing the libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Importing the dataset
dataset = pd.read_csv('foo.tsv', delimiter = '\t', quoting = 3, lineterminator='\n')

# Cleaning the texts
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
corpus = []
# Change size number based on size of dataset 
for i in range(0, 6823):
    review = re.sub('[^a-zA-Z]', ' ', dataset['Comment'][i])
    review = review.lower()
    review = review.split()
    temp = [] 
    for word in review: 
        if not word in set(stopwords.words('english')):
            temp.append(word)
    corpus.append(temp)
    
#Word to vec model 
from gensim.models import Word2Vec
model = Word2Vec(corpus, min_count=1, size = 200, workers = 8)

result = model.most_similar(positive=['video', 'streaming', 'problems'], topn=10)
print(result)