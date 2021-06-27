from utils import *
from formulas import hFormula,sFormula,simple,lt
from functools import cmp_to_key
from cmath import *
from numpy.polynomial import polynomial as P
from numpy.fft import *
from hprovers import *
from dcolor import *
import matplotlib.pyplot as plt
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

def path_of(term,start=0) :
  def step(t,n) :
    if isinstance(t, tuple):
      h, bs = t
      for b in bs:
        for xs in step(b,n+1):
          yield ((n,h),) + xs
    else:
      yield ((n,t),)
  css=list(step(term,start))
  cs = {c for cs in css for c in cs}
  return sorted(cs)

def path2cs(xs):
  cs=[]
  for n,x in xs :
     c=rect((1+n),(1+x))
     cs.append(c)
  return cs

def cs2path(cs):
  xs=[]
  for c in cs :
     #c=rect(1/(1+n),(1+x))
     pf=polar(c)
     a=pf[0]
     n=a-1
     x=pf[1]-1
     xs.append((n,x))
  xs=sorted(xs)#,key=lambda v:v[0])
  return xs

def identity(x) :
  return x

def cs2poly(cs):
  return P.polyfromroots(cs)

def poly2cs(ps) :
  return P.polyroots(ps)

def cs2fft(cs):
  return fft(cs)

def fft2cs(cs):
  return ifft(cs)

def css2fft(css):
  return fft(css)


def funchain(fs,x):
  r=x
  for f in fs:
    r=f(r)
  return r

def to_poly(cs) :
  def f(z) :
    r=1
    for c in cs:
      r*=(z-c)
    return r
  return f

def plot_ps(ps) :
  x,y=zip(*ps)
  plt.scatter(x,y)
  plt.show()

def plot_cs(cs) :
  dc = DColor(xmin=-10, xmax=10, ymin=-10, ymax=10, samples=1000)
  f=to_poly(cs)
  dc.plot(lambda z : f(z))

def pic_test() :
  #t=(0, [(0, [(1, [0, 2, (1, [2])])])])
  t=(0, [3, (0, [(3, [(3, [(1, [2])])])])])
  t=(1, [2, (1, [(2, [(1, [(0, [1])])])])])
  #t=(3, [3, 3, (0, [1]), (1, [2, 3, 3])])
  p=path_of(t)
  print('PATH:',p)
  #p=[2,4]
  cs=path2cs(p)
  #cs=cs2poly(cs)
  cs = fft(cs)
  plot_cs(cs)

def poly_code(t):
  fs=[path2cs,cs2poly]
  p=path_of(t)
  return funchain(fs,p)

def fft_code(t):
  fs=[path2cs,cs2fft]
  p=path_of(t)
  return funchain(fs,p)


def test_experiments(n=2) :
  for t in hFormula(n):
    print('\nFORMULA',t)

    p=path_of(t)
    print('PATH, ORIG:', p)
    cs = path2cs(p)
    p_ = cs2path(cs)
    print('PATH, AGAIN:', p_)
    print('')

    cs = sorted(cs, key=lambda x: x.real)
    print('COMPLEX VECT', p, len(cs) * 2, cs)
    ps = cs2poly(cs)
    print('POLY', p, len(ps) * 2, ps)
    cs_ = poly2cs(ps)
    print('COMP. VECT. AGAIN:',sorted(cs_,key=lambda x:x.real))
    print('')
    fs = cs2fft(cs)
    print('FFT', p, len(fs) * 2, fs)
    cs__ = fft2cs(fs)
    print('BACK FROM FFT', p, len(fs) * 2, cs__)
    print('----------')

    print("\nPOLY CODES:")
    for res in poly_code(t) :
      print(res)

    print("\nFFT CODES:")
    for res in fft_code(t):
      print(res)

    print('=================\n')
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
  test_experiments()
  #test_formulas(n=4)
  #pic_test()

