from kpartitions import kpartition
from formulas import part2list, leafCount,decorateFull
from sat import classical_tautology, to_cnf

# ( ('->','<->','&','v') )
 
def libFormula(n,k,neg,lib) : 
  for tree in libTree(n,neg,lib) :
    m=leafCount(tree)
    for lpart in genKPartition(m,k) :
      leafIter=iter(lpart)
      yield decorateFull(tree,leafIter)
        
def genKPartition(n,k) : 
  for pss in kpartition(n,k) :
    yield part2list(n,pss) 
   
def libTree (n,neg,lib) :
  if n==0 : 
    yield ()
  else :
    if neg :
      for m in libTree(n-1,neg,lib) :
        yield ('~',m)
    for k in range(0,n) :    
      for l in libTree(k,neg,lib) :
        for r in libTree(n-1-k,neg,lib) : 
          for op in lib :      
            yield (op,l,r)
            
def distinctLeafCount(t) :
  leaves=set()
  def count(t) :
    if isinstance(t,tuple) :
      for x in t[1:] :
        count(x)
    else :
      leaves.add(t)
  count(t)
  return len(leaves)   

  
def reduceForm(t) :
  if isinstance(t,tuple) and len(t) == 3 :
    op,x,y=t
    a=reduceForm(x)
    b=reduceForm(y)
    if op == '^' :
      return '~',('<->',a,b)
    elif op == '<' :
      return '~',('->',b,a)
    elif op=='<-' :
      return '<-',b,a
    elif op == '>' :
      return '~',('->',a,b)  
    elif op=='nand' :
      return '~',('&',a,b)
    elif op=='nor' :
       return '~',('v',a,b)
    else :
      return op,a,b
  elif isinstance(t,tuple) and len(t) == 2 :
    op,x=t
    assert(op=='~')      
    a=reduceForm(x)
    return op,a
  elif t=='false' :
    return '&',0,('~',0)
  elif t=='true' :
    return '->',0,0
  else :
    return t
  
def syn(form0,neg,lib) :
  print(form0)
  form=reduceForm(form0)
  print(form)
  k=distinctLeafCount(form)
  assert k>0
  m = 2**k+k
  print(k,m)
  for n in range(k,m) :
    for f0 in libFormula(n,k,neg,lib) :
      f=reduceForm(f0)
      eq = '<->',form,f
      #print(eq)
      #print(to_cnf(eq))
      if classical_tautology(eq) :
        return f0
   
def stest() :
  form=('^',0,('&',1,2))  
  lib=['->']
  neg=True
  r=syn(form,neg,lib)
  print(r)
  
def stest1() :
  form=('^',0,('nand',1,2))  
  lib=['->']
  neg=True
  r=syn(form,neg,lib)
  print(r)
  
def stest2() :
  form=('<->',0,('<->',1,2))  
  lib=['->']
  neg=True
  r=syn(form,neg,lib)
  print(r)  
  
