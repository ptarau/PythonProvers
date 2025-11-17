from typing import Tuple, List

N = int


def put_digit(b, d, n):
    assert b > 1 and 0 <= d < b and n >= 0
    return n * b + d


def get_digit(b, n):
    assert b > 1 and n > 0
    q, d = divmod(n, b)
    return d, q


def to_base(b, n):
    if n == 0:
        return [0]
    ds = []
    while n > 0:
        d, n = get_digit(b, n)
        ds.append(d)
    return ds


def from_base(b, ns):
    n = 0
    for d in reversed(ns):
        n = put_digit(b, d, n)
    return n


def collatz(n):
    print(n)
    while n > 1:
        if n % 2 == 0:
            _d, n = get_digit(2, n)
        else:
            n = put_digit(3, 1, n)
        print(n, end=" ")
    print()
    return n


import math


def toy_primes(N):
    # return list(range(1, N))
    return [int(n * math.log(n)) for n in range(2, N + 1)]


def to_bins(ns):
    bs = []
    m = max(ns)
    for i in range(m + 1):
        if i in ns:
            d = 1
        else:
            d = 0
        bs.append(d)
    return bs


# generalize for b: split in b bins, based on digit 0..b-1
# ns would then be a set partition of N in b bins
# seen as an infinite series of base b digits indicating the bin
# a generalization of the characteristic function to a b-base equivalent
# example of bins: [0..] modulo b
def bunpair(n, ns, b=2):

    hs = []
    ts = []
    i = 0
    assert n >= 0, n
    if n == 0:
        return 0, 0

    while n > 0:
        d, n = get_digit(b, n)
        if i in ns:
            hs.append(d)
        else:
            ts.append(d)
        i += 1
    return from_base(2, hs), from_base(2, ts)


def bpair(ht, ns, b=2):
    bs = to_bins(ns)
    h, t = ht
    hs = to_base(b, h)
    ts = to_base(b, t)
    rs = []
    i = 0
    while hs or ts:
        d = bs[i]
        if d:
            if hs:
                dh, hs = hs[0], hs[1:]
            else:
                dh = 0
            rs.append(dh)
        else:
            if ts:
                dt, ts = ts[0], ts[1:]
            else:
                dt = 0
            rs.append(dt)
        i += 1
    return from_base(b, rs)


def test1(m=20):
    ns = toy_primes(m)
    ps = []
    for n in range(m):
        h, t = bunpair(n, ns)
        # print(n, "-->", (h, t))
        if t == 0:
            print("!!!!!!!!", n, "->", h, t)
        ps.append((h, t))
    assert len(ps) == m
    # return ps


if __name__ == "__main__":
    pass
    collatz(12)
