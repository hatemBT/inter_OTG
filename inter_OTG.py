#####################################################
#              Auther : hatem ben tayeb             #
#              Email : hatemtayeb2@gmail.com        #
#              Script : analyse numerique           #
#              Subjet : interpolation               #
#####################################################


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from PyQt5.QtWidgets import QSizePolicy

import sys
import time
import os
import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QGroupBox, QFormLayout, QPushButton, QLabel, QLineEdit, \
    QVBoxLayout, QTableWidget, QComboBox, QTableWidgetItem, QSizePolicy, QPlainTextEdit


class Inter_OTG(QWidget):

    def __init__(self):
        self.x = []
        self.y = []
        super(Inter_OTG, self).__init__()
        self.setGeometry(160, 100, 815, 520)
        self.setWindowTitle("Easy_interpolation")
        self.grid = QGridLayout()
        self.grid2 = QGridLayout()
        self.allGB = QGroupBox("settings")
        self.allGB.setLayout(self.grid2)
        # -------------------------------------------------
        self.fonct = QPlainTextEdit()
        self.fonct.adjustSize()

        self.combo = QComboBox()
        itm = ["lagrange", "neville", "newton"]
        for i in itm:
            self.combo.addItem(i)
        self.qb = QGroupBox("Manipulate")
        self.qf = QFormLayout()
        self.x0 = QLabel("X0 : ")
        self.x0F = QLineEdit("3")
        self.start = QPushButton("Start")
        self.clear = QPushButton("clear")

        # -------------------------------------------------
        self.qb1 = QGroupBox("Load DATA")  # --->
        self.plotfig = QGroupBox("interpolate")
        self.qV = QVBoxLayout()

        self.table = QTableWidget()

        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Xi", "Yi"])
        self.m = PlotCanvas(self, width=5, height=4)
        self.load = QPushButton("Load Data")
        self.interP = QPushButton("interpolate points")
        # -------------------------------------------------
        self.getfct = QPushButton("get function")
        self.qb1.setLayout(self.qV)
        self.qV.addWidget(self.table)
        self.qV.addWidget(self.load)
        self.qV.addWidget(self.interP)
        self.qf.addRow(self.combo)
        self.qf.addRow(self.x0, self.x0F)
        self.qf.addRow(self.start, self.clear)
        self.qf.addRow(self.fonct)
        self.qf.addRow(self.getfct)
        self.qb.setLayout(self.qf)

        self.qV2 = QVBoxLayout()  # ---->
        self.qV2.addWidget(self.m)
        self.plotfig.setLayout(self.qV2)

        self.grid2.addWidget(self.qb, 0, 0)
        self.grid2.addWidget(self.qb1, 1, 0)
        self.grid.addWidget(self.allGB, 0, 0)
        self.grid.addWidget(self.plotfig, 0, 1)
        self.setLayout(self.grid)
        # -------------------------------------------------

        self.start.clicked.connect(lambda: self.get_points())
        self.load.clicked.connect(lambda: self.load_data())
        self.interP.clicked.connect(lambda: self.m.interpolate())

        # self.fonct.insertPlainText(PlotCanvas.interpolate(self))
        self.clear.clicked.connect(lambda: self.clear_data())
        self.getfct.clicked.connect(lambda: self.get_fct())

    def get_fct(self):
        with open('fonction.txt', 'r') as f:
            self.fonct.insertPlainText(f.read())
            # print(f.read())

    def get_points(self):
        x = []
        y = []

        def onclick(event):

            x.append(np.round(event.xdata))
            y.append(np.round(event.ydata))
            print(x)
            print(y)


        fig, pl = plt.subplots()
        pl.axis([0, 10, 0, 10])

        cid = fig.canvas.mpl_connect('button_press_event', onclick)
        # pl.plot(t, 'r')
        #plt.pause(0.2)

        plt.plot(x, y,'ro')
        plt.show()
        with open('xpoints.txt', 'w') as f:
            for i in x:
                f.write(str(i) + ',')

        with open('ypoints.txt', 'w') as f:
            for i in y:
                f.write(str(i) + ',')

        self.table.setRowCount(len(x))


    xi = []
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
                    self.xi.append(round(float(i)))
                    cp += 1
                else:
                    pass

        cp1 = 0
        with open('ypoints.txt', 'r') as f:
            xx = f.read().split(',')
            for i in xx[:-1]:
                if i != None:
                    self.table.setItem(cp1, 1, QTableWidgetItem(str(i)))
                    self.yi.append(round(float(i)))
                    cp1 += 1
                else:
                    pass




    def clear_data(self):
        os.remove("xpoints.txt")
        os.remove("ypoints.txt")
        os.remove("fonction.txt")
        self.fonct.clear()
        for i in range(self.table.rowCount()):
            for j in range(self.table.columnCount()):
                self.table.setItem(i, j, QTableWidgetItem("0.0"))

        self.xi = []
        self.yi = []
        self.table.setRowCount(len(self.xi))



class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    # def plot(self):
    #     data = [np.random.random() for i in range(25)]
    #     ax = self.figure.add_subplot(111)
    #     ax.plot(data, 'r-')
    #     ax.set_title('Interpolation ')
    #     self.draw()

    def interpolate(self):
        x = np.array(Inter_OTG.xi)
        y = np.array(Inter_OTG.yi)

        # x0 = float(self.x0F.text())
        fit = np.polyfit(x, y, len(x) - 1)
        xx = np.linspace(min(x), max(x))
        fct = np.poly1d(fit)
        print(fct)
        with open('fonction.txt', 'w') as f:
            f.write(str(fct))

        yy = np.polyval(fit, xx)
        global ax
        ax = self.figure.add_subplot(111)
        ax.plot(xx, yy, '-', x, y, 'ro')
        ax.set_title('Interpolation')
        ax.set_xlabel('x coordinates')
        ax.set_ylabel('f(x) ')
        ax.axis([min(xx), max(xx), min(yy), max(yy)])


        # poly = lagrange(x, y)
        # f = Polynomial(poly).coef
        # print(f)
        # # calculate new x's and y's
        #
        # t = np.linspace(0, 20, 100)plt

        self.draw()

        return fct




if __name__ == '__main__':
    app = QApplication(sys.argv)  # definir l'application gloabal
    appp = Inter_OTG()  # notre application de type widget
    appp.show()  # afficher notre application
    sys.exit(app.exec_())  # exécuter
