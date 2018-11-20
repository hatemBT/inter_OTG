import numpy as np
import sympy as sp
from sympy.abc import x
nppoly = np.polynomial.polynomial.Polynomial([1,2,3])




sp.init_printing()
print(sp.Poly(reversed(nppoly.coef),x).as_expr())