
from cmath import *
from numpy.polynomial import polynomial as P
from numpy.fft import *
from dcolor import *
import matplotlib.pyplot as plt

from formulas import *

def path_of(term,start=0) :
  def step(t,n) :
    if isinstance(t, tuple):
      h, bs = t
      for b in bs:
        for xs in step(b,n+1):
          yield ((n,h),) + xs
    else:
      yield ((n,t),)
  css=list(step(term,start))
  cs = {c for cs in css for c in cs}
  return sorted(cs)

def df_code(term) :
  """
  assumes terms canonically sorted
  for code to be the same for equivlent formulas
  """
  cs=[]

  def visit(t):
    if simple(t) :
      cs.append(t+2)
    else:
      h,bs=t
      cs.append(h+2)
      cs.append(1)
      for b in bs:
        visit(b)
      cs.append(0)
  visit(term)
  return cs

def path2cs(xs):
  cs=[]
  for n,x in xs :
     c=rect((1+n),(1+x))
     cs.append(c)
  return cs

def cs2path(cs):
  xs=[]
  for c in cs :
     #c=rect(1/(1+n),(1+x))
     pf=polar(c)
     a=pf[0]
     n=a-1
     x=pf[1]-1
     xs.append((n,x))
  xs=sorted(xs)#,key=lambda v:v[0])
  return xs

def identity(x) :
  return x

def cs2poly(cs):
  return P.polyfromroots(cs)

def poly2cs(ps) :
  return P.polyroots(ps)

def cs2fft(cs):
  return fft(cs)

def fft2cs(cs):
  return ifft(cs)

def css2fft(css):
  return fft(css)

def funchain(fs,x):
  r=x
  for f in fs:
    r=f(r)
  return r

def to_poly(cs) :
  def f(z) :
    r=1
    for c in cs:
      r*=(z-c)
    return r
  return f

def plot_ps(ps) :
  x,y=zip(*ps)
  plt.scatter(x,y)
  plt.show()

def plot_cs(cs) :
  dc = DColor(xmin=-10, xmax=10, ymin=-10, ymax=10, samples=1000)
  f=to_poly(cs)
  dc.plot(lambda z : f(z))

def poly_code(t):
  fs=[path2cs,cs2poly]
  p=path_of(t)
  return funchain(fs,p)

def fft_code(t):
  fs=[path2cs,cs2fft]
  p=path_of(t)
  return funchain(fs,p)


# tests
def pic_test(size=20) :
  t=ranHorn(size)
  print('TERM:',t)
  p=path_of(t)
  print('PATH:',p)
  #p=[2,4]
  cs=path2cs(p)
  #cs=cs2poly(cs)
  cs = fft(cs)
  plot_cs(cs)

def test_encoders(n=2) :
  for t in hFormula(n):
    print('\nFORMULA',t)

    p=path_of(t)
    print('PATH, ORIG:', p)
    cs = path2cs(p)
    p_ = cs2path(cs)
    print('PATH, AGAIN:', p_)
    print('')
    ds=df_code(t)
    print("DEPTH FIRST CODE:",ds)
    cs = sorted(cs, key=lambda x: x.real)
    print('COMPLEX VECT', p, len(cs) * 2, cs)
    ps = cs2poly(cs)
    print('POLY', p, len(ps) * 2, ps)
    cs_ = poly2cs(ps)
    print('COMP. VECT. AGAIN:',sorted(cs_,key=lambda x:x.real))
    print('')
    fs = cs2fft(cs)
    print('FFT', p, len(fs) * 2, fs)
    cs__ = fft2cs(fs)
    print('BACK FROM FFT', p, len(fs) * 2, cs__)
    print('----------')

    print("\nPOLY CODES:")
    for res in poly_code(t) :
      print(res)

    print("\nFFT CODES:")
    for res in fft_code(t):
      print(res)

    print('=================\n')

if __name__=="__main__":
  pass
  test_encoders()

  pic_test()
