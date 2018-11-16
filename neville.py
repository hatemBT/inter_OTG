#####################################################
#              Auther : hatem ben tayeb             #
#              Email : hatemtayeb2@gmail.com        #
#              Script : eval_perform                #
#              Subjet : evaluation de performance   #
#####################################################

from scipy.interpolate import lagrange,interp1d
from numpy.polynomial.polynomial import Polynomial
import sys
import time
import os
import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QGroupBox, QFormLayout, QPushButton, QLabel, QLineEdit, \
    QVBoxLayout, QTableWidget, QComboBox, QTableWidgetItem


class inter_OTG(QWidget):



    def __init__(self):
        self.x = []
        self.y = []
        super(inter_OTG, self).__init__()
        self.setGeometry(100, 200, 287, 400)
        self.setWindowTitle("Easy_interpolation")
        self.grid = QGridLayout()
        # -------------------------------------------------
        self.combo = QComboBox()
        itm= ["lagrange","neville","newton"]
        for i in itm:
            self.combo.addItem(i)
        self.qb = QGroupBox("Manipulate")
        self.qf = QFormLayout()
        self.x0 = QLabel("X0 : ")
        self.x0F = QLineEdit("3")
        self.start = QPushButton("Start")
        self.clear = QPushButton("clear")

        # -------------------------------------------------
        self.qb1 = QGroupBox("View DATA")
        self.qV = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setRowCount(10)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Xi", "Yi"])

        self.load = QPushButton("Load Data")
        self.interP = QPushButton("interpolate points")
        # -------------------------------------------------
        self.qb1.setLayout(self.qV)
        self.qV.addWidget(self.table)
        self.qV.addWidget(self.load)
        self.qV.addWidget(self.interP)
        self.qf.addRow(self.combo)
        self.qf.addRow(self.x0, self.x0F)
        self.qf.addRow(self.start, self.clear)
        self.qb.setLayout(self.qf)

        self.grid.addWidget(self.qb, 0, 0)
        self.grid.addWidget(self.qb1, 1, 0)
        self.setLayout(self.grid)
        # -------------------------------------------------

        self.start.clicked.connect(lambda : get_points(self))
        self.load.clicked.connect(lambda : load_data(self))
        self.interP.clicked.connect(lambda :interpolate(self))
        self.clear.clicked.connect(lambda : clear_data())



def clear_data():
    os.remove("xpoints.txt")
    os.remove("ypoints.txt")

def get_points(self):
    x = []
    y = []

    def onclick(event):

        x.append(np.round(event.xdata))
        y.append(np.round(event.ydata))
        print(x)
        print(y)


    fig, pl = plt.subplots()
    pl.axis([0,10,0,10])

    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    #pl.plot(t, 'r')
    plt.show()

    with open('xpoints.txt','w') as f:
        for i in x :
            f.write(str(i)+',')

    with open('ypoints.txt','w') as f:
        for i in y :
            f.write(str(i)+',')

xi =[]
yi = []
def load_data(self):
    global xi
    global yi

    cp = 0
    with open('xpoints.txt', 'r') as f:
        xx = f.read().split(',')
        for i in xx[:-1]:
            if i != None:
                self.table.setItem(cp, 0, QTableWidgetItem(str(i)))
                xi.append(round(float(i)))
                cp+=1
            else:
                pass

    cp1 = 0
    with open('ypoints.txt', 'r') as f:
        xx = f.read().split(',')
        for i in xx[:-1]:
            if i != None:
                self.table.setItem(cp1, 1, QTableWidgetItem(str(i)))
                yi.append(round(float(i)))
                cp1+=1
            else:
                pass


    print(xi)
    print(yi)


def interpolate(self):
    x= np.array(xi)
    y= np.array(yi)

    x0 = float(self.x0F.text())
    fit = np.polyfit(x,y,x0)
    xx = np.linspace(min(x), max(x))
    yy = np.polyval(fit, xx)

    plt.plot(xx, yy, '-', x, y, 'ro')
    plt.axis([min(xx) , max(xx) , min(yy) , max(yy) ]);

    # poly = lagrange(x, y)
    # f = Polynomial(poly).coef
    # print(f)
    # # calculate new x's and y's
    #
    # t = np.linspace(0, 20, 100)


    plt.show()






if __name__ == '__main__':
    app = QApplication(sys.argv)  # definir l'application gloabal
    appp = inter_OTG()  # notre application de type widget
    appp.show()  # afficher notre application
    sys.exit(app.exec_())  # exécuter
