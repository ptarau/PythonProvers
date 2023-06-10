import networkx as nx
import matplotlib.pyplot as plt


def to_horn_graph(css,ics=None):
    g=nx.DiGraph()
    for i,(h,bs) in enumerate(css):
        if bs == []:
            g.add_edge(True,b,clause=i)
        else:
            for b in bs:
                g.add_edge(b,h,clause=i)
        if ics is not None:
          for ic in ics:
              g.add_edge(ic,False,clause=i)

    return g


def draw(G,edge_label='clause'):
    #pos = nx.spring_layout(G)
    pos=nx.nx_agraph.graphviz_layout(G)

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
    p1,p2,p3,p4,p5="p1,p2,p3,p4,p5".split(",")
    css=[(p5,[p3,p4]),(p2,[p1]),(p1,[p2]),(p4,[p3]),(p3,[])]
    ics=[p1,p2]
    g=to_horn_graph(css,ics=ics)
    print(g.number_of_edges())
    draw(g)

test()
