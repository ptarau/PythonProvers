# binary and binary-unary (Mozkin) tree generators

import random
from ranpart import getBellNumber, getRandomSet, randPart
from remy import ranBin, ranBin0
from provers import isTuple
from utils import *

# ---- all-terms of given size generators

# implicational and nested Horn formulas of size n
# total number: catalan(n)*bell(n+1)
# superexponential growth - see https://oeis.org/A289679

def iFormula(n) :
  """
  nested implicational formulas
  """
  for tree in bin(n) :
    for lpart in genListPartition(n+1) :
      leafIter=iter(lpart)
      yield decorate(tree,leafIter)

def decorate_horn(tree,leafIter) :
  x=leafIter.__next__()
  _,bs=tree
  if not bs :
    return x
  else :
    return x,[decorate_horn(b,leafIter) for b in bs]

def hFormula(n) :
  """
  nested Horn formulas
  """
  for tree in horn(n) :
    for lpart in genListPartition(n+1) :
      atomIter=iter(lpart)
      yield decorate_horn(tree,atomIter)

def sFormula(n) :
  """
  nested Strict Horn formulas
  """
  for lpart in genListPartition(n+1) :
    for x in strict_horn(n,lpart):
      yield x

def fFormula(n) :
  """
  full IPC formulas
  """
  for tree in opTree(n) :
    m=leafCount(tree)
    for lpart in genListPartition(m) :
      leafIter=iter(lpart)
      yield decorateFull(tree,leafIter)

def leafCount(t) :
  k = len(t)
  if not k : 
    return 1
  elif k == 2 :
    op,tt = t
    return leafCount(tt)
  else :
    op,l,r = t
    return leafCount(l)+leafCount(r)
    
      
# >>> iCounts(7)
#[1, 2, 10, 75, 728, 8526, 115764]
def iCounts(n) :
   return list(countFor(iFormula,n))


def hCounts(n):
  return list(countFor(hFormula, n))

def sCounts(n):
  return list(countFor(sFormula, n))

def fCounts(n) :
  return list(countFor(fFormula,n))
  
# binary tree of size n

def bin(n) :
  if not n : 
    yield ()
  else :
    for k in range(0,n) :    
      for l in bin(k) :
        for r in bin(n-1-k) :        
          yield (l,r)


def decorate(tree,leafIter) :
  if not tree :
    return leafIter.__next__()
  else :
    l,r=tree
    return decorate(l,leafIter),decorate(r,leafIter)


# rose tree (multi-way tree) of size n
def rose(n):
  if n == 0:
    yield []
  else:
    for k in range(0, n):
      for l in rose(k):
        for r in rose(n - 1 - k):
          yield [l] + r

def horn(n):
  """
  generates nested horn clauses of size n
  """
  if n == 0:
    yield 'o',[]
  else:
    for k in range(0, n):
      for f,l in horn(k):
        for g,r in horn(n - 1 - k):
          yield g, [(f,l)] + r

def strict_horn(m,vs):
  """
  generates nested horn clauses of size n
  such that trivially provable formulas are
  removed
  """
  def sh(n,i) :
    if n == 0:
      yield (vs[i],[]),i
    else:
      for k in range(0, n):
        for (f,l),i1 in sh(k,i):
          for (g,r),i2 in sh(n-1-k,i1+1):
            xs=[(f, l)] +r
            if  (g,[]) not in xs and lt_sorted(xs):
              assert simple(g) and simple(f)
              assert simple(g)
              yield (g,xs),i2

  def trim(x) :
    g,xs=x
    if not xs: return g
    return g,list(map(trim,xs))

  for x,_ in sh(m,0) :
    yield trim(x)


def simple(x) :
  return not isinstance(x,list) and not isinstance(x,tuple)

def lt(x,y) :
  if x==y : return False
  a=not simple(x)
  b=not simple(y)
  if not a and b : return True
  if a and not b : return False
  if not a and not b :
    return x<y

  # both lists or tuples
  l,r=len(x),len(y)
  if l<r : return True
  elif l>r : return False

  # same length
  if not x and not y: return True
  for u,v in zip(x,y) :
    if u==v : continue
    return lt(u,v)
  return False

def leq(x,y) :
  return not lt(y,x)

def lt_sorted(xs) :
  for i,y in enumerate(xs):
    if i==0:continue
    x=xs[i-1]
    #assert not(lt(x, y) and lt(y, x))
    #assert not (lt(x, y) and x==y)
    #assert lt(x,y) or lt(y,x) or x==y
    if not lt(x,y) : return False
  return True

    
# set partition generator, as list of indices

def genListPartition(n) : 
  xs=list(range(n))
  for pss in partition(xs) :
    yield part2list(n,pss) 
  
   
# set parition as list of lists


from more_itertools import set_partitions as partition

def partition1(xs):
    if len(xs) == 1:
        yield [ xs ]
        return

    first = xs[0]
    for smaller in partition1(xs[1:]):
        # insert `first` in each of the subpartition's subsets
        for n, subset in enumerate(smaller):
            yield smaller[:n] + [[ first ] + subset]  + smaller[n+1:]
        # put `first` in its own subset 
        yield [ [ first ] ] + smaller
        
