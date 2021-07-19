class expr :
  def __init__(self,x): self.val = x
  #def __neg__(self) : return expr(('~',self.val))
  def __invert__(self) : return expr(('->',self.val,'false'))
  def __rshift__(self, other) : return expr(('->',self.val,other.val))
  def __eq__(self, other) : return expr(('<->',self.val,other.val))
  def __and__(self, other) : return expr(('&',self.val,other.val))
  def __xor__(self, other) : return expr(('^',self.val,other.val))
  def __or__(self, other) :return expr(('v',self.val,other.val))
  
  def __str__(self) : return str(self.val)
  
  def run(self) :
    return eval(str(self))

def syntest() :
  x = expr(0)
  y = expr(1)
  z = expr(2)

  return ((x&~y== ~y&x)|(z>>z)).run()

if __name__=="__main__":
  print(syntest())
