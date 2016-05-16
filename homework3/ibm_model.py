import collections
import sys

class Counts:
    def __init__(self):
        self.word = collections.defaultdict(int)
        self.words = collections.defaultdict(int)
        self.alignment = collections.defaultdict(int)
        self.alignments = collections.defaultdict(int)


class Model:
    def recalculate(self, counts):
        self.counts = counts
        self.initialize_step = False
        self.initialize_step_2 = False

    def p(self, e, f, j, i, l, m):
        pass

    def t(self, f, e):
        if self.initialize_step:
            return 1.0 / self.counts.word[e]
        else:
            if self.counts.word[e] > 0:
                return self.counts.words[(e, f)] / self.counts.word[e]
            else:
                return 0

    def align(self, esent, fsent):
        l = len(esent)
        m = len(fsent)
        alignment = []
        for i, f_i in enumerate(fsent):
            j, p = amax([(j, self.p(e_j, f_i, j, i, l, m)) for j, e_j in enumerate(esent)])
            alignment.append(j)
        return alignment


class IBMModel1(Model):
    def __init__(self, counts):
        self.initialize_step = True
        self.initialize_step_2 = False
        self.counts = counts

    def p(self, e, f, j, i, l, m):
        return self.t(f, e)


class IBMModel2(Model):
    def __init__(self, model1):
        self.initialize_step = False
        self.initialize_step_2 = True
        self.counts = model1.counts

    def q(self, j, i, l, m):
        if self.initialize_step_2:
            return 1.0 / (l + 1.0)
        else:
            if self.counts.alignment[(i, l, m)] > 0.0:
                return self.counts.alignments[(j, i, l, m)] / self.counts.alignment[(i, l, m)]
            else:
                return 0.0

    def p(self, e, f, j, i, l, m):
        return self.t(f, e) * self.q(j, i, l, m)


class Counter:
    def __init__(self, target, source):
        self.both = list(zip(target, source))

    def initialize_counts(self):
        self.initial_counts = Counts()
        for e, f in self.both:
            for e_j in e:
                for f_i in f:
                    key = (e_j, f_i)
                    if key not in self.initial_counts.words:
                        self.initial_counts.words[key] = 1.0
                        if e_j not in self.initial_counts.word:
                            self.initial_counts.word[e_j] = 1.0
                        else:
                            self.initial_counts.word[e_j] += 1.0
                    else:
                        self.initial_counts.words[key] += 1.0
        return self.initial_counts

    def estimate_counts(self, model):
        counts = Counts()
        for k, (e, f) in enumerate(self.both):
            l = len(e)
            m = len(f)
            for i, f_i in enumerate(f):
                denominator = sum((model.p(e_j, f_i, j, i, l, m) for (j, e_j) in enumerate(e)))
                for j, e_j in enumerate(e):
                    if denominator > 0.0:
                        delta = model.p(e_j, f_i, j, i, l, m) / denominator
                    else:
                        delta = 0
                    counts.words[(e_j, f_i)] += delta
                    counts.word[e_j] += delta
                    counts.alignments[(j, i, l, m)] += delta
                    counts.alignment[(i, l, m)] += delta
        return counts


def amax(l):
    if not l:
        return None, 0
    else:
        return max(l, key=lambda x: x[1])


def em_algorithm(counter, model, iterations):
    for i in range(iterations):
        counts = counter.estimate_counts(model)
        model.recalculate(counts)
    return model


def ibm_model1(target, source):
    counter = Counter(target, source)
    counts = counter.initialize_counts()
    model = IBMModel1(counts)
    model = em_algorithm(counter, model, 5)
    return model


def ibm_model2(model1, target, source):
    counter = Counter(target, source)
    model = IBMModel2(model1)
    del model1
    model = em_algorithm(counter, model, 5)
    return model


def align(model, t, s, k, out=sys.stdout):
    for i in range(k):
        alignment = model.align(t[i], s[i])
        out.write(" ".join(t[i]) + "\n")
        out.write(" ".join(s[i]) + "\n")
        out.write(str(alignment) + "\n\n")

