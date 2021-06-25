import timeit

def ordset(xs):
  """
  a generator for elements of xs
  with duplicates removed
  """
  return tuple(dict(zip(xs,xs)))

def time(f,*args) :
  """
  computes execution time
  """
  t1 = timeit.default_timer()
  res=f(*args)
  t2 = timeit.default_timer()
  print('TIME:',round(t2-t1,4),'for:',f.__name__,*args)
  return res

def pp(xs):
  """
  prints elements of a generator
  one on each line
  """
  for x in xs : print(x)

def count(xs) :
  """
  counts elements of a generator
  """
  return sum(1 for _ in xs)
