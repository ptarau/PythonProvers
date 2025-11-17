# implements Cantor's N^K->N bijection and ist inverse

from math import comb


def n2ns(n):
    if n == 0:
        return []
    k, m = unpair(n - 1)
    return to_kseq(k + 1, m)


def ns2n(ns):
    if ns == []:
        return 0
    k = len(ns)
    m = from_kseq(ns)
    return 1 + pair((k - 1, m))


def from_kseq(ns):
    return from_kset(seq2set(ns))


def to_kseq(k, n):
    return set2seq(to_kset(k, n))


def from_kset(xs):
    return sum(comb(n, k) for (n, k) in zip(xs, range(1, len(xs) + 1)))


def from_kset_(xs):  # just to visualize ...
    s = 0
    for n, k in zip(xs, range(1, len(xs) + 1)):
        c = comb(n, k)
        print(n, k, "==>", c)
        s += c
    return s


def to_kset(k, n):
    return binomial_digits(k, n, [])


def binomial_digits(k, n, ds):
    if k == 0:
        return ds
    assert k > 0
    m = upper_binomial(k, n)
    bdigit = comb(m - 1, k)
    return binomial_digits(k - 1, n - bdigit, [m - 1] + ds)


def upper_binomial(k, n):

    def rough_limit(nk, i):
        if comb(i, k) > nk:
            return i
        return rough_limit(nk, 2 * i)

    def binary_search(fr, to):
        if fr == to:
            return fr
        mid = (fr + to) // 2
        if comb(mid, k) > n:
            return binary_search(fr, mid)
        return binary_search(mid + 1, to)

    m = rough_limit(n + k, k)
    return binary_search(m // 2, m)


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


def pair(xy):
    x, y = xy
    return 2**x * (2 * y + 1) - 1


def unpair(z):
    k = 0
    z += 1
    while z % 2 == 0:
        z = z // 2
        k += 1
    return k, (z - 1) // 2


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


if __name__ == "__main__":
    test_cantor()
