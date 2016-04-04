#! /usr/bin/env python
import os
import functools

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
    filepath = os.path.join(folder, filename)
    with open(filepath, 'r', encoding='ascii') as f:
        return f.read()


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




