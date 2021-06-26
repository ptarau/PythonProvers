from utils import *
from formulas import *
from hprovers import *
from classifiers import *
from experiments import *
import random
random.seed(1234)

def padded_path(xs,max_l,pad=(0,0)) :
   ys=[(a+1,b+1) for (a,b) in xs]
   l=len(ys)
   assert l<=max_l
   zs= ys+([pad]*(max_l-l))
   return zs

def path_encoder(ts)  :

  xss=[path_of(t) for t in ts]
  max_l=max(len(xs) for xs in xss)
  for xs in xss:
     ys=padded_path(xs,max_l,pad=(0,0))
     yield [z for xy in ys for z in xy]

class ProofSet:
  def __init__(self,
               generator=hFormula,
               prover=hprove,
               encoder=path_encoder,
               term_size=6):
    self.formulas=[]
    self.proven=[]
    self.term_size=term_size
    self.generator=generator
    self.prover=prover
    self.encoder=encoder
    self.formula_count=0

  def build(self):
    for formula in self.generator(self.term_size):
      self.formula_count+=1
      is_proven=self.prover(formula)
      self.formulas.append(formula)
      self.proven.append(is_proven)
    codes=list(self.encoder(self.formulas))
    X=codes
    y=self.proven
    return X,y

class DataSet(ProofSet) :
  def __init__(self,split_perc=10,**kwargs):
    super().__init__(**kwargs)
    self.split_perc=split_perc

  def split(self):
     X,y=self.build()
     assert len(X)==len(y)
     data_size=len(X)
     k=self.split_perc*data_size//100
     Xy=list(zip(X,y))
     random.shuffle(Xy)
     vaXy,teXy=[],[]
     for _ in range(k) :
       vaXy.append(Xy.pop())
     for _ in range(k) :
       teXy.append(Xy.pop())
     X_tr,y_tr = zip(*Xy)
     X_va, y_va = zip(*vaXy)
     X_te, y_te = zip(*teXy)
     return X_tr,y_tr,X_va,y_va,X_te,y_te

class Learner:
  def __init__(self,classifier=rf_clf,dataset=None):
    self.classifier=classifier
    self.X_tr,self.y_tr,self.X_va,self.y_va,self.X_te,self.y_te=dataset.split()

  def run(self):
    res=run_with_data(self.classifier(),
                  self.X_tr,self.y_tr,self.X_va,self.y_va,self.X_te,self.y_te)

    def show_aucs(res):
      va,te=res
      print('\n', '-' * 40)
      print('VALIDATION:',round(va,4))
      print('TEST AUC:  ',round(te,4))
      print('-' * 40)

    show_aucs(res)

def test_ml1() :
  D=DataSet(generator=sFormula,term_size=6)
  L=Learner(classifier=rf_clf,dataset=D)
  L.run()

def test_ml2() :
  D=DataSet(generator=hFormula,term_size=6)
  L=Learner(classifier=rf_clf,dataset=D)
  L.run()

def test_ml3() :
  D=DataSet(generator=sFormula,term_size=6)
  L=Learner(classifier=neural_clf,dataset=D)
  L.run()

test_ml=test_ml3

if __name__=="__main__":
  test_ml()
