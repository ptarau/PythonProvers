import pycosat
from cnf import to_cnf

def picotest() :
  cnf = [[1, -5, 4], [-1, 5, 3, 4], [-3, -4]]
  print(pycosat.solve(cnf))
  for sol in pycosat.itersolve(cnf) :
    print(sol)
    
    
# need to import only this
def classical_tautology(t) :
  return is_taut(t)
  
def is_sat(t) :
  cnf=to_cnf(t)
  #print('cnf',cnf)
  sol=pycosat.solve(cnf)
  #print('sol',sol)
  return 'UNSAT' != pycosat.solve(cnf)
  
def is_taut1(t) :
  nt = ('->',t,'false')
  return not is_sat(nt)
  
  
def is_taut(t) :
  cnf=to_cnf(t)
  #print('cnf',cnf)
  last=cnf[-1]
  #print('last',last)
  last[0] = -last[0] 
  sol=pycosat.solve(cnf)
  #print('sol',sol)
  return 'UNSAT' == pycosat.solve(cnf)
  