import networkx as nx

from ml import *


def sFormula_(n):
    for t in hFormula(n):
        if simple(t):
            yield t
        else:
            yield to_strict(t)


def consts_of(term):
    def const_of(t):
        if not simple(t):
            for x in t:
                yield from const_of(x)
        else:
            yield t

    return sorted(set(const_of(term)))


def term_sort(t):
    if not isinstance(t, tuple):
        return t
    h, bs = t
    cs = list(map(term_sort, bs))
    #ds = sorted(cs, key=sort_key)
    ds=qsorted(cs)
    return (h, ds)


def sort_key(t):
    if not isinstance(t, tuple): return t
    return t[0]


def sort_test():
    a=(0,[(1,[3]),(0,[4]),(1,[2])])
    print('\nsort_test')
    print(a)
    b=term_sort(a)
    print(b)





def uFormula(n):
    for x in sFormula_(n):
        yield to_strict(x)


# ----------




def edges_of(term):
    def es(h, bs):
        for b in bs:
            if simple(b):
                yield (h, b)
            else:
                hh, bb = b
                yield h, hh
                yield from es(hh, bb)

    if not simple(term):
        head, body = term
        yield from es(head, body)


def to_nx(t):
    return nx.DiGraph(list(edges_of(t)))


def plot_es(t):
    print(t)
    print(list(edges_of(t)))
    g = to_nx(t)
    print('!!!', g.number_of_edges())
    nx.draw(g, with_labels=True, width=2.0)
    plt.show()


def test_formulas(n=3):
    print('hFormula');
    pp(hFormula(n))
    print(count(hFormula(n)))
    print('---')
    print(count(sFormula_(n)))
    print('sFormula_');
    pp(sFormula_(n))
    print('---')
    print('sFormula');
    pp(sFormula(n))
    print(count(sFormula(n)))
    print('\n==========proved hFormula\n')
    for x in hFormula(n):
        if hprove(x):
            print(x)
    print("\n========proved sFormula\n")
    for x in sFormula(n):
        if hprove(x):
            print(x)
    print('\n==========proved uFormula\n')
    for x in uFormula(n):
        if simple(x): continue
        if hprove(x):
            print(x)
            # plot_es(x)


if __name__ == "__main__":
    pass
    test_formulas(n=3)
    '''
    plot_es((0, [3, (0, [(3, [(0, [(1, [2])])])])]))
    plot_es((2, [(2, [(1, [0, 2, (1, [2])])])]))
    plot_es((0, [3, (0, [(3, [2])]), (1, [2])]))
    plot_es((0, [(5, [(1, [(2, [(3, [(4, [(5, [6])])])])])])]))
    plot_es((0, [(0, [(1, [(1, [(0, [(0, [(0, [1])])])])])])]))
    plot_es((1, [3, (1, [(0, [1, (0, [(1, [2])])])])]))
    '''
    sort_test()
