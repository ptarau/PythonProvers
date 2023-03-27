import timeit


def hprove(GBs):
    """
    Prover for Intuitionstic Implicational Formulas
    in equivalent Nested Horn Clauses form

    """
    G, Bs = GBs
    return any(ljh(G, Bs))


def ljh(G, Vs):
    # print('ljh:', G, Vs)
    if G in Vs:
        yield True
    elif isinstance(G, tuple):
        H, Bs = G
        yield any(ljh(H, Bs + Vs))
    elif check_head(G, Vs):
        for X, Vs2 in select(Vs):
            if not isinstance(X, tuple): continue
            (B, As) = X
            for A, Bs in select(As):
                if ljh_imp(A, B, Vs2):
                    NewB = trimmed((B, Bs))
                    yield any(ljh(G, [NewB] + Vs2))


def ljh_imp(X, B, Vs):
    # print('ljh_imp:',X,B,Vs)
    if not isinstance(X, tuple):
        return X in Vs
    else:
        D, Cs = X
        R = any(ljh(X, [(B, [D])] + Vs))
        return R


def check_head(G, Vs):
    for X in Vs:
        if isinstance(X, tuple):
            if G == X[0]: return True
        elif G == X:
            return True
    return False


def trimmed(X):
    H, Bs = X
    if not Bs: return H
    return X


def select(xs):
    for i in range(len(xs)):
        yield xs[i], xs[:i] + xs[i + 1:]


def hprove_(GBs):
    """
    Prover for Intuitionstic Implicational Formulas
    in equivalent Nested Horn Clauses form

    variant with tracing anabled
    """
    G, Bs = GBs
    # print(G,'assuming',Bs)
    return any(ljh_(G, Bs))


def ljh_(G, Vs):
    if G in Vs:
        # print(G,'if0',Vs)
        yield True
    elif isinstance(G, tuple):
        H, Bs = G
        R = any(ljh_(H, Bs + Vs))
        # print(G,'if1',Bs+Vs)
        yield R
    elif check_head(G, Vs):
        for X, Vs2 in select(Vs):
            if not isinstance(X, tuple): continue
            # print('choice1', X)
            (B, As) = X
            for A, Bs in select(As):
                # print('choice2',A)
                if ljh_imp_(A, B, Vs2):
                    NewB = trimmed((B, Bs))
                    R = any(ljh_(G, [NewB] + Vs2))
                    # print(G,'if2',[NewB] + Vs2)
                    yield R


def ljh_imp_(X, B, Vs):
    if not isinstance(X, tuple):
        # print(X,'if4',Vs)
        return X in Vs
    else:
        D, Cs = X
        R = any(ljh_(X, [(B, [D])] + Vs))
        # print(X, '<---if5____', [(B, [D])] + Vs)
        return R


# to make this self-contained, for testing with pypy

def partition_(xs):
    if len(xs) == 1:
        yield [xs]
        return

    first = xs[0]
    for smaller in partition_(xs[1:]):
        # insert `first` in each of the subpartition's subsets
        for n, subset in enumerate(smaller):
            yield smaller[:n] + [[first] + subset] + smaller[n + 1:]
        # put `first` in its own subset
        yield [[first]] + smaller


# from partition as list of list, to list of indices
def part2list_(N, pss):
    res = []
    l = len(pss)
    for i in range(N):
        for j in range(l):
            if i in pss[j]:
                res.append(j)
    return res


def list_partition(n):
    xs = list(range(n))
    for pss in partition_(xs):
        yield part2list_(n, pss)


def horn_(n):
    """
    generates nested horn clauses of size n
    """
    if n == 0:
        yield 'o', []
    else:
        for k in range(0, n):
            for f, l in horn_(k):
                for g, r in horn_(n - 1 - k):
                    yield g, [(f, l)] + r


def decorate_horn_(tree, leafIter):
    x = leafIter.__next__()
    _, bs = tree
    if not bs:
        return x
    else:
        return x, [decorate_horn_(b, leafIter) for b in bs]


def hFormula_(n):
    """
    nested Horn formulas
    """
    for tree in horn_(n):
        for lpart in list_partition(n + 1):
            atomIter = iter(lpart)
            yield decorate_horn_(tree, atomIter)


# tests

def timer():
    return timeit.default_timer()


def test_select():
    xs = [1, 2]
    for x in select(xs): print(*x)


def hptest():
    a, b, c, d, X, Y = 0, 1, 2, 3, 4, 5
    X = (d, [(b, [(d, [c])]), c])
    Y = (d, [(b, [d]), c])
    hprove_((X, [Y]))
    print('')
    hprove_((Y, [X]))


def xptest():
    xCombType = (7, [(7, [(0, [0, 1]), (4, [(4, [2, 3]), (3, [2]), 2]), (5, [5, 6])])])
    print('xCombType', hprove_(xCombType))


def test_hforms(n=4):
    proven = 0
    forms = 0
    t1 = timer()
    for t in hFormula_(n):
        forms += 1
        ok = hprove(t)
        proven += ok
    t2 = timer()
    failed = forms - proven
    print('formulas:', forms, 'proven:',
          proven, 'failed:', failed, 'density:', round(proven / forms, 4))
    print('TIME:', round(t2 - t1, 2))


class Term:
    def __init__(self, head, body=[]):
        self.head = head
        self.body = body

    def __repr__(self):
        h = str(self.head)
        if self.body == []:
            return "Term(" + h + ")"
        bs = "[" + ",".join(map(str, self.body)) + "]"
        return "Term(" + h + "," + bs + ")"


def hform2term(x):
    if not isinstance(x, tuple):
        return Term(x)
    h, bs = x
    ts = [hform2term(b) for b in bs]
    return Term(h, ts)


def show_hForms():
    for x in hFormula_(4):
        t = hform2term(x)
        print(x)
        print(t)
        print()


def save_hForms(n, suf='.tsv'):
    with open('hforms_' + str(n) + suf, 'w') as f:
        for i, x in enumerate(hFormula_(n)):
            ok = int(hprove(x))
            t = hform2term(x)
            print(ok, '\t', t, file=f)


def small_test():
    t = (0, [(0, [1]), 1])
    ok = hprove(t)
    print(t)
    print(ok)


if __name__ == "__main__":
    test_hforms(7)
    # hptest()
    # print('\n-------\n')
    # xptest()
    # show_hForms()
    # test_hforms(4)
    # save_hForms(2)
    # save_hForms(3)
    # save_hForms(4)
    # save_hForms(5)
    # save_hForms(6)
    # save_hForms(7)
    # small_test()
