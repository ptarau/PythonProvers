from cmath import *

from numpy.fft import *
from numpy.polynomial import polynomial as P

from dcolor import *
from formulas import *
from hprovers import hprove
from utils import *


def tdepth(t):
    return max(len(p) for p in path_of(t))


def leaf_count(t):
    return sum(1 for _ in path_of(t))


def tsize(t):
    if simple(t):
        return 1
    else:
        h, bs = t
        return 1 + sum(tsize(x) for x in bs)


def path_of(term, start=0):
    def step(t, n):
        if isinstance(t, tuple):
            h, bs = t
            for b in bs:
                for xs in step(b, n + 1):
                    yield ((n, h),) + xs
        else:
            yield ((n, t),)

    css = list(step(term, start))
    cs = {c for cs in css for c in cs}
    return sorted(cs)


def term2path(term):
    ps = []

    def walk(t, d, i):
        if not isinstance(t, tuple):
            ps.append((d, i, t))
        else:
            h, bs = t
            ps.append((d, i, h))
            for j, b in enumerate(bs):
                walk(b, d + 1, j)

    # h0 = term[0] if isinstance(term, tuple) else term
    # ps.append((0, 0, h0))
    walk(term, 0, 0)
    return sorted(ps)


def term2list(term):
    ps = [None] * (tsize(term))
    i = -1

    def walk(p, t):
        nonlocal i
        if not isinstance(t, tuple):
            i += 1
            ps[i] = (p, t)
        else:
            h, bs = t
            i += 1
            assert ps[i] is None
            ps[i] = (p, h)
            p = i
            for b in bs:
                walk(p, b)

    walk(None, term)
    return ps


def list2term(ps):
    def build(i):
        h = ps[i][1]
        children = [build(k) for k, (j, c) in enumerate(ps) if j == i]
        if not children: return h
        return h, children

    return build(0)


def term2nx(t):
    is_tautology = int(hprove(t))
    ps = term2list(t)
    g = nx.DiGraph()
    d = []
    for i, (p, c) in enumerate(ps):
        d.append((i, {'x': c}))
        if p is None:
            continue
        g.add_edge(i, p)

    nx.set_node_attributes(g, dict(d))
    g.y = is_tautology
    return g


def store_dataset(generator=hFormula, m=5):
    gs = []
    for n in range(1, m + 1):
        for t in generator(n):
            g = term2nx(t)
            gs.append(g)
    fname = "CACHE/nhorn_" + generator.__name__ + "_" + str(m) + ".pickle"
    to_pickle(gs, fname)


def load_dataset(generator=hFormula,m=5):
    fname = "CACHE/nhorn_" + generator.__name__ + "_" + str(m) + ".pickle"
    ts = from_pickle(fname)
    return ts


def tl_test(size=10):
    t = ranHorn(size)
    print('TERM:\n', t)
    t = to_strict(t)
    print('STRICT\n', t)
    ps = term2list(t)
    print(ps)
    print('----')
    tt = list2term(ps)
    assert t == tt
    print(tt)
    g = term2nx(t)
    if hprove(t):
        print('TAUTOLOGY!')
    draw(g)


def d_test(m=7):
    gen=sFormula
    store_dataset(generator=gen, m=m)
    gs = load_dataset(generator=gen,m=m)
    tauts = sum(g.y for g in gs)
    forms = len(gs)
    print('STORED NXs:', tauts, '/', forms, 'ratio:', tauts / forms)


def df_code(term):
    """
    assumes terms canonically sorted
    for code to be the same for equivlent formulas
    """
    cs = []

    def visit(t):
        if simple(t):
            cs.append(t + 2)
        else:
            h, bs = t
            cs.append(h + 2)
            cs.append(1)
            for b in bs:
                visit(b)
            cs.append(0)

    visit(term)
    return cs


def path2cs(xs):
    cs = []
    for n, x in xs:
        c = rect((1 + n), (1 + x))
        cs.append(c)
    return cs


def cs2path(cs):
    xs = []
    for c in cs:
        # c=rect(1/(1+n),(1+x))
        pf = polar(c)
        a = pf[0]
        n = a - 1
        x = pf[1] - 1
        xs.append((n, x))
    xs = sorted(xs)  # ,key=lambda v:v[0])
    return xs


def identity(x):
    return x


def cs2poly(cs):
    return P.polyfromroots(cs)


def poly2cs(ps):
    return P.polyroots(ps)


def cs2fft(cs):
    return fft(cs)


def fft2cs(cs):
    return ifft(cs)


def css2fft(css):
    return fft(css)


def funchain(fs, x):
    r = x
    for f in fs:
        r = f(r)
    return r


def to_poly(cs):
    def f(z):
        r = 1
        for c in cs:
            r *= (z - c)
        return r

    return f


def plot_ps(ps):
    x, y = zip(*ps)
    plt.scatter(x, y)
    plt.show()


def plot_cs(cs):
    dc = DColor(xmin=-10, xmax=10, ymin=-10, ymax=10, samples=1000)
    f = to_poly(cs)
    dc.plot(lambda z: f(z))


def poly_code(t):
    fs = [path2cs, cs2poly]
    p = path_of(t)
    return funchain(fs, p)


def fft_code(t):
    fs = [path2cs, cs2fft]
    p = path_of(t)
    return funchain(fs, p)


# tests
def pic_test(size=20):
    t = ranHorn(size)
    print('TERM:', t)
    p = path_of(t)
    print('PATH:', p)
    # p=[2,4]
    cs = path2cs(p)
    # cs=cs2poly(cs)
    cs = fft(cs)
    plot_cs(cs)
    print("\nTPATH:")
    ps = term2path(t)
    for p in ps:
        print(p)


def test_encoders(n=2):
    for t in hFormula(n):
        print('\nFORMULA', t)

        p = path_of(t)
        print('PATH, ORIG:', p)
        cs = path2cs(p)
        p_ = cs2path(cs)
        print('PATH, AGAIN:', p_)
        print('')
        ds = df_code(t)
        print("DEPTH FIRST CODE:", ds)
        cs = sorted(cs, key=lambda x: x.real)
        print('COMPLEX VECT', p, len(cs) * 2, cs)
        ps = cs2poly(cs)
        print('POLY', p, len(ps) * 2, ps)
        cs_ = poly2cs(ps)
        print('COMP. VECT. AGAIN:', sorted(cs_, key=lambda x: x.real))
        print('')
        fs = cs2fft(cs)
        print('FFT', p, len(fs) * 2, fs)
        cs__ = fft2cs(fs)
        print('BACK FROM FFT', p, len(fs) * 2, cs__)
        print('----------')

        print("\nPOLY CODES:")
        for res in poly_code(t):
            print(res)

        print("\nFFT CODES:")
        for res in fft_code(t):
            print(res)

        print('=================\n')
        print('TERM:', t)
        ps = term2path(t)
        print('TPATH:')
        for x in ps:
            print(x)
        print('===================')


if __name__ == "__main__":
    pass
    # test_encoders()
    # pic_test()
    # tl_test()
    d_test()
