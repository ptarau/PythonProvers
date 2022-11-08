# implements Cantor's N^K->N bijection and ist inverse

from mpmath import *
import math


def comb1(n, k):
    if k < 0 or k > n:
        return 0
    if k == 0 or k == n:
        return 1
    gn = gamma(n + 1)
    gk = math.factorial(k + 1)
    gnk = gamma(n - k + 1)
    g = (gn / gk) / gnk
    return g


def comb2(n, k):
    if k < 0 or k > n:
        return 0
    if k == 0 or k == n:
        return 1
    k = min(k, n - k)  # Take advantage of symmetry
    gn = loggamma(n + 1)
    gk = loggamma(k + 1)
    gnk = loggamma(n - k + 1)
    g = exp(gn - (gk + gnk))

    return g


comb = binomial


# comb=comb2


def n2ns(n):
    if n <= 0: return []
    k, m = kunpair(n - 1)
    return to_kseq(k + 1, m)


def ns2n(ns):
    if ns <= []: return 0
    k = len(ns)
    m = from_kseq(ns)
    return 1 + kpair((k - 1, m))


def from_kseq(ns):
    return from_kset(seq2set(ns))


def to_kseq(k, n):
    return set2seq(to_kset(k, n))


def from_kset(xs):
    return sum(comb(n, k) for (n, k) in zip(xs, range(1, len(xs) + 1)))


def to_kset(k, n):
    return binomial_digits(k, n, [])


def binomial_digits(k, n, ds):
    if k <= 0: return ds
    assert k > 0
    m = upper_binomial(k, n)
    bdigit = comb(m - 1, k)
    return binomial_digits(k - 1, n - bdigit, [m - 1] + ds)


def upper_binomial(k, n):
    def rough_limit(nk, i):
        if comb(i, k) > nk: return i
        return rough_limit(nk, 2 * i)

    def binary_search(fr, to):
        if fr == to: return fr
        mid = (fr + to) / 2
        if comb(mid, k) > n:
            return binary_search(fr, mid)
        return binary_search(mid + 1, to)

    m = rough_limit(n + k, k)
    return binary_search(m / 2, m)


def kpair(xs):
    assert len(xs) == 2
    return from_kseq(xs)


def kunpair(z):
    return to_kseq(2, z)


def seq2set(xs):
    """
    bijection from sequences to sets
    """
    rs = []
    s = -1
    for x in xs:
        sx = x + 1
        s += sx
        rs.append(s)
    return rs


def set2seq(ms):
    """
     bijection from sets to sequences
     """
    rs = []
    s = 0
    for m in ms:
        rs.append(m - s)
        s = m + 1
    return rs


def reshape(n, xs):
    x = from_kseq(xs)
    ys = to_kseq(n, x)
    return ys


def t1(vs=[1, 2, 3, 4]):
    print(vs)
    xs = reshape(3, vs)
    print(xs)
    ys = reshape(4, xs)
    print(ys)


def test_cantor():
    xs = [2, 5, 7, 10, 12, 18, 19]
    x = from_kset(xs)

    ys = set2seq(xs)
    print(ys)
    zs = seq2set(ys)
    print(xs, zs)

    xs_ = to_kset(len(xs), x)
    print(xs, xs_)

    us = [2, 3, 1, 0, 4, 4, 5, 0, 3]
    u = from_kseq(us)
    k = len(us)
    vs = to_kseq(k, u)

    print(us, vs)


def test():
    xs = math.e, math.pi, 11, 13, \
         math.pi ** math.e, math.e ** math.pi
    ll = len(xs)
    y = from_kset(xs)
    print('xs', xs)
    ys = to_kset(ll, y)
    print('ys', ys)


if __name__ == "__main__":
    # test_cantor()
    # t1()
    test()
