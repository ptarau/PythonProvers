from cantor import *
import math

PREC = 52


def to_int(x, prec=PREC):
    x = round(x * (1 << prec))
    return x


def to_ints(xs):
    return [to_int(x) for x in xs]


def from_int(n, prec=PREC):
    return n / (1 << prec)


def from_ints(ns):
    return [from_int(n) for n in ns]


def from_xseq(xs):
    xs = to_ints(xs)
    x = from_kseq(xs)
    return from_int(x)


def to_xseq(k, x):
    x = to_int(x)
    xs = to_kseq(k, x)
    return from_ints(xs)


def from_xset(xs):
    xs = to_ints(xs)
    x = from_kset(xs)
    return from_int(x)


def to_xset(k, x):
    x = to_int(x)
    xs = to_kset(k, x)
    return from_ints(xs)


def test():
    a = 12345.678
    b = to_xseq(5, a)
    aa = from_xseq(b)

    r = from_int(to_int(3.141223))

    print(r)

    print(a, '\n', b, '\n', aa)
    print()

    xs = math.e, math.pi, 11, 13, math.pi ** math.e, math.e ** math.pi
    ll = len(xs)
    y = from_xset(xs)
    print('xs', xs)
    ys = to_xset(ll, y)
    print('ys', ys)

test()
