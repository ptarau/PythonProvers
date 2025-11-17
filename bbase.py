from typing import Tuple, List

N = int


def get_bdigit(b: N, n: N) -> Tuple[N, N]:
    assert b > 1 and n > 0
    q, d = divmod(n, b)
    if d == 0:
        return b - 1, q - 1
    return d - 1, q


def put_bdigit(b: N, d: N, n: N) -> N:
    assert b > 1 and 0 <= d < b and n >= 0
    return 1 + d + b * n


def to_bbase(b: N, n: N) -> List[N]:
    if n == 0:
        return []
    d, m = get_bdigit(b, n)
    return [d] + to_bbase(b, m)


def from_bbase(b: N, ds: List[N]) -> N:
    if not ds:
        return 0
    d, rest = ds[0], ds[1:]
    m = from_bbase(b, rest)
    return put_bdigit(b, d, m)


def _split_with(sep: N, xs: List[N]) -> List[List[N]]:
    try:
        i = xs.index(sep)
    except ValueError:
        return [xs[:]]
    head = xs[:i]
    return [head] + _split_with(sep, xs[i + 1 :])


def _intercalate(sep: List[N], xss: List[List[N]]) -> List[N]:
    if not xss:
        return []
    out: List[N] = xss[0][:]
    for chunk in xss[1:]:
        out += sep
        out += chunk
    return out


def nat2nats(k: N, n: N) -> List[N]:
    """

    stream base = k+1 (digits 0..k, sep=k),
    element base = k   (digits 0..k-1).
    """
    if n == 0:
        return []
    if n == 1:
        return [0]
    n1 = n - 1
    k1 = k + 1
    xs = to_bbase(k1, n1)
    nss = _split_with(k, xs)
    return [from_bbase(k, part) for part in nss]


def nats2nat(k: N, ns: List[N]) -> N:
    """
    Inverse nat2nats
    """
    if not ns:
        return 0
    if len(ns) == 1 and ns[0] == 0:
        return 1
    nss = [to_bbase(k, x) for x in ns]
    xs = _intercalate([k], nss)
    n_prime = from_bbase(k + 1, xs)
    return n_prime + 1


def test_bbase(b=2, n=200):
    ms = set()
    for i in range(n):
        ns = nat2nats(b, i)
        j = nats2nat(b, ns)
        assert i == j, i
        ms.add(i)
        print(i, "<->", ns)
    assert len(ms) == n, ms


class Iso:
    def __init__(self, f, g):
        self.f = f
        self.g = g


def compose(A: Iso, B: Iso):
    def cf(x):
        return B.f(A.f(x))

    def cg(x):
        return A.g(B.g(x))

    return Iso(cf, cg)


if __name__ == "__main__":
    pass
    test_bbase()
