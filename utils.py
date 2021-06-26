import os
import json
import timeit
from inspect import getframeinfo, stack

PARAMS=dict(TRACE=1)

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

def ppp(*args,**kwargs) :
  """
  logging mechanism with possible DEBUG extras
  will tell from which line in which file the printed
  messge orginates from
  """
  if PARAMS["TRACE"] < 1: return
  if PARAMS["TRACE"] >= 1 :
    caller = getframeinfo(stack()[1][0])
    print('DEBUG:',
        caller.filename.split('/')[-1],
        '->', caller.lineno, end=': ')
  print(*args, **kwargs)
