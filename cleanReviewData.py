import nltk
from nltk.corpus import stopwords

import re


def cleanReview(review):
    stopwords = nltk.corpus.stopwords.words('english')
    br = ['br']
    stopwords.extend(br)
    review = review.decode("utf-8")
    review = review.replace('\n', ' ')

    review = re.sub('\d+', ' ', review)
    review = review.replace('-', '')
    review = review.replace('\'', '')
    review = review.replace('\"', '')
    review = re.sub(r"[,.;@#()<>:?!&$]+\ *", " ", review)
    review = review.lower()


    list = [word for word in nltk.wordpunct_tokenize(review) if word not in stopwords]
    return ' '.join(list)