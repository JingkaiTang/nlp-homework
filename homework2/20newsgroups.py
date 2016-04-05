#! /usr/bin/env python
import os
import sys
import functools
import chardet

from nltk.corpus import stopwords
from sklearn.metrics import classification_report
from sklearn.cross_validation import train_test_split

from naivebayes import NaiveBayesTextClassifier

data_dir = sys.argv[1]

def prepare_file(folder, filename):
    fp = os.path.join(folder, filename)
    raw_data = open(fp, 'rb').read()
    codec = chardet.detect(raw_data)
    codec = codec.get('encoding')
    if not codec:
        codec = 'utf-8' 
    return raw_data.decode(codec)


def get_texts(categories):
    documents = []
    classes = []

    for category in categories:
        category_files_path = os.path.join(data_dir, category)
        text_ids = os.listdir(category_files_path)
        prepare_category_file = functools.partial(prepare_file, category_files_path)
        texts = [prepare_category_file(f) for f in text_ids]
        documents += texts
        classes += [category] * len(texts)

    return documents, classes

print('Get Gategories...')
categories = os.listdir(data_dir)
print('Reading Data...')
documents, classes = get_texts(categories)

train_docs, test_docs, train_classes, test_classes = train_test_split(documents, classes, train_size=0.9)

clf = NaiveBayesTextClassifier(categories=categories, min_df=1, lowercase=True, stop_words=stopwords.words('english'))

print('Training...')
clf.train(train_docs, train_classes)

print('Predicting...')
predicted_classes = clf.classify(test_docs)

print('Result:')
print('-' * 72)
print(classification_report(test_classes, predicted_classes))
print('-' * 72)

