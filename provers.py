# derived from Prolog version
'''
ljb(A,Vs):-memberchk(A,Vs),!.
ljb((A->B),Vs):-!,ljb(B,[A|Vs]). 
ljb(G,Vs1):-
  select((A->B),Vs1,Vs2),
  ljb_imp(A,B,Vs2),
  !,
  ljb(G,[B|Vs2]).

ljb_imp((C->D),B,Vs):-!,ljb((C->D),[(D->B)|Vs]).
ljb_imp(A,_,Vs):-memberchk(A,Vs).   
'''

# restricted to implicational logic
def iprove(G) : return next(ljb(G,None),False)

def ljb(G,Vs1) :
  if memb(G,Vs1) :
    yield True
  elif not isVar(G) :
    A,B = G
    for R in ljb(B,(A,Vs1))  : yield R 
  else : # isVar(G)
    for V,Vs2 in selectFirst(Vs1) :
      if not isVar(V) :
        A,B=V
        if ljb_imp(A,B,Vs2) :
          Vs3 = (B,Vs2)
          for R in ljb(G,Vs3) : yield R
 
def ljb_imp(A,B,Vs1) :
  if isVar(A) :
    return memb(A,Vs1)
  else :
    C,D=A
    Vs2 = ((D,B),Vs1)
    for R in ljb((C,D),Vs2) : return R

# derived from Prolog version   
'''
ljfa(A,Vs):-memberchk(A,Vs),!.
ljfa(_,Vs):-memberchk(false,Vs),!.
ljfa(A <-> B,Vs):-!,ljfa((A->B),Vs),ljfa((B->A),Vs).
ljfa((A->B),Vs):-!,ljfa(B,[A|Vs]).
ljfa(A & B,Vs):-!,ljfa(A,Vs),ljfa(B,Vs).
ljfa(G,Vs1):- % atomic or disj
  select(Red,Vs1,Vs2),
  ljfa_reduce(Red,G,Vs2,Vs3),
  !,
  ljfa(G,Vs3).
ljfa(A v B, Vs):-(ljfa(A,Vs);ljfa(B,Vs)),!.

ljfa_reduce((A->B),_,Vs1,Vs2):-!,ljfa_imp(A,B,Vs1,Vs2).
ljfa_reduce((A & B),_,Vs,[A,B|Vs]):-!.
ljfa_reduce((A<->B),_,Vs,[(A->B),(B->A)|Vs]):-!.
ljfa_reduce((A v B),G,Vs,[B|Vs]):-ljfa(G,[A|Vs]).
  
ljfa_imp((C-> D),B,Vs,[B|Vs]):-!,ljfa((C->D),[(D->B)|Vs]).
ljfa_imp((C & D),B,Vs,[(C->(D->B))|Vs]):-!.
ljfa_imp((C v D),B,Vs,[(C->B),(D->B)|Vs]):-!.
ljfa_imp((C <-> D),B,Vs,[((C->D)->((D->C)->B))|Vs]):-!.
ljfa_imp(A,B,Vs,[B|Vs]):-memberchk(A,Vs).  
'''

# - unfinished - TODO

def ljf_reduce(V,G,Vs) :        
      if not isVar(V) :
        Op,A,B=V
        if Op=='->' :
          if ljf_imp(A,B,Vs2) :
             Vs3 = (B,Vs2)
             for R in ljf(G,Vs3) : yield R
        #elif  Op == '&' 
          
# full prover   
def fprove(G) : return next(ljb(G,None),False)

def ljf(G,Vs) :
  if memb(G,Vs) : yield True
  elif memb('false',Vs) : yield True  
  elif not isVar(G) :
    Op,A,B = G
    if Op == '<->' :
       for x in ljf(('->',A,B)) :
         if x :
           for y in ljf(('->',B,A)) : 
             if y : yield True
    elif Op == '->' :
       for R in ljf(B,(A,Vs))  : yield R         
    elif Op == '&' :
       for x in ljf(A) :
         if x :
           for y in ljf(B) : 
             if y : yield True
    elif Op == 'v' :
       for x in ljf(A,) :
         yield x
       for y in ljf(B) : 
         yield y
  else : # isVar(G)
    for V,Vs2 in selectFirst(Vs1) :
      for R in ljf_reduce(V,Vs2) :
        yield R
        
def ljf_imp(A,B,Vs1) :
  if isVar(A) :
    yield memb(A,Vs1)
  else :
    C,D=A
    Vs2 = ((D,B),Vs1)
    for R in ljf((C,D),Vs2) : yield R   
    
    
# helpers    
    
def selectFirst(Xs) :
  if Xs :
    X,Ys = Xs
    yield (X,Ys)
    for (Z,Zs) in selectFirst(Ys) :
      yield (Z,(X,Zs))
      
def isVar(i) : return isinstance(i,int)

def memb(X,Xs) :
 if not Xs :
   return False
 else :
   Y,Ys=Xs
   if X == Y :
     return True
   else :
     return memb(X,Ys)
 
   