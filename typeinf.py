
import timeit

#sys.setrecursionlimit(20000) # no need, but just in case

# grammar for lambda terms
# term = int | [term] | (term,term)

# grammar for types: 
# type = int | (type,type)

# generator for simply typed lambda terms 
# of size n and their with their types
# [0,1,2,3,10,34,98,339,1263,4626,18099,73782,306295]
def typed(n) :
  for x  in closed(n) :
    t = typeOf(x)
    if t is not None :
      yield (x,t) 

# generator for closed lambda terms of size n
# [0,1,2,4,13,42,139,506,1915,7558,31092,132170,580466]
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

# computes type of term x    
def typeOf(x) :
  ts=[] # list of vars/types, as ints
  es=[] # for unify

  # makes new var
  def newvar() :
    i = len(es)
    es.append(i)
    return i
  
  # recursive inner function, sees ts, es  
  def tof(x) :
    if isvar(x) : # de Bruijn index
      return ts[x]
    elif len(x) is 1 :
      a = x[0]
      s = newvar()
      ts.append(s)
      t = tof(a)
      if t is None : return None
      else :
        ts.pop()
        return (s,t)
    else : # len is 2  
      a,b = x
      st = tof(a) # (S->T)
      if st is None : return None
      s1 = tof(b) # S1
      if s1 is None : return None
      t = newvar()
      st1 = (s1,t)
      if unifyWithEnv(st,st1,es) : return t
      else : return None
      
  t = tof(x)
  if t is None : return None
  else : return extractType(t,es)     

# unification algorithm, specialized to types        
def  unifyToTerm(x1,x2) :
  vs = makeEnv()
  if unifyWithEnv(x1,x2,vs) :
    t1 = extractType(x1,vs)
    t2 = extractType(x2,vs)
    return (t1,t2)
  else :
    return None

# unifies, returning the envoronment with bindings    
def  unifyToEnv(x1,x2) :
  vs = makeEnv()
  if unifyWithEnv(x1,x2,vs) : return vs
  else : return None

# just for testing - type inferencer creates Env as it goes 
def makeEnv() :
  return list(range(1000))

# builds a term following bindings in environment. es      
def extractType(x,es) : 
  t = deref(x,es)
  if isvar(t) : return t
  else :
    a,b = t
    r = extractType(a,es),extractType(b,es)
    return r

# unifies, by extendng given environment vs      
def unifyWithEnv(x1,x2,vs) :
  t1 = deref(x1,vs)
  t2 = deref(x2,vs)
  b1 = isvar(t1)
  b2 = isvar(t2)
  if b1 and b2 :
    if t1 != t2 : 
      i,j = max(t1,t2),min(t1,t2)
      vs[i]=j
    return True
  elif b1:
    return bind(t1,t2,vs)
  elif b2 :  
    return bind(t2,t1,vs)
  else :
    l1,r1=t1
    l2,r2=t2
    return unifyWithEnv(l1,l2,vs) and unifyWithEnv(r1,r2,vs)

# occurs check, for sound unification  
def occurs(j,t,vs) :
  i = deref(j,vs)
  s = deref(t,vs)
  return occurs1(i,s,vs)
     
def occurs1(i,t,vs) :
  if isvar(t) : return i==t
  else :
    l,r=t
    return occurs(i,l,vs) or occurs(i,r,vs)

# vars are just ints 
def isvar(i) : return isinstance(i,int)
 
# follows variables references to unbound var or nonvar     
def deref(i,vs) : 
  while(isvar(i)) :
    j = vs[i]
    if i is j : break
    i = j
  return i

# binds var to term  
def bind(i,t,vs) :
  if occurs1(i,t,vs) : return False
  else :
    vs[i]=t
    return True

# human readable form of type t
def showType(t) :
  if isvar(t) : return 'T'+str(t)
  else :
    l,r=t
    sl = showType(l)
    sr = showType(r)
    return '('+sl+'->'+sr+')'

# human readable form of term x
def showTerm(x) :
  if isvar(x) : return str(x)
  elif len(x) == 1 :
    a = x[0]
    sa = showTerm(a)
    return 'l('+sa+')' 
  else :
    a,b=x
    sa = showTerm(a)
    sb = showTerm(b)
    return 'a('+ sa+','+sb+')'
    
# -------------- tests ------------------
   


def test1() :
  t1 = (((1, 1), (2, 1)), (1, 2))
  vs1 = [0, 1, 1, 2, 0]
  return [occurs(2,t1,vs1),occurs(3,t1,vs1),occurs(0,t1,vs1),occurs(4,t1,vs1)]
    
def test2() :
  t1 = (((1, 1), (2, 1)), (1, 2))
  t2 = ((5, 6), 7)
  t3 = ((0, 1), 1)
  t4 = (2, 2)

  print(t1,'=',t2)
  print(unifyToEnv(t1,t2))
  print(unifyToTerm(t1,t2))
  print(unifyToEnv(t3,t4))
  print(unifyToTerm(t3,t4))
 
def test3() :
  for t in closed(4) : print(t)

# computes all closed terms of size n       
def cgo(n) :
  count = 0 
  for r in closed(n) : 
    count+=1    
    if(n<6) : # too may otherwise
      print(showTerm(r))
        
  print('closed =',count)   

# computes all simply typed terms of size n
def tgo(n) :
  tcount = 0  
  for r in typed(n) : 
    x,t=r
    tcount +=1
    if(n<6) : # too may otherwise
      print(showTerm(x),showType(t))

  print('typed = ',tcount)

# benchmarks

def bmf(f,n) :
 start_time = timeit.default_timer()
 f(n)
 end_time=timeit.default_timer()
 print('time = ',end_time - start_time)  

# times closed terms of size n
def bmc(n) : return bmf(cgo,n) 

# times simply typed terms of size n
def bmt(n) : return bmf(tgo,n) 

# usage 

''' 
>>> tgo(4)
l(l(l(l(0)))) (T0->(T1->(T2->(T3->T0))))
l(l(l(l(1)))) (T0->(T1->(T2->(T3->T1))))
l(l(l(l(2)))) (T0->(T1->(T2->(T3->T2))))
l(l(l(l(3)))) (T0->(T1->(T2->(T3->T3))))
l(l(a(0,1))) ((T1->T2)->(T1->T2))
l(l(a(1,0))) (T0->((T0->T2)->T2))
l(a(0,l(1))) (((T1->T1)->T2)->T2)
l(a(l(0),0)) (T0->T0)
l(a(l(1),0)) (T0->T0)
a(l(0),l(0)) (T1->T1)
typed =  10

>>> >>> bmc(12)
closed = 580466
time =  0.7327192299999297

>>> bmt(10)
typed =  18099
time =  0.9006380939972587

'''
      
if __name__=="__main__":
  tgo(4)
