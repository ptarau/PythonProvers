import timeit
from formulas import iFormula, ranLBin
from remy import ranBin0

from provers import iprove, fprove, isVar
import gs

def allFormTest(n) :
  provable = 0
  unprovable = 0
  for t in iFormula(n) :
    if(iprove(t)) :
      provable+=1
    else :
      unprovable+=1
  total=provable+unprovable   
  print('total',total,'provable',provable,'unprovable',unprovable)   
    


  
# helpers

def ishow(t) :
  if isVar(t) : return str(t)
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
  
def bm() :
  bmf2(ranTestProver,16,60)
    
def proveGs() :
  succ=0
  fail=0
  for g in gs.gs: 
    if(prove(g)) :
      succ+=1; 
    else :
      fail+=1
  return succ,fail      
  