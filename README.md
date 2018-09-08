# PythonProvers
Intuitionistic Theorem Provers and Formula Generators in Python

## Tested with python 3.7.0

## Main components:

* generator all implicational formulas of size n (note that implication i->j is represented as the tuple (i,j) with i,j natural numbers

* generator for random implicational formulas combining Remy's algorithm and a random set partition generator
* an implicational propositional intuitionistic logic theorem prover
* a generator for closed lambda terms and a type inference algorithm for generating simply-typed terms of a given size

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
```

See more examples of use in tester.py .

