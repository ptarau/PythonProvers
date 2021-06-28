from utils import *
from formulas import hFormula,sFormula,simple,lt
from functools import cmp_to_key
from hprovers import *
import networkx as nx

def sFormula_(n) :
  for t in hFormula(n):
    if simple(t) : yield t
    else : yield to_strict(t)

def consts_of(term) :
  def const_of(t):
    if not simple(t):
      for x in t:
        yield from const_of(x)
    else:
      yield t

  return sorted(set(const_of(term)))

def cmp(x,y) :
  if x==y : return 0
  elif lt(x,y) : return -1
  return 1

def term_sort(xs):
  #assert isinstance(xs,list)
  cmp_fun = cmp_to_key(cmp)
  return tuple(sorted(xs,key=cmp_fun ))

def to_strict(x) :
  #print("###",x) # bug - builds deep heads?
  if simple(x) : return x
  h,xs = x
  assert simple(h)
  assert not simple(xs)
  if not xs: return h
  ys=ordset([to_strict(y) for y in xs if h!=y])
  #print('!!!',list(ys))
  if not ys or h in ys: return h
  assert h not in ys
  return h,term_sort(ys)

def listify(t) :
  if simple(t) : return t
  else :
    h,bs=t
    return h,[listify(x) for x in bs]

def uFormula(n) :
  xs=ordset(x for x in sFormula_(n))
  for x in xs:
    yield listify(x)


#----------

def tdepth(t) :
  return max(len(p) for p in path_of(t))

def leaf_count(t) :
  return sum(1 for _ in path_of(t))

def tsize(t) :
  if simple(t) :
    return 1
  else:
    h,bs=t
    return 1+sum(tsize(x) for x in bs)

def edges_of(term) :
  def es(h,bs):
    for b in bs:
      if simple(b):
        yield (h,b)
      else :
        hh, bb = b
        yield h,hh
        yield from es(hh,bb)
  if not simple(term):
    head,body=term
    yield from es(head,body)

def to_nx(t):
  return nx.DiGraph(list(edges_of(t)))

def plot_es(t):
  g=to_nx(t)
  nx.draw(g,with_labels=True,width=2.0)


def test_formulas(n=3) :
  print('hFormula');pp(hFormula(n))
  print(count(hFormula(n)))
  print('---')
  print(count(sFormula_(n)))
  print('sFormula_');pp(sFormula_(n))
  print('---')
  print('sFormula');pp(sFormula(n))
  print(count(sFormula(n)))
  print('\n==========proved hFormula\n')
  for x in hFormula(n):
    if hprove(x):
      print(x)
  print("\n========proved sFormula\n")
  for x in sFormula(n) :
    if hprove(x) :
      print(x)
  print('\n==========proved uFormula\n')
  for x in uFormula(n):
    if simple(x) : continue
    if hprove(x):
      print(x)


if __name__=="__main__":
  pass
  test_formulas(n=4)


