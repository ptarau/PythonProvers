from pyeda.inter import *

# need to import only this
def classical_tautology(t) :
  x = tuple2expr(t)
  return is_taut(x)
  
def is_sat(t) :
  #cnf = t.tseitin()
  cnf=t.to_cnf()
  return not None == cnf.satisfy_one()
  
def is_taut(t) :
  return not(is_sat(Not(t)))
  
def tuple2expr(t) :
  return t2e(t,True) 
  
def t2e(t,simp) :  
  if isinstance(t,tuple) :
    l=len(t)
    if l==2 : 
      op,x=t
      assert(op=='~')
      a=t2e(x,simp)
      return Not(a,simplify=simp)
    elif l==3 :
      op,x,y=t 
      a=t2e(x,simp)
      b=t2e(y,simp)
      if(op=='->') : 
        return Implies(a,b,simplify=simp)
      elif op=='<->' : 
        return Equal(a,b,simplify=simp)
      elif(op=='&') :
        return And(a,b,simplify=simp)
      elif(op=='v') :
        return Or(a,b,simplify=simp)
      else :
        raise "bad op="+op
  elif t=='false' :
    return expr(False)
  else :
    if isinstance(t,int) :
      return exprvar('X',t)
    else :
      return exprvar(t)
      