# from partition as list of list, to list of indices
def part2list(N,pss) :
  res=[]
  l=len(pss)
  for i in range(N) :
    for j in range(l) :
      if i in pss[j] :
        res.append(j)
  return res
   
# random tree generators          
           
def links2lbin(k,L,xs) :
  if 0 == k % 2 :
    return xs[k // 2]
  else :
    return links2lbin(L[k],L,xs),links2lbin(L[k+1],L,xs)   

# labeled random binary trees  - using Remy's algorithm
    
def ranLBin1(N) :
  L = ranBin0(N)
  b = getBellNumber(N+1)
  bs = getRandomSet(N+1, b)
  return links2lbin(L[0],L,bs)  

  
# labeled random binary trees  
    
def ranLBin(K,N) :
  b = getBellNumber(N+1) 
  bss=[]
  for _ in range(K) :
    bs = getRandomSet(N+1, b)
    bss.append(bs)
  Ls = []  
  for _ in range(K) :
    L = ranBin0(N)
    Ls.append(L) 
  for L in Ls :
    for bs in bss :
       yield links2lbin(L[0],L,bs)
       
def toHorn(t):
  h=t
  bs = []
  while isinstance(t,tuple) :
    a,h=t
    bs.append(toHorn(a))
    t=h
  if bs : return h,bs
  return h

def ranHorns(size,howMany=None) :
  if howMany is None: howMany=size*size
  for b in ranLBin(howMany,size):
    yield toHorn(b)

def mixHorns(size) :
  yield from hFormula(size//3)
  yield from ranHorns(size)

# Motzkin trees of size n
def mot (n) :
  if n==0 : 
    yield ()
  else :
    for m in mot(n-1) :
      yield [m]
    for k in range(0,n-1) :    
      for l in mot(k) :
        for r in mot(n-2-k) :        
          yield (l,r)

# operator tree

def binOp() : 
  return iter( ('->','<->','&','v') )
  

def opTree (n) :
  if n==0 : 
    yield ()
  else :
    for m in opTree(n-1) :
      yield ('~',m)
    for k in range(0,n) :    
      for l in opTree(k) :
        for r in opTree(n-1-k) : 
          for op in binOp() :      
            yield (op,l,r)
          
          
def decorateFull(tree,leafIter) :
  if not tree : 
    return leafIter.__next__()
  else :
    if len(tree) == 2 :
      op,t=tree
      return (op,decorateFull(t,leafIter))
    else :  
      op,l,r=tree
      return (op,decorateFull(l,leafIter),decorateFull(r,leafIter))
    
def expandNeg(t) :
  if not isTuple(t) : return t
  elif len(t) == 2 :
    op,tt = t
    # assert op == '~'
    et = expandNeg(tt)
    return ('->',et,'false')
  else :
    op,l,r=t
    return (op,expandNeg(l),expandNeg(r))
    
# closed lambda terms
def closed(n) :
  return clam(n,0)
  
def clam (n,c) :
  if n==0 : 
    for v in range(c) :
      yield v
  else :
    for m in clam(n-1,c+1) :
      yield [m]
    for k in range(0,n-1) :    
      for l in clam(k,c) :
        for r in clam(n-2-k,c) :        
          yield (l,r)

# helpers

def countFor(f,n) :
  for i in range(n) :
    count = 0
    for t in f(i) : 
      count+=1
    yield count

def countsFor(mes,f,n) :
  print(mes)
  print([c for c in countFor(f,n)])
  print("")

def showFor(mes,f,n) :
  print(mes,'of size',n)
  for t in f(n) :
    print(t)
  print("")
  
# tests
 
def go() :  
  showFor('Binary trees',bin,3)
  showFor('Motzkin trees',mot,4)
  showFor('Implicational Formulas',iFormula,3)
  showFor('Set Partitions',genListPartition,4)
  showFor('Nested Horn Formulas', hFormula, 3)
  showFor('Nested Strict Formulas', sFormula, 3)
  showFor('Full IPC Formulas', fFormula, 2)
  
  print('COUNTS\n')
  countsFor('Binary trees',bin,12)
  countsFor('Motzkin trees',mot,12)
  countsFor('closed lambda terms',closed,12)

  countsFor('Set Partitions',genListPartition,3)

  print('Implicational Formulas',iCounts(7))
  print('Nested Horn Formulas', hCounts(7))
  print('Strict Nested Horn Formulas', sCounts(7))
  print('Full IPC Formulas', fCounts(5))
  
  print("done")

def xtt():
  pass
  showFor('Nested Strict Formulas', sFormula, 2)
  print('Strict Nested Horn Formulas', sCounts(7))

"""
def const_as_bits(c,cs) :
  i=cs.index(c)
  return 1<<i

def bits_to_consts(bs,cs) :
  xs=[]
  for i,c in enumerate(cs):
    if 1&(bs>>i) :
      xs.append(c)
  return xs
"""

if __name__=="__main__":
  xtt()
