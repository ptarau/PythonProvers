import timeit

from hprovers import hprove, hFormula_


def fhprove(GBs):
    """
    Prover for Intuitionstic Implicational Formulas
    in equivalent Nested Horn Clauses form

    """
    G, Bs = decons(GBs)
    return any(ljhf(G, Bs))


def ljhf(G, Vs):
    # print('!!', G, ':-', Vs)
    if G in Vs:
        yield True
    elif isinstance(G, tuple):
        H, Bs = decons(G)
        yield any(ljhf(H, Bs + Vs))
    elif check_head(G, Vs):
        for X, Vs2 in select(Vs):
            if not isinstance(X, tuple): continue
            B, As = decons(X)
            for A, Bs in select(As):
                if ljhf_imp(A, B, Vs2):
                    NewB = trimmed(B,Bs)
                    yield any(ljhf(G, (NewB,) + Vs2))


def ljhf_imp(X, B, Vs):
    if not isinstance(X, tuple):
        return X in Vs
    else:
        D, Cs = decons(X)
        R = any(ljhf(X, ((B, D),) + Vs))
        return R


def check_head(G, Vs):
    for X in Vs:
        if isinstance(X, tuple):
            if G == X[0]:
                return True
        elif G == X:
            return True
    return False


def trimmed(H,Bs):
    if not Bs: return H
    return (H,)+Bs


def select(xs):
    for i in range(len(xs)):
        yield xs[i], xs[:i] + xs[i + 1:]


def decons(x):
    return x[0], x[1:]


# to make this self-contained, for testing with pypy

def partition(xs):
    if len(xs) == 1:
        yield (xs,)
        return

    first = xs[0]
    for smaller in partition(xs[1:]):
        # insert `first` in each of the subpartition's subsets
        for n, subset in enumerate(smaller):
            yield smaller[:n] + ((first,) + subset,) + smaller[n + 1:]
        # put `first` in its own subset
        yield ((first,),) + smaller


# for x in partition((1,2,3,4)) : print(x)

# from partition as list of list, to list of indices
def part2list(N, pss):
    res = []
    l = len(pss)
    for i in range(N):
        for j in range(l):
            if i in pss[j]:
                res.append(j)
    return tuple(res)


def list_partition(n):
    xs = tuple(range(n))
    for pss in partition(xs):
        yield part2list(n, pss)


# for x in list_partition(4): print(x)

def decorate_horn(tree, leafIter):
    x = leafIter.__next__()
    _, bs = tree
    if not bs:
        return x
    else:
        return (x,) + tuple(decorate_horn(b, leafIter) for b in bs)


def fhFormula(n):
    """
    nested Horn formulas
    """
    for tree in horn(n):
        for lpart in list_partition(n + 1):
            atomIter = iter(lpart)
            yield decorate_horn(tree, atomIter)


def horn(n):
    """
    generates nested horn clauses of size n
    """
    if n == 0:
        yield 'o', ()
    else:
        for k in range(0, n):
            for f, l in horn(k):
                for g, r in horn(n - 1 - k):
                    yield g, ((f, l),) + r


# for x in fhFormula(3):   print(x)

# tests

def timer():
    return timeit.default_timer()


def test_select():
    xs = [1, 2]
    for x in select(xs): print(*x)


def hptest():
    a, b, c, d, X, Y = 0, 1, 2, 3, 4, 5
    X = (d, (b, (d, c)), c)
    Y = (d, (b, d), c)
    res = fhprove((Y, X))
    print('RES:', res)


def xptest():
    xCombType = (7, (7, (0, 0, 1), (4, (4, 2, 3), (3, 2), 2), (5, 5, 6)))
    xCombType = (7, (7, (0, 0, 1), (4, (4, 2, 3), (3, 2), 2), (5, 5, 6)))
    print('xCombType', fhprove(xCombType))


def test_fhprovers(n=5):
    proven = 0
    forms = 0
    bad = 0
    t1 = timer()
    for f, h in zip(fhFormula(n), hFormula_(n)):
        forms += 1
        gold = hprove(h)
        ok = fhprove(f)
        proven += ok
        if gold and not ok:
            bad += 1
            print('should not fail:', f, '-----', h)
        elif not gold and ok:
            bad += 1
            print('should not succeeed:', f, '-----', h)
    t2 = timer()
    print('formulas:', forms, 'proven:',
          proven, 'bad:', bad, 'density:', round(proven / forms, 4))
    print('TIME:', round(t2 - t1, 2))


if __name__ == "__main__":
    test_fhprovers(7)
    # hptest()
    # print('\n-------\n')
    # xptest()
