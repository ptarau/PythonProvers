from syntax import expr as expr
from cnf import to_cnf as to_cnf

import signal

def fp(g) : return fprove(g.run())
  
x=expr(0)
y=expr(1)
z=expr(2)

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
def iprove(G) : return any(ljb(G,None))

def ljb(G,Vs1) :
  if memb(G,Vs1) : yield True
  elif isTuple(G) :
    A,B = G
    yield any(ljb(B,(A,Vs1)))
  else : # atomic G
    for V,Vs2 in selectFirst(Vs1) :
      if isTuple(V) :
        A,B=V
        if ljb_imp(A,B,Vs2) :
          yield any(ljb(G,(B,Vs2)))
 
def ljb_imp(A,B,Vs1) :
  if not isTuple(A) : return memb(A,Vs1)
  else :
    C,D=A
    return any(ljb((C,D),((D,B),Vs1)))

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

#def timed_call(g,t) :
  
# full intuitionistic propositional prover

# defaults when no timeout is needed
max_time = 60
timeout = False

def timeout_handler(no,frame) :
  global timeout
  timeout=True
  
signal.signal(signal.SIGALRM, timeout_handler)

def set_max_time(t) :
  global max_time
  max_time=t

def get_max_time() :
  global max_time
  return max_time
  
def fprove(G) :
  #pp(G)
  global timeout
  timeout = False
  time=get_max_time()
  signal.alarm(time)  
  try :
    return any(ljf(G,None))
  except Exception:
    return 'timeout'
  finally :
    signal.alarm(0)
       
def ljf(G,Vs) :
  #print('ljf'),ppp(G,Vs)
  global timeout
  if timeout : raise(Exception('timeout'))
  elif memb(G,Vs) or memb('false',Vs) : yield True  
  elif isTuple(G) and not G[0] == 'v'  :
    Op,A,B = G    
    if Op == '<->' :
       if any(ljf(B, (A,Vs))) and any(ljf(A, (B,Vs))) : yield True
    elif Op == '->' : 
       if any(ljf(B,(A,Vs))) : yield True         
    elif Op == '&' :
       if any(ljf(A,Vs)) and any(ljf(B,Vs)) : yield True
    else:
       raise ValueError('unexpected operator: '+Op)
  else : # G is atomic, or 'false' or 'v'
    for V,Vs1 in selectFirst(Vs) :
      if isTuple(V) :
        Vs2 = ljf_reduce(V,G,Vs1)
        if Vs2  and any(ljf(G,Vs2)) : yield True
    if isTuple(G) and G[0] == 'v' :
       Op,A,B = G
       if any(ljf(A,Vs)) or any(ljf(B,Vs)) : yield True
         
def ljf_reduce(V,G,Vs) :        
      Op,A,B=V
      if Op=='->' : return ljf_imp(A,B,Vs)
      elif Op == '&' :return A,(B,Vs)
      elif Op == '<->' : return ('->',A,B),(('->',B,A),Vs)
      elif Op == 'v' :
        if any(ljf(G,(A,Vs))) : return B,Vs
          
def ljf_imp(A,B,Vs) :
  if isTuple(A) :
    Op,C,D=A
    if Op == '->' :
      if any(ljf(A,(('->',D,B),Vs))) : return B,Vs
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

'''
def memb(X,Xs) :
 if not Xs :
   return False
 else :
   Y,Ys=Xs
   if X == Y :
     return True
   else :
     return memb(X,Ys)
'''

def memb(X,Xs) :
  Ys=Xs
  while Ys :
    Y,Zs = Ys
    Ys=Zs
    if Y==X : return True
  return False
 
def tprove(x) :
  from sat import classical_tautology as ct
  return ct(x) and fprove(x)

def cprove(x) :
  from sat import classical_tautology as ct
  return ct(x)
  
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
  
