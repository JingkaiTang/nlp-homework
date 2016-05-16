#!/usr/bin/env python

from ibm_model import ibm_model1, ibm_model2, align


def read_corpus(corpus):
    return [line.split() for line in open(corpus).readlines()]

if __name__ == '__main__':
    tf = 'res/en.txt'
    sf = 'res/zh.txt'
    t = read_corpus(tf)
    s = read_corpus(sf)

    model1 = ibm_model1(t, s)
    align(model1, t, s, 10000, open('m1.txt', 'w'))

    model2 = ibm_model2(model1, t, s)
    align(model2, t, s, 10000, open('m2.txt', 'w'))
