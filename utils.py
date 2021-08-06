import json
import os
import pickle
import timeit
from inspect import getframeinfo, stack

import matplotlib.pyplot as plt
import networkx as nx

PARAMS = dict(TRACE=1, CACHE="CACHE/")


def ordset(xs):
    """
    a generator for elements of xs
    with duplicates removed
    """
    return tuple(dict(zip(xs, xs)))


def time(f, *args):
    """
    computes execution time
    """
    t1 = timeit.default_timer()
    res = f(*args)
    t2 = timeit.default_timer()
    print('TIME:', round(t2 - t1, 4), 'for:', f.__name__, *args)
    return res


def pp(xs):
    """
    prints elements of a generator
    one on each line
    """
    for x in xs: print(x)


def count(xs):
    """
    counts elements of a generator
    """
    return sum(1 for _ in xs)


def ppp(*args, **kwargs):
    """
    logging mechanism with possible DEBUG extras
    will tell from which line in which file the printed
    messge orginates from
    """
    if PARAMS["TRACE"] < 1: return
    if PARAMS["TRACE"] >= 1:
        caller = getframeinfo(stack()[1][0])
        print('DEBUG:',
              caller.filename.split('/')[-1],
              '->', caller.lineno, end=': ')
    print(*args, **kwargs)


def to_json(obj, fname, indent=1):
    """
    serializes an object to a json file
    assumes object made of array and dicts
    """
    with open(fname, "w") as outf:
        json.dump(obj, outf, indent=indent)


def from_json(fname):
    """
    deserializes an object from a json file
    """
    with open(fname, "r") as inf:
        obj = json.load(inf)
        return obj


def to_pickle(obj, fname):
    """
    serializes an object to a .pickle file
    """
    with open(fname, "wb") as outf:
        pickle.dump(obj, outf)


def from_pickle(fname):
    """
    deserializes an object from a pickle file
    """
    with open(fname, "rb") as inf:
        return pickle.load(inf)


def exists_file(fname):
    """tests  if it exists as file or dir """
    return os.path.exists(fname)


def ensure_path(fname):
    """
    makes sure path to directory and directory exist
    """
    d, _ = os.path.split(fname)
    os.makedirs(d, exist_ok=True)


def files_of(directory):
    """
    generator yielding files in a directory
    """
    for entry in os.scandir(directory):
        yield entry.path


def draw(g):
    # for x in g.nodes() :
    labels = dict((k, str(v))
                  for k, v in nx.get_node_attributes(g, 'x').items())
    nx.draw(g, labels=labels, with_labels=True, pos=nx.planar_layout(g))

    plt.show()
