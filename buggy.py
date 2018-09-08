from provers import isTuple, selectFirst, memb


      
# full prover   - TODO
def gprove(G) : return next(ljg(G,None),False)

def ljg(G,Vs1) :
  if memb(G,Vs1) : 
    yield True
  elif isTuple(G) :
    A,B = G
    for R in ljg(B,(A,Vs1))  : yield R         
  else : # isVar(G)
    for V,Vs2 in selectFirst(Vs1) :
      if isTuple(V) :
        A,B=V
        Vs3 = ljg_imp(A,B,Vs2)
        for R in ljg(G,Vs3) : yield R
            
def ljg_imp(A,B,Vs1) :
  if not isTuple(A) :
    if memb(A,Vs1) :
      return (B,Vs1)
  else :
    C,D=A
    Vs2 = ((D,B),Vs1)
    if next(ljg( (C,D),Vs2),False)  :
      return (B,Vs2)       