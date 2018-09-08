from formulas import iFormula,iCounts,fCounts,ranLBin,binOp,opTree,fFormula,expandNeg,genListPartition
from remy import ranBin0
from provers import iprove, ljb, fprove, isTuple
from buggy import gprove, ljg
import gs

import timeit
import trace

def nobug() :
  tr = trace.Trace()
  #it = ('->', ('->', ('->', 0, 0), 0), 0)
  tr.run("fprove( ('->', ('->', ('->', 0, 0), 0), 0) )")
  
def bug() :
  tr = trace.Trace()
  tr.run("t2()")
  
# try iprove on all implicational formulas of size n
def allFormTest(n) :
  return allFormTest2(iprove,iFormula,identity,n)

def fullFormTest(n) :
  return allFormTest2(fprove,fFormula,expandNeg,n)   
  
# try fprove on all implicational formulas of size n
# fprove covers full untuitionistic propositional logic
# but this shows that it covers the implicational subset
def allFormTest1(n) :
  return allFormTest2(fprove,iFormula,to_triplet,n)  

def buggyTest(n) :
  return allFormTest2(gprove,iFormula,identity,n) 
  
def allFormTest2(f,generator,transformer,n) :
  provable = 0
  unprovable = 0
  for t0 in generator(n) :
    t = transformer(t0)
    if(f(t)) :
      provable+=1
    else :
      unprovable+=1
  total=provable+unprovable   
  print('total',total,'provable',provable,'unprovable',unprovable)   
    

def proverDiff(n) :
  for t0 in iFormula(n) :
    t = to_triplet(t0)
    f= fprove(t)
    i=iprove(t0)
    if(f and not i) :
     print('should_be_unprovable',t)
    if(i and not f) :
     print('should_be_provable',t) 
    
  
def identity(x) : return x

def to_triplet(x) :
  if not isTuple(x) : return x
  else :
    a,b=x
    return ('->',to_triplet(a),to_triplet(b))
  
# helpers

def ishow(t) :
  if not isTuple(t) : return str(t)
  else :
    x,y=t
    return '(' + ishow(x) + '->' + ishow(y) + ')'

# tests -----------------------------------

t1 = ishow(((0,1),(0,(0,2))))

def bmf1(f,n) :
 start_time = timeit.default_timer()
 f(n)
 end_time=timeit.default_timer()
 print('time = ',end_time - start_time)  
 
def bmf0(g) :
 start_time = timeit.default_timer()
 res=g
 end_time=timeit.default_timer()
 print('time = ',end_time - start_time)  
 print('res = ',res)

def bmf2(f,x,y) :
 start_time = timeit.default_timer()
 res=f(x,y)
 print(res)
 end_time=timeit.default_timer()
 print('time = ',end_time - start_time)  
 print('res = ',res)
 
 
g=(1,(5,(0,(3,2)))) 

k=(0,(1,0))

s=((0,(1,2)),((0,1),(0,2)))

a=((0,(1,1)),((0,1),(0,2)))

def ranTestProver(K,N) :
  succ=0 
  fail=0
  for t in ranLBin(K,N) :
    print(t)
    res=iprove(t)
    if res : succ+=1
    else : fail+=1
    print(res,'\n')  
  return 'succ', succ,'fail',fail
  
def rbm() :
  bmf2(ranTestProver,16,60)
    
def proveGs() :
  succ=0
  fail=0
  for g in gs.gs: 
    if(iprove(g)) :
      succ+=1; 
    else :
      fail+=1
  return succ,fail     
 
 
def bm() :
  bmf1(allFormTest,6)

def bm1() :
  bmf1(allFormTest1,6)

def fbmn(n) :
  bmf1(fullFormTest,n)

def fbm() :
  fbmn(5)
   
def bugbm() :
  bmf1(buggyTest,6)  
  
def t1() :
  x=('->',('&',0,1),1)
  return fprove(x)
  
  
def t2() :
  x= ('<->', 0, ('v', 0, 1))
  return fprove(x)

  