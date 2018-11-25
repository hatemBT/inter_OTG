#####################################################
#              Auther : hatem ben tayeb             #
#              Email : hatemtayeb2@gmail.com        #
#              Script : analyse numerique           #
#              Subjet : interpolation               #
#####################################################


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QGroupBox, QPushButton,\
    QVBoxLayout, QTableWidget, QTableWidgetItem, QSizePolicy


class PlotCanvas(FigureCanvas):

    global fig
    def __init__(self, parent=None, width=10, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)


        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,QSizePolicy.Expanding,QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.axes.grid()
        self.axes.set_xlim([-50, 50])
        self.axes.set_ylim([-50, 50])
        self.axes.set_aspect('equal')

        self.xpts = []
        self.ypts = []
        def onclick(event):
            self.xpts.append(np.round(event.xdata))
            self.ypts.append(np.round(event.ydata))
            circle = plt.Circle((event.xdata, event.ydata), 1, color='green')
            self.axes.add_patch(circle)
            fig.canvas.draw()
            print(self.xpts)
            print(self.ypts)


        cid = fig.canvas.mpl_connect('button_press_event', onclick)








    def interpolate(self):


        sp.init_printing()

        X = sp.symbols('x')

        x1 = np.array(self.xpts)
        yy = np.array(self.ypts)

        Rx = [sp.Rational(i) for i in x1]
        Ry = [sp.Rational(i) for i in yy]
        res = list(zip(Rx, Ry))

        
        pol = sp.interpolate(res, X)
        sf = sp.sympify(pol)
        print(pol)
        print(sf)


        try:
            with open('xpoints.txt', 'a') as f:
                for i in self.xpts:
                    f.write(str(i) + ',')

            with open('ypoints.txt', 'a') as f:
                for i in self.ypts:
                    f.write(str(i) + ',')
        except (IOError,IndexError):
            print("Error saving files !")


        fit = np.polyfit(x1, yy, len(x1) - 1)
        xx = np.linspace(min(x1), max(x1))
        #fct = np.poly1d(fit)



        yy = np.polyval(fit, xx)
        global ax
        ax = self.figure.add_subplot(111)

        ax.plot(xx, yy, '-',label="interpolation function")
        for i in range(len(self.xpts)):
            ax.annotate(xy=[self.xpts[i], self.ypts[i]], text="({},{})".format(self.xpts[i], self.ypts[i]))

        ax.legend()


        ax.set_title('$'+sp.latex(sf)+'$')
        ax.set_xlabel('x coordinates')
        ax.set_ylabel('f(x) ')
        self.draw()

        return (len(x1),self.xpts,self.ypts)

    def clr(self):
        self.axes.cla()
        self.axes.grid()
        self.axes.set_xlim([-50, 50])
        self.axes.set_ylim([-50, 50])
        self.axes.set_aspect('equal')
        self.xpts = []
        self.ypts = []
        self.draw()




class Inter_OTG(QWidget):

    def __init__(self):
        self.xpts = []
        self.ypts = []
        super(Inter_OTG, self).__init__()
        self.canvas  = PlotCanvas
        self.setGeometry(160, 100, 725, 520)
        self.setWindowTitle("H.B Tayeb : Inter_OTG")

        self.clear = QPushButton("Clear Data")
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.verticalHeader().hide()
        self.table.setHorizontalHeaderLabels(["Xi", "Yi"])
        self.m = PlotCanvas(self, width=5, height=4)
        self.load = QPushButton("Get and Inetrpolate ")
        self.allGB = QGroupBox("DATA IN/OUT")
        self.qV = QVBoxLayout()
        self.allGB.setLayout(self.qV)
        self.qV.addWidget(self.clear)
        self.qV.addWidget(self.table)
        self.qV.addWidget(self.load)

        # -------------------------------------------------



        # -------------------------------------------------
        self.plotfig = QGroupBox("the result graph")
        self.qV2 = QVBoxLayout()  # ---->
        self.qV2.addWidget(self.m)
        self.plotfig.setLayout(self.qV2)
        self.grid2 = QGridLayout()
        self.grid2.addWidget(self.allGB, 0, 0)
        self.grid2.addWidget(self.plotfig, 0, 1)
        self.setLayout(self.grid2)
        # -------------------------------------------------


        self.load.clicked.connect(lambda: self.load_data_interpolate())
        self.clear.clicked.connect(lambda: self.clear_data())





    xi = []
    yi = []

    def load_data_interpolate(self):
        length,valx,valy = self.m.interpolate()
        self.table.setRowCount(length)
        global xi
        global yi



        cp = 0

        for i in valx:
            self.table.setItem(cp, 0, QTableWidgetItem(str(i)))
            self.xi.append(float(i))
            cp += 1

        cp1 = 0
        for i in valy:
            if i != None:
                self.table.setItem(cp1, 1, QTableWidgetItem(str(i)))
                self.yi.append(float(i))
                cp1 += 1





    def clear_data(self):
        self.m.clr()
        self.table.setRowCount(0)




if __name__ == '__main__':
    app = QApplication(sys.argv)  # definir l'application gloabal
    appp = Inter_OTG()  # notre application de type widget
    appp.show()  # afficher notre application
    sys.exit(app.exec_())  # exécuter
