from formulas import (
  iFormula,iCounts,fCounts,ranLBin,binOp,opTree,
  fFormula,expandNeg,genListPartition
)
from cnf import tseitin,to_cnf,fixVars, from_cnf
from remy import ranBin0
from provers import (
   iprove, ljb,fprove,tprove,cprove,ljf,
   isTuple,ishow,fshow,to_triplet,fromList, toList,identity,selectFirst,
   pp,ppp,set_max_time,get_max_time, fp as fp
)
from sat import classical_tautology as classical_tautology,is_taut,is_sat
from syntax import expr as expr, syntest as syntest

xx=expr(0)
yy=expr(1)
zz=expr(2)

import timeit
import trace

# tests    
    
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
  
def fullFormTest1(n) :
  return allFormTest2(tprove,fFormula,expandNeg,n) 
  
# try fprove on all implicational formulas of size n
# fprove covers full untuitionistic propositional logic
# but this shows that it covers the implicational subset
def allFormTest1(n) :
  return allFormTest2(fprove,iFormula,to_triplet,n)  


def allFormTest2(f,generator,transformer,n) :
  yes_py=[]
  provable = 0
  unprovable = 0
  
  for t0 in generator(n) :
    t = transformer(t0)
    if(f(t)) :
      provable+=1
      yes_py.append(provable+unprovable)
    else :
      unprovable+=1
  total=provable+unprovable
  ratio=provable/total
  print(n,'provable',provable,'total',
    total,'unprovable',unprovable,'ratio',ratio)   
    

def proverDiff(n) :
  for t0 in iFormula(n) :
    t = to_triplet(t0)
    f= fprove(t)
    i=iprove(t0)
    if(f and not i) :
     print('should_be_unprovable',t)
    if(i and not f) :
     print('should_be_provable',t) 
    

def fixYes() :
  return list(list2tuple(yes))
  
def list2tuple(xs) :
  if isinstance(xs,list) :
    g=map(list2tuple,xs) 
    return tuple(g)
  else :
    return xs

def testYes() :
  for x in list2tuple(yes) :
    y = expandNeg(x)
    if not fprove(y) :
      #print(x)
      print(y)
      print('')

def load_iltp() :
  f=open('iltp.txt','r')
  for line in f :
    try :
      yield(eval(line))
    except MemoryError as e :
      pass
  f.close()
  
def store_iltp() :
  iltp=[]
  for l in load_iltp() :
      iltp.append(l)
  return iltp
   
# max_time: 30, same at 60
#provable 95 unprovable 50 timed_out 99 wrong 0 RIGHT: 145 total_tried 244
def test_iltp(time) :
  test_iltp_with(fprove,time)

def test_iltp1(time) :
  test_iltp_with(tprove,time)

def test_iltp2(time) :
  test_iltp_with(cprove,time)

  
def test_iltp_with(prover,time) :  
  set_max_time(time)
  ls = store_iltp()
  ts = list2tuple(ls)
  provable=0
  unprovable=0
  wrong=0
  timed_out=0
  print('max_time',get_max_time())
  for t in ts :
    N,TF,FN,G = t
    g = expandNeg(G)
    print(N,FN)
    R=prover(g)
    if R==TF :
      if(R==True) : 
        provable+=1
        print('  ok:',R,'at:',provable)    
      elif(R==False) : 
        unprovable+=1
        print('  ok:',R,'at:',unprovable)     
    elif R=='timeout':
        timed_out+=1
        print('  should_be:',TF,'TIMED OUT!','at:',timed_out)
    else :
      wrong+=1
      print(N,'  WRONG result:',R,'should_be:',TF,'at:',wrong)
      #pp(g)  
  print('max_time:',get_max_time())  
  right=provable+unprovable
  total=right+wrong+timed_out
  print('provable',provable,'unprovable',unprovable,
  'timed_out',timed_out,'wrong',wrong,
  'RIGHT:',right,'total_tried',total)
  
      
  
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
  
def bm() : 
  bmn(8)
  
def bmn(n) :
  for k in range(n) :
    bmf1(allFormTest,k)

def bm1() :
  bmf1(allFormTest1,7)

#8 provable 31839 total 332193 unprovable 300354 ratio 0.0958448853527919
#  time =  13.916768707000003
#9 provable 115623 total 2100961 unprovable 1985338 ratio 0.05503338710237839
#  time =  3692.055582994

def fbmn(n) :
  for k in range(n) :
    bmf1(fullFormTest,k)

def fbmn1(n) :
  for k in range(n) :
    bmf1(fullFormTest1,k)
    
def fbm() :
  fbmn(5)
   
def bugbm() :
  bmf1(buggyTest,6)  
  
def t1() :
  x=('->',('&',0,1),1)
  return fprove(x)
  
def t2() :
  x= ('->', ('v', 0, 1), ('v', 1, 0))
  return fprove(x)

def t3() :
  g=1
  vs=(0, (0, (0, (0, (('->', 1, 1), (0, (0, (('->', 1, 1), (0, (0, (0, (('->', 1, 1), (0, (0, (0, (0, (('->', 1, 1), (0, (0, (0, (0, (('->', 1, 1), (0, (0, (0, None)))))))))))))))))))))))))
  return next(ljf(g,vs),False)
  
def t4() :
  a=expr(0)
  t = a >> (a | ~a)
  print(t, '--->',fp(t))
  
def t5() :
  p=expr(0)
  q=expr(1)
  r=expr(2)
  s=expr(3)
  t= (((p | q) & r) >> (~s)).run()  
  print(t)
  res=to_cnf(t)
  l=len(res)
  print(res)
  print('len',l)
  
  
def t6() :
  x=('->',('->',0,0),'false')
  y=is_sat(x)
  print('res',y)
  a=to_cnf(x)
  b=from_cnf(a)
  print('form',x)
  print('cnf',a)
  print('from',b)
  print('fshow',fshow(b))
  print('res',fprove(b))
  
  
def t7() :
  p=expr(0)
  q=expr(1)
  t=(~(p>>q) >> (q>>p)).run()
  ir=fprove(t)
  print(ir)
  print(t)
  cr=is_taut(t)
  print('bug',cr)
  
  
  