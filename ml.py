import random

from classifiers import *
from encoders import *
from hprovers import *

random.seed(1234)


def padded_path(xs, max_l, pad=(0, 0)):
    ys = [(a + 1, b + 1) for (a, b) in xs]
    l = len(ys)
    assert l <= max_l
    zs = ys + ([pad] * (max_l - l))
    return zs


def padded_seq(xs, max_l, pad=0):
    ys = [a + 1 for a in xs]
    l = len(ys)
    assert l <= max_l
    zs = ys + ([pad] * (max_l - l))
    return zs


def to_path_of_pairs(ts):
    xss = [path_of(t) for t in ts]
    max_l = max(len(xs) for xs in xss)
    for xs in xss:
        yield padded_path(xs, max_l, pad=(0, 0))


def to_def_code(ts):
    xss = [df_code(t) for t in ts]
    max_l = max(len(xs) for xs in xss)
    for xs in xss:
        yield padded_seq(xs, max_l, pad=0)


def path_encoder(ts):
    for ys in to_path_of_pairs(ts):
        yield [z for xy in ys for z in xy]


def complex2pair(z):
    return abs(z), phase(z)


def bijective_encoder(ts, bijection=None):
    for ps in to_path_of_pairs(ts):
        cs = path2cs(ps)
        fs = bijection(cs)
        yield [z for xy in fs for z in complex2pair(xy)]


def polar_encoder(ts):
    yield from bijective_encoder(ts, bijection=identity)


def fft_encoder(ts):
    yield from bijective_encoder(ts, bijection=cs2fft)


def poly_encoder(ts):
    yield from bijective_encoder(ts, bijection=cs2poly)


class ProofSet:
    def __init__(self,
                 generator=hFormula,
                 prover=hprove,
                 encoder=path_encoder,
                 term_size=6):
        self.formulas = []
        self.proven = []
        self.term_size = term_size
        self.generator = generator
        self.prover = prover
        self.encoder = encoder

    def fresh_build(self, show=True):
        for formula in self.generator(self.term_size):
            is_proven = self.prover(formula)
            self.formulas.append(formula)
            self.proven.append(is_proven)
        codes = list(self.encoder(self.formulas))
        X = codes
        y = self.proven
        if show:
            print('Dataset:', self)
            s = sum(self.proven)
            l = len(self.formulas)
            r = round(s / l, 4)
            print('Formulas:', l, 'Size:', self.term_size,
                  'Proven:', s, 'Ratio:', r, '\n')
        return X, y

    def build(self, show=True):
        Xy = self.load()
        if not Xy:
            Xy = self.fresh_build(show=show)
            self.store(*Xy)
        return Xy

    def __repr__(self):
        fs = self.generator, self.prover, self.encoder
        ns = [f.__name__ for f in fs] + [str(self.term_size)]
        return "-".join(ns)

    def cache_name(self):
        return PARAMS["CACHE"] + str(self) + ".json"

    def store(self, X, y):
        fname = self.cache_name()
        ensure_path(fname)
        to_json((X, y), fname)

    def load(self):
        fname = self.cache_name()
        if not exists_file(fname): return None
        return from_json(fname)


class DataSet(ProofSet):
    def __init__(self, split_perc=10, **kwargs):
        super().__init__(**kwargs)
        self.split_perc = split_perc

    def split(self):
        X, y = self.build()
        assert len(X) == len(y)
        data_size = len(X)
        k = self.split_perc * data_size // 100
        Xy = list(zip(X, y))
        random.shuffle(Xy)
        vaXy, teXy = [], []
        for _ in range(k):
            vaXy.append(Xy.pop())
        for _ in range(k):
            teXy.append(Xy.pop())
        X_tr, y_tr = zip(*Xy)
        X_va, y_va = zip(*vaXy)
        X_te, y_te = zip(*teXy)
        return X_tr, y_tr, X_va, y_va, X_te, y_te


class Learner:
    def __init__(self, classifier=rf_clf, dataset=None, score='auc'):
        self.classifier = classifier
        self.score = score
        self.X_tr, self.y_tr, self.X_va, self.y_va, self.X_te, self.y_te = \
            dataset.split()

    def run(self):
        res = run_with_data(self.classifier(),
                            self.X_tr, self.y_tr, self.X_va, self.y_va, self.X_te, self.y_te,
                            score=self.score)

        def show_aucs(aucs):
            print('SHOWING:',aucs)
            va, te = aucs
            print('\n', '-' * 40)
            print('VALIDATION', self.score, ':', round(va, 4))
            print('TEST      ', self.score, ':', round(te, 4))
            print('-' * 40)

        show_aucs(res)


# tests

def test_ml1():
    D = DataSet(generator=hFormula, term_size=6)
    L = Learner(classifier=rf_clf, dataset=D)
    L.run()


def test_ml2():
    D = DataSet(generator=sFormula, term_size=7)
    L = Learner(classifier=rf_clf, dataset=D)
    L.run()


def test_ml3():
    D = DataSet(generator=sFormula, term_size=6)
    L = Learner(classifier=neural_clf, dataset=D)
    L.run()


def test_ml4():
    D = DataSet(generator=sFormula, encoder=fft_encoder, term_size=7)
    L = Learner(classifier=neural_clf, dataset=D)
    L.run()


def test_ml5():
    D = DataSet(generator=sFormula, encoder=poly_encoder, term_size=7)
    L = Learner(classifier=rf_clf, dataset=D)
    L.run()


def test_ml6():
    D = DataSet(generator=sFormula, encoder=polar_encoder, term_size=7)
    L = Learner(classifier=rf_clf, dataset=D, score='auc')
    L.run()


def test_ml7():
    D = DataSet(generator=ranHorns,
                # encoder=polar_encoder,
                term_size=18)
    L = Learner(classifier=rf_clf, dataset=D)
    L.run()


def test_ml8():
    D = DataSet(generator=mixHorns,
                # encoder=polar_encoder,
                term_size=18)
    L = Learner(classifier=rf_clf, dataset=D, score='auc')
    L.run()


def test_ml9():
    D = DataSet(generator=sFormula,
                encoder=to_def_code,
                term_size=7)
    L = Learner(classifier=rf_clf, dataset=D, score='acc')
    L.run()


def test_ml10():
    D = DataSet(generator=sFormula,
                encoder=to_def_code,
                term_size=7)
    L = Learner(classifier=neural_clf, dataset=D, score='acc')
    L.run()


def test_ml11():
    D = DataSet(  # generator=sFormula,
        generator=mixHorns,
        encoder=to_def_code,
        term_size=7)
    L = Learner(classifier=rf_clf, dataset=D, score='cross')
    L.run()


def test_ml12():
    D = DataSet(  # generator=sFormula,
        generator=mixHorns,
        encoder=to_def_code,
        term_size=7)
    L = Learner(classifier=neural_clf, dataset=D, score='cross')
    L.run()


test_ml = test_ml4

if __name__ == "__main__":
    pass
    test_ml()
