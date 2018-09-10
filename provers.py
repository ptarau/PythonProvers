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
def iprove(G) : return ljb_holds(G,None)

def ljb_holds(X,Vs) : return next(ljb(X,Vs),False)

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
    return ljb_holds((C,D),Vs2)

# derived from Prolog version   
'''
ljf(A,Vs):-memberchk(A,Vs),!.
ljf(_,Vs):-memberchk(false,Vs),!.
ljf(A <-> B,Vs):-!,ljf((A->B),Vs),ljf((B->A),Vs).
ljf((A->B),Vs):-!,ljf(B,[A|Vs]).
ljf(A & B,Vs):-!,ljf(A,Vs),ljf(B,Vs).
ljf(G,Vs1):- % atomic or disj or false
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
  return ljf_holds(G,None)

def ljf_holds(X,Vs) : return next(ljf(X,Vs),False)
  
def ljf(G,Vs) :
  #print('ljf'),ppp(G,Vs)
 
  if memb(G,Vs) or memb('false',Vs) : yield True  
  elif isTuple(G) and not G[0] == 'v'  :
    Op,A,B = G
    
    if Op == '<->' :
       if ljf_holds(B, (A,Vs)) and ljf_holds(A, (B,Vs)) : yield True
    elif Op == '->' : 
       if ljf_holds(B,(A,Vs)) : yield True         
    elif Op == '&' :
       if ljf_holds(A,Vs) and ljf_holds(B,Vs) : yield True
    else:
       raise ValueError('unexpected operator: '+Op)
  else : # isVar(G) or 'false' or
    for V,Vs1 in selectFirst(Vs) :
      if isTuple(V) :
        Vs2 = ljf_reduce(V,G,Vs1)
        if Vs2  and ljf_holds(G,Vs2) : yield True
    if isTuple(G) and G[0] == 'v' :
       Op,A,B = G
       if ljf_holds(A,Vs) or ljf_holds(B,Vs) : yield True
         
def ljf_reduce(V,G,Vs) :        
      Op,A,B=V
      if Op=='->' : return ljf_imp(A,B,Vs)
      elif Op == '&' :return A,(B,Vs)
      elif Op == '<->' : return ('->',A,B),(('->',B,A),Vs)
      elif Op == 'v' :
        if ljf_holds(G,(A,Vs)) : return B,Vs
          
def ljf_imp(A,B,Vs) :
  if isTuple(A) :
    Op,C,D=A
    if Op == '->' :
      if ljf_holds(A,(('->',D,B),Vs)) : return B,Vs
    elif Op == '&' : return ('->',C,('->',D,B)),Vs   
    elif Op == 'v' :
      cb = ('->',C,B)
      db = ('->',D,B)
      return cb,(db,Vs)
    else :
      # assert(Op == '<->') 
      cd = ('->',C,D)
      dc= ('->',D,C)
      return ('->',cd,('->',dc,B)),Vs
  else :   
    if memb(A,Vs) : return B,Vs
   
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
 
    
# other

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
    
def fromList(Ls) :
  Xs = None
  Rs = Ls.copy()
  while Rs :
    X = Rs.pop()
    Xs = X,Xs
  return Xs
  
def toList(Is) : 
  return list(inImmutable(Is))
  