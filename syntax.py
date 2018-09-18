class expr :
  def __init__(self,x):
    self.val = x
  #def __neg__(self.val) : return ('~',self.val)
  def __invert__(self) : return ('~',self.val)
  def __rshift__(self, other) : return expr(('->',self.val,other.val))
  def __eq__(self, other) : return expr(('<->',self.val,other.val))
  def __and__(self, other) : return expr(('&',self.val,other.val))
  def __xor__(self, other) : return expr(('^',self.val,other.val))
  def __or__(self, other) :return expr(('|',self.val,other.val))
  
  def __str__(self) : return str(self.val)
  
  def run(self) :
    return eval(str(self))
    
x=expr(0)
y=expr(1)
z=expr(2)

def go() : return (x&y==y&x).run()
