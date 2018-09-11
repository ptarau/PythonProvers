# PythonProvers
Intuitionistic Theorem Provers and Formula Generators in Python

## Tested with python 3.7.0

## Main components:

* generator all implicational formulas of size n (note that implication i->j is represented as the tuple (i,j) with i,j natural numbers

* generator for random implicational formulas combining Remy's algorithm and a random set partition generator
* an implicational propositional intuitionistic logic theorem prover
* a generator for closed lambda terms and a type inference algorithm for generating simply-typed terms of a given size
* tests on a Python-readable version of the ILTP propositional logic tests

## Examples of use

```
after python3 -i tester.py
try out:

>>> list(iFormula(3))
...
>>> s
((0, (1, 2)), ((0, 1), (0, 2)))
>>> iprove(s)
True

>>> it = ('->','p',('~', ('~','p')))
>>> it = expandNeg(it)
>>> fprove(it)
True

>>> allFormTest(6)
6 provable 27406 total 115764 unprovable 88358 ratio 0.23674026467641063
>>> fullFormTest(7)
7 provable 2067 total 39369 unprovable 37302 ratio 0.05250323858873733

```

See more examples of use in tester.py .
