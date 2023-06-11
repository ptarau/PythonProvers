import networkx as nx
import matplotlib.pyplot as plt
from collections import deque


def qprove(css0):

    props = dict()
    css = []
    for c in css0:
        if isinstance(c, tuple):
            h, bs = c
        else:
            h, bs = c, []
        css.append((h, bs))

    for h, bs in css:
        props[h] = False
        for b in bs: props[b] = False
    for h, bs in css:
        if bs == []:
            props[h] = True

    change = True
    while change:
        change = False
        for i, c in enumerate(css):
            if c is None: continue
            h, bs = c
            if all(props[b] for b in bs):
                if h == 'false':
                    return None

                if not props[h] and all(props[b] for b in bs):
                    props[h] = True
                    change = True
                    css[i] = None

    return [p for p, v in props.items() if v]


def to_horn_graph(css, ics=None):
    g = nx.DiGraph()
    for i, c in enumerate(css):
        if isinstance(c, tuple):
            h, bs = c
            if bs == []:
                g.add_edge(True, b, clause=i)
            else:
                for b in bs:
                    g.add_edge(b, h, clause=i)
            if ics is not None:
                for ic in ics:
                    g.add_edge(ic, False, clause=i)
        else:
            g.add_edge(True, c, clause=i)

    return g


# dict based ord sets

def dpop(d):
    if not d: return None
    it = iter(d)
    return d.pop(next(it))


def dadd(d, x):
    d[x] = True


def ddel(d, x):
    del d[x]


def gprove(g, css, ics=None):
    G = to_horn_graph(css, ics=ics)

    for e in G.edges(): print(e)
    draw(G)

    qs = dict()
    facts = dict()
    for fact in G.successors(True):
        dadd(qs, fact)
        dadd(facts, fact)

    while True:
        print("MODEL", list(facts))
        print("QUEUE", list(qs))
        if g in qs:
            return True

        q = dpop(qs)
        if q is None:
            break
        for x in G[q]:
            if x != q: dadd(qs, x)

        fs = []
        for b in G[q]:
            print('???', b)
            dadd(qs, b)
            hs = G.predecessors(b)
            for h in hs:
                fs.append(h)

        for f in fs:
            if (f, h) in G.edges():
                G.remove_edge(b, h)

    return False


def draw(G, edge_label='clause'):
    # pos = nx.spring_layout(G)
    pos = nx.nx_agraph.graphviz_layout(G)

    plt.figure()
    nx.draw(
        G, pos, edge_color='black', width=1, linewidths=2,
        node_size=500, node_color='grey', alpha=0.9,
        labels={node: node for node in G.nodes()},
        arrows=True,
    )
    edge_labels = [((x, y), G[x][y][edge_label]) for (x, y) in G.edges()]
    nx.draw_networkx_edge_labels(
        G, pos,
        font_color='black',
        edge_labels=dict(edge_labels)
    )
    plt.axis('off')
    plt.show()


def test():
    p1, p2, p3, p4, p5 = "p1,p2,p3,p4,p5".split(",")
    css = [(p5, [p3, p4]), (p2, [p1]), (p1, [p2]), (p4, [p3]), (p3, [])]
    ics = [p1, p2]
    g = to_horn_graph(css, ics=ics)
    print(g.number_of_edges())
    draw(g)

    #css = [2, (2, [0, 1, 2, 3]), (0, [2, 3]), 3, (4, [0, 2, 3]),('false',[0,4])]
    css = [2, (2, [0, 1, 2, 3]), (0, [2, 3]), 3, (4, [0, 2, 3])]
    print(css)
    r = qprove(css)
    print('model:', r)
    g = to_horn_graph(css)
    draw(g)


test()
