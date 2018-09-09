#from tester import ishow,fshow

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

# prover restricted to implicational logic
# >>> allFormTest(6)
# total 115764 provable 27406 unprovable 88358
def iprove(G) : return next(ljb(G,None),False)

def ljb(G,Vs1) :
  if memb(G,Vs1) :
    yield True
  elif isTuple(G) :
    A,B = G
    for R in ljb(B,(A,Vs1))  : yield R 
  else : # isVar(G)
    for V,Vs2 in selectFirst(Vs1) :
      if isTuple(V) :
        A,B=V
        if ljb_imp(A,B,Vs2) :
          for R in ljb(G,(B,Vs2)) : yield R
 
def ljb_imp(A,B,Vs1) :
  if not isTuple(A) :
    return memb(A,Vs1)
  else :
    C,D=A
    Vs2 = ((D,B),Vs1)
    return next(ljb((C,D),Vs2),False)

# derived from Prolog version   
'''
ljf(A,Vs):-memberchk(A,Vs),!.
ljf(_,Vs):-memberchk(false,Vs),!.
ljf(A <-> B,Vs):-!,ljf((A->B),Vs),ljf((B->A),Vs).
ljf((A->B),Vs):-!,ljf(B,[A|Vs]).
ljf(A & B,Vs):-!,ljf(A,Vs),ljf(B,Vs).
ljf(G,Vs1):- % atomic or disj
  select(Red,Vs1,Vs2),
  ljf_reduce(Red,G,Vs2,Vs3),
  !,
  ljf(G,Vs3).
ljf(A v B, Vs):-(ljf(A,Vs);ljf(B,Vs)),!.

ljf_reduce((A->B),_,Vs1,Vs2):-!,ljf_imp(A,B,Vs1,Vs2).
ljf_reduce((A & B),_,Vs,[A,B|Vs]):-!. 
ljf_reduce((A<->B),_,Vs,[(A->B),(B->A)|Vs]):-!.
ljf_reduce((A v B),G,Vs,[B|Vs]):-ljf(G,[A|Vs]).
  
ljf_imp((C-> D),B,Vs,[B|Vs]):-!,ljf((C->D),[(D->B)|Vs]).
ljf_imp((C & D),B,Vs,[(C->(D->B))|Vs]):-!. 
ljf_imp((C v D),B,Vs,[(C->B),(D->B)|Vs]):-!.
ljf_imp((C <-> D),B,Vs,[((C->D)->((D->C)->B))|Vs]):-!.
ljf_imp(A,B,Vs,[B|Vs]):-memberchk(A,Vs).  
'''

# full intuitionistic propositional prover
def fprove(G) :
  #pp(G)
  return next(ljf(G,None),False)

def ljf(G,Vs) :
  #print('ljf'),ppp(G,Vs)
 
  if memb(G,Vs) : yield True
  elif memb('false',Vs) : yield True  
  elif isTuple(G) :
    Op,A,B = G
    if Op == '<->' :
       for x in ljf( ('->',A,B), Vs) :
           for y in ljf( ('->',B,A), Vs) : 
              yield True
    elif Op == '->' : 
       for R in ljf(B,(A,Vs))  : 
         yield R         
    elif Op == '&' :
       for x in ljf(A,Vs) :
           for y in ljf(B,Vs) : 
             yield True
    elif Op == 'v' :
       for x in ljf(A,Vs) :
         yield x
       for y in ljf(B,Vs) : 
         yield y
    else:
       raise ValueError('unexpected operator: '+Op)
  #elif G=='false' :
     #raise('false')
     #return False
  else : # isVar(G) or 'false'
    for V,Vs1 in selectFirst(Vs) :
      if isTuple(V) :
        Vs2 = ljf_reduce(V,G,Vs1)
        if Vs2 :
          for R in ljf(G,Vs2) :
             yield R
           
def ljf_reduce(V,G,Vs) :        
        Op,A,B=V
        if Op=='->' : 
          #print('ljf_reduce'),ppp(G,Vs)
          return ljf_imp(A,B,Vs)
        elif  Op == '&' :
          return A,(B,Vs)
        elif Op == '<->' :
          return ('->',A,B),(('->',B,A),Vs)
        elif Op=='v' :
          if next(ljf(G,(A,Vs)),False) :
            return B,Vs
          
def ljf_imp(A,B,Vs1) :
  if not isTuple(A) :
    if memb(A,Vs1) :
      return B,Vs1
  else :
    Op,C,D=A
    if Op == '->' : 
      Vs2 = (('->',D,B),Vs1)
      if next(ljf(('->',C,D),Vs2),False)  :
        return B,Vs2
    elif Op == '&' :     
      return ('->',C,('->',D,B)),Vs1   
    elif Op == 'v' :
      return ('->',('->',C,D),('->',('->',D,C),B)),Vs1
    else :
      # assert(Op == '<->') 
      cd = ('->',C,D)
      dc = ('->',D,C)
      return ('->',cd,('->',dc,B)),Vs1
         
# helpers    
    
def selectFirst(Xs) :
  if Xs :
    X,Ys = Xs
    yield (X,Ys)
    for (Z,Zs) in selectFirst(Ys) :
      yield (Z,(X,Zs))
      
def isTuple(i) : return isinstance(i,tuple)
#def isVar(i) : return  isinstance(i,int)

def memb(X,Xs) :
 if not Xs :
   return False
 else :
   Y,Ys=Xs
   if X == Y :
     return True
   else :
     return memb(X,Ys)
 
    
# helpers

def identity(x) : return x

def to_triplet(x) :
  if not isTuple(x) : return x
  else :
    a,b=x
    return ('->',to_triplet(a),to_triplet(b))
  
def ishow(t) :
  if not isTuple(t) : return str(t)
  else :
    x,y=t
    return '(' + ishow(x) + '->' + ishow(y) + ')'
  
def fshow(t) :
  if not isTuple(t) : return str(t)
  else :
    op,x,y=t
    return '(' + fshow(x) + ' '+ op + ' ' + fshow(y) + ')'
 
def pp(t) :
  print(fshow(t))
  
def ppp(t,vs) :
  print(fshow(t),' :-',end='')
  for x in inImmutable(vs) :
    print('  ',fshow(x),end='')  
  print('\n')
 
def inImmutable(Is) :
  if not Is : return None
  else :
    I,Js = Is
    yield I
    for J in inImmutable(Js) : yield J 
    
    