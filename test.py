# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.interpolate import lagrange
# from numpy.polynomial.polynomial import Polynomial
#
# # get x and y vectors
# #
# # x=[1, 4, 6, 8]
# # y=[7, 6, 8, 4]
# #
# # #x= [np.round(i)for i in x1]
# # #y= [np.round(i)for i in y1]
# # print(x)
# # print(y)
# #
# # # calculate polynomial
# # poly = lagrange(x, y)
# # f=Polynomial(poly).coef
# # print(f)
# # # calculate new x's and y's
# #
# # t=np.linspace(0,10,10)
# #
# # plt.plot(x,y,'o', np.polyval(f,t))
# # plt.show()
#
#
#
#
# """
# Show how to modify the coordinate formatter to report the image "z"
# value of the nearest pixel given x and y
# """
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.cm as cm
#
# X = 10*np.random.rand(5,3)
#
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.imshow(X, cmap=cm.jet, interpolation='nearest')
#
# numrows, numcols = X.shape
# def format_coord(x, y):
#     col = int(x+0.5)
#     row = int(y+0.5)
#     if col>=0 and col<numcols and row>=0 and row<numrows:
#         z = X[row,col]
#         return 'x=%1.4f, y=%1.4f, z=%1.4f'%(x, y, z)
#     else:
#         return 'x=%1.4f, y=%1.4f'%(x, y)
#
# ax.format_coord = format_coord
# plt.show()
#
#


from matplotlib.widgets import Cursor
import numpy as np
import matplotlib.pyplot as plt


# Fixing random state for reproducibility
np.random.seed(19680801)

fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, facecolor='#FFFFCC')

x, y = 4*(np.random.rand(2, 100) - .5)
ax.plot(x, y, 'o')
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)

# Set useblit=True on most backends for enhanced performance.
cursor = Cursor(ax, useblit=True, color='red', linewidth=2)

plt.show()

