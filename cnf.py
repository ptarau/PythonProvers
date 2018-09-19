def to_cnf(f) :
  t,d = fixVars(f)  
  #print('fixed',t)
  if not isinstance(t,tuple): return [[t]]
  
  l = len(d)
  v,Eqs = tseitin(t,l+1)
  
  def step() :
     for eq in Eqs :
       xs = small_to_cnf(eq)
       for x in xs :
         #print('eq',x)
         yield list(x)
         
  cnf = list(step())  
  cnf.append([v])
  return cnf  
         
def fixVars(t) :
  d={}
  k=0
  def fv(u) :
    nonlocal k
    if isinstance(u,tuple) :
      op,x,y=u
      return (op,fv(x),fv(y))
    else :
      if u in d :
        return d[u]
      else :
        k+=1
        d[u]=k
        return k
  return (fv(t),d) 
          
def tseitin(t,l) :
  eqs=[]
  v=l
  def ts(t) :
    nonlocal v 
    if isinstance(t,tuple) :
      #print('enter_ts',t)
      op,x,y=t
      a=ts(x)
      b=ts(y)
     
      if isinstance(a,tuple) :
        i=v
        v+=1
        eqs.append((i,a))
      else :
        i=a
     
      if isinstance(b,tuple) :
        j=v
        v+=1
        eqs.append((j,b))
      else :
        j=b   
  
      return ((op,i,j)) 
    else :
      return t
  r=ts(t)
  #print('exit__ts',r)
  #v+=1
  eqs.append((v,r)) 
  return (v,eqs)    
  
def small_to_cnf(Ct) :
  C,t=Ct
  #print('Ct',Ct)
  op,A,B=t
  if op == '&' :
    r=[(-A,-B,C),(A,-C),(B,-C)]
  elif op=='v' :
    r=[(A,B,-C),(-A,C),(-B,C)]
  elif op=='<->' :
    r=[(-A,-B,C),(A,B,C),(A,-B,-C),(-A,B,-C)]
  elif op=='^' :
    r=[(-A,-B,-C),(A,B,-C),(A,-B,C),(-A,B,C)]
  elif op=='->' :
    if B=='false' :
      r= [(-A,-C),(A,C)]
    else :
      r = [(-A,B,-C),(A,C),(-B,C)]
  else :
    raise Exception(op + " is unknown")
  return r

# helper, for debug
  
def from_cnf(f) :
  def to_neg(t) :
    if t<0 :
      return ('->',-t,'false')
    else :
      return t
  def to_disj(t) :
    l=len(t)
    if l== 1:
      return to_neg(t[0])
    elif l==2 :
      return ('v',to_neg(t[0]),to_neg(t[1]))
    else :
      x,y,z=t
      a=to_neg(x)
      b=to_neg(y)
      c=to_neg(z)
      return ('v',('v',a,b),c)
  def to_conj(x) :
   if len(x)==1 : 
     return x[0]
   else :
     return ('&',x[0],to_conj(x[1:]))
   
  ds = [to_disj(d) for d in f] 
  return to_conj(ds)