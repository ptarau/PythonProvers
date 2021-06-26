from utils import *
import numpy as np
from sklearn.metrics import roc_auc_score
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
  #sizes = (128,72,128)  # 0.7780
  sizes = (128,64,128)   # 0.7791 <= BEST
  #sizes = (128,96,128)  # 0.7638
  #ppp('MLP hidden unit sizes:',sizes)
  return MLPClassifier(
    early_stopping=False,
    shuffle=True,
    hidden_layer_sizes=sizes,
    random_state=1234,
    activation='logistic',
    max_iter=400
  )

def run_with_data(classifier,x_tr,y_tr,x_va,y_va,x_te,y_te,show=True):
  x_tr, y_tr, x_va, y_va, x_te, y_t= \
    tuple(map(np.array,[x_tr, y_tr, x_va, y_va, x_te, y_te]))

  def run() :
    scores = []
    print(x_tr)
    print('SHAPES:',x_tr.shape,y_tr.shape)
    classifier.fit(x_tr,y_tr)

    p_va = classifier.predict_proba(x_va)
    p_te = classifier.predict_proba(x_te)

    auc_va = roc_auc_score(y_va, p_va[:, 1])
    auc_te = roc_auc_score(y_te, p_te[:, 1])

    scores.append(auc_va)
    scores.append(auc_te)
    return scores

  return run()
