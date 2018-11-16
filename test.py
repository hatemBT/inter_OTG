import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import lagrange
from numpy.polynomial.polynomial import Polynomial

# get x and y vectors

x=[1, 4, 6, 8]
y=[7, 6, 8, 4]

#x= [np.round(i)for i in x1]
#y= [np.round(i)for i in y1]
print(x)
print(y)

# calculate polynomial
poly = lagrange(x, y)
f=Polynomial(poly).coef
print(f)
# calculate new x's and y's

t=np.linspace(0,10,10)

plt.plot(x,y,'o', np.polyval(f,t))
plt.show()


