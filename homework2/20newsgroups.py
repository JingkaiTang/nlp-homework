#! /usr/bin/env python
import os
import functools
import chardet

from sklearn.metrics import classification_report, accuracy_score
from sklearn.cross_validation import train_test_split

DATA_BASE_DIR = 'data'
DATA_DIR = '20_newsgroups'

base_dir = os.path.dirname(os.path.abspath(__file__))
print('base dir: %s' % base_dir)
data_base_dir = os.path.join(base_dir, DATA_BASE_DIR)
print('data base dir: %s' % data_base_dir)
data_dir = os.path.join(data_base_dir, DATA_DIR)
print('data dir: %s' % data_dir)

if not os.path.exists(data_base_dir):
    os.mkdir(data_base_dir)

if not os.path.exists(data_dir):
    pass


def prepare_file(folder, filename):
    fp = os.path.join(folder, filename)
    raw_data = open(fp, 'rb').read()
    codec = chardet.detect(raw_data)
    return raw_data.decode(codec.get('encoding', 'utf-8'))


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

categories = os.listdir(data_dir)
print('categories', categories)
documents, classes = get_texts(categories)
print('classes', classes)

train_docs, test_docs, train_classes, test_classes = train_test_split(documents, classes, train_size=0.7)
print('len of train: %d' % len(train_docs))
print('len of test: %d' % len(test_docs))

#from sklearn.feature_extraction.text import HashingVectorizer
from nltk.corpus import stopwords

#vectorizer = HashingVectorizer(stop_words='english', non_negative=True, n_features=10000)

from naivebayes import NaiveBayesTextClassifier
clf = NaiveBayesTextClassifier(categories=categories, min_df=1, lowercase=True, stop_words=stopwords.words('english'))
clf.train(train_docs, train_classes)

print("-" * 42)
print("{:<25}: {:>6} articles".format("Total", len(train_docs)))
print("{:<25}: {:>6} words".format(
    "Number of words", clf.bag.shape[1]
))
print("-" * 42)

print("> Start classify test data")
predicted_classes = clf.classify(test_docs)


def category_to_number(classes, category_type):
    return list(map(category_type.index, classes))


print(classification_report(test_classes, predicted_classes))
print('-' * 42)
print("{:<25}: {:>6} articles".format("Test data size", len(test_classes)))
print("{:<25}: {:>6.2f} %".format(
    "Accuracy", 100 * accuracy_score(test_classes, predicted_classes))
)
print('-' * 42)
