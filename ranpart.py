from random import random, randint
from math import factorial, e

unm = lambda n, m, b: ((m**n) / (factorial(m) * b)) / e


def genBellNumbers(n):
    B = [0] * (n + 1)  # Bell Numbers
    # Stirling numbers of the second kind
    S = [[0] * (n + 1) for i in range(n + 1)]
    S[0][1] = 1
    B[0] = 1
    for i in range(1, n + 1):
        for j in range(1, i + 1):
            S[i][j] = S[i - 1][j] * j + S[i - 1][j - 1]
            B[i] += S[i][j]
        S[i - 1] = []  # clean Stirling numbers (ram management)
    return B


def getBellNumber(n):
    B = genBellNumbers(n)
    return B[n]
    
# finds out how many urns fit in the given probability
def getM1(p, n, b) :
    m = 0
    while(p > 0) :
        m += 1
        p -= unm(n, m, b)   
    return m
    
def getM(n, b) :
    p = random()
    return getM1(p,n,b)

# 1 - choose M from unm (getM)
# 2 - Drop n labelled balls uniformly into M boxes
# 3 - Form a set partition λ of [n] with i and j in the same block if and
# only if balls i and j are in the same box

def fillUrnes(n,bell) :
   u=getM(n,bell)
   urnes=[None]*u
   for i in range(n) :
     k = randint(0, u - 1)
     if urnes[k] is None : urnes[k]=[]
     urnes[k].append(i)
   g = [u for u in urnes if u is not None]  
   return sorted(list(g))  


def fillRanSet(N,bell) :
  uss = fillUrnes(N,bell)
  bs=[None]*N
  k = 0
  for us in uss :
    for i in us :
      bs[i]=k
    k+=1
  return bs,uss 
   
def getRandomSet(n, bell):
    m = getM(n, bell)
    ps=[None] * n
    norm = [None] * m
    c = 0
    for i in range(n):
        k = randint(0, m - 1)
        c = normalize(norm,k,c)
        ps[i] = norm[k]
    return ps

def normalize(norm,k,c) :
  if norm[k] is None :
    norm[k] = c
    c += 1
  return c
  
def randPart(n,bell) :
  bs = getRandomSet(n,bell)
  m = max(bs)
  d = [None] * (m+1)
  for i in range(n) :
    p=bs[i]
    if d[p] is None :
      d[p] = []
    d[p].append(i)
  return d
    
