# binary and binary-unary (Mozkin) tree generators

import random
from ranpart import getBellNumber, getRandomSet, randPart
from remy import ranBin, ranBin0
from provers import isTuple

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

def hFormula(n) :
  """
  nested Horn formulas
  """
  for tree in horn(n) :
    for lpart in genListPartition(n+1) :
      atomIter=iter(lpart)
      yield decorate_horn(tree,atomIter)

def path_of(t) :
  if isinstance(t,tuple)  :
    h,bs=t
    for b in bs:
      for xs in path_of(b):
        yield (h,)+xs
  else:
    yield (t,)

def consts_of(term) :
  def const_of(t):
    if isinstance(t, tuple) or isinstance(t, list):
      for x in t:
        yield from const_of(x)
    else:
      yield t

  return sorted(set(const_of(term)))

def xtt():
  for t in hFormula(5) :
    print('t:',t)
    for p in path_of(t):
       print(p)
    print('\n')

'''
def const_as_bits(c,cs) :
  i=cs.index(c)
  return 1<<i

def bits_to_consts(bs,cs) :
  xs=[]
  for i,c in enumerate(cs):
    if 1&(bs>>i) :
      xs.append(c)
  return xs

def horn_to_bins(t):
  cs = consts_of(t)

  def h2b(z):
    (x,ys) = z
    h = const_as_bits(x, cs) #int
    bs = []
    for y in ys:
      if isinstance(y,tuple):
        b = h2b(y)
      else:
        b=const_as_bits(y,cs)
      bs.append(b)
    return h,bs
  return h2b(t)
'''



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
  if n == 0:
    yield 'o',[]
  else:
    for k in range(0, n):
      for f,l in horn(k):
        for g,r in horn(n - 1 - k):
          yield g, [(f,l)] + r


def decorate_horn(tree,leafIter) :
  x=leafIter.__next__()
  _,bs=tree
  if not bs :
    return x
  else :
    return x,[decorate_horn(b,leafIter) for b in bs]


    
# set partition generator, as list of indices

def genListPartition(n) : 
  xs=list(range(n))
  for pss in partition(xs) :
    yield part2list(n,pss) 
  
   
# set parition as list of lists
          
def partition(xs):
    if len(xs) == 1:
        yield [ xs ]
        return

    first = xs[0]
    for smaller in partition(xs[1:]):
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
      if on(i,pss[j]) :
        res.append(j)
  return res
   
def on(i,js) :
  for j in js :
    if i==j : return True
  return False  

   
# random tree generators          
           
def links2lbin(k,L,xs) :
  if 0 == k % 2 :
    return xs[k // 2]
  else :
    return links2lbin(L[k],L,xs),links2lbin(L[k+1],L,xs)   

# labeled random binary trees  - using Remy;s algorithm
    
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
  print(mes)
  for t in f(n) :
    print(t)
  print("")
  
# tests
 
def go() :  
  showFor('Binary trees',bin,3)
  showFor('Motzkin trees',mot,4)
  showFor('Implicational Formulas',iFormula,3)
  
  print('COUNTS\n')
  countsFor('Binary trees',bin,12)
  countsFor('Motzkin trees',mot,12)
  countsFor('closed lambda terms',closed,12)

  print('Implicational Formulas',iCounts(7))
  
  print("done")

xtt()
