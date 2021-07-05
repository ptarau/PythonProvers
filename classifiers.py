from utils import *
import numpy as np
from sklearn.metrics import roc_auc_score
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier

learner_dict=dict()

def learner(f) :
  learner_dict[f.__name__]=f
  return f

@learner
def rf_clf() :
  return RandomForestClassifier(n_estimators=256,
                                       n_jobs=16,
                                       random_state=1234
                                       )

@learner
def neural_clf():
  #sizes = (128,72,128)
  sizes = (128,64,128)
  #sizes = (128,96,128)
  return MLPClassifier(
    early_stopping=False,
    shuffle=True,
    hidden_layer_sizes=sizes,
    random_state=1234,
    activation='logistic',
    max_iter=512,
    verbose=True
  )

def run_with_data(classifier,x_tr,y_tr,x_va,y_va,x_te,y_te,
                  score='acc',show=True):
  x_tr, y_tr, x_va, y_va, x_te, y_t= \
    tuple(map(np.array,[x_tr, y_tr, x_va, y_va, x_te, y_te]))

  def run() :
    nonlocal x_tr,y_tr
    if score=='cross':
      x_tr = np.concatenate((x_tr, x_va),axis=0)
      y_tr = np.concatenate((y_tr, y_va), axis=0)
    print(x_tr)
    print('SHAPES:',x_tr.shape,y_tr.shape)

    classifier.fit(x_tr,y_tr)

    if score=='acc':
      va = classifier.predict(x_va)
      te = classifier.predict(x_te)

      acc_va = accuracy_score(y_va, va)
      acc_te = accuracy_score(y_te, te)

      return acc_va, acc_te

    elif score=='auc':
      p_va = classifier.predict_proba(x_va)
      p_te = classifier.predict_proba(x_te)

      auc_va = roc_auc_score(y_va, p_va[:, 1])
      auc_te = roc_auc_score(y_te, p_te[:, 1])

    elif score == 'cross':
      scores = cross_val_score(classifier, x_tr, y_tr, cv=10)
      auc_va = scores.mean()
      te = classifier.predict(x_te)
      auc_te = accuracy_score(y_te,te)

      return auc_va,auc_te

  return run()
