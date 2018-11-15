from numpy import *

def Neville(x, xdata, ydata):
    """return p[xdata](x)"""
    xdata = x - xdata
    print xdata
    n = len(xdata)
    for i in range(1,n):
        num = xdata[:n-i]*ydata[1:n-i+1] - xdata[1:n-i+1]*ydata[:n-i]       
        den = xdata[:n-i] - xdata[i:n]
        ##ydata[:n-i] = num/den
        ydata[:n-i] = (xdata[:n-i]*ydata[1:n-i+1] - xdata[1:n-i+1]*ydata[:n-i])/(xdata[:n-i] - xdata[i:n])
    return ydata[0]




print Neville(0,array([1,2,3]),array([1,2,1]))