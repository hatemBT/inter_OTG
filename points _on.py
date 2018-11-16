import matplotlib.pyplot as plt
import numpy as np

x=[]
y=[]

def onclick(event):
    global x
    global y
    global f
    x.append(np.round(event.xdata))
    y.append(np.round(event.ydata))
    print(x)
    print(y)





t= np.linspace(0,100,200)
fig,    pl = plt.subplots()

cid = fig.canvas.mpl_connect('button_press_event', onclick)
pl.plot(t, 'r')
plt.show()



