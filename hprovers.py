def hprove(GBs) :
  G,Bs=GBs
  return any(ljh(G,Bs))

def ljh(G,Vs):
  if G in Vs : yield True
  elif isinstance(G,tuple) :
    H,Bs=G
    yield any(ljh(H,Bs+Vs))
  elif check_head(G,Vs) :
    for X, Vs2 in select(Vs):
      if not isinstance(X,tuple): continue
      (B, As) = X
      for A, Bs in select(As):
        if ljh_imp(A, B, Vs2):
          NewB = trimmed((B, Bs))
          yield any(ljh(G, [NewB] + Vs2))

def ljh_imp(X,B,Vs) :
  if not isinstance(X,tuple) :
    return X in Vs
  else:
    D,Cs=X
    return any(ljh(X,[(B,[D])]+Vs))

def check_head(G,Vs):
  for X in Vs:
    if isinstance(X,tuple):
      if G==X[0] : return True
    elif G==X : return True
  return False

def trimmed(X) :
  H,Bs = X
  if not Bs : return H
  return X

def select(xs):
  for i in range(len(xs)):
    yield xs[i], xs[:i] + xs[i + 1:]


# tests

def test_select() :
  xs=[1,2]
  for x in select(xs) : print(*x)

def test_hprovers():
  print("RUN hornFormTest(7) in tester" )

if __name__=="__main__":
  test_hprovers()
