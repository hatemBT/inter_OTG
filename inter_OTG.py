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
from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QGroupBox, QFormLayout, QPushButton, QLabel, QLineEdit, \
    QVBoxLayout, QTableWidget, QTableWidgetItem, QSizePolicy, QPlainTextEdit



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


        self.axes.set_xlim([-40, 40])
        self.axes.set_ylim([-40, 40])
        self.axes.set_aspect('equal')
        self.x = []
        self.y = []
        def onclick(event):
            self.x.append(np.round(event.xdata))
            self.y.append(np.round(event.ydata))
            circle = plt.Circle((event.xdata, event.ydata), 1, color='green')
            self.axes.add_patch(circle)
            fig.canvas.draw()  # this line was missing earli
            print(self.x)
            print(self.y)


        cid = fig.canvas.mpl_connect('button_press_event', onclick)








    def interpolate(self):

        x = np.array(self.x)
        y = np.array(self.y)



        with open('xpoints.txt', 'a') as f:
            for i in self.x:
                f.write(str(i) + ',')

        with open('ypoints.txt', 'a') as f:
            for i in self.y:
                f.write(str(i) + ',')


        fit = np.polyfit(x, y, len(x) - 1)
        xx = np.linspace(min(x), max(x))
        fct = np.poly1d(fit)

        with open('fonction.txt', 'w') as f:
            f.write(str(fct))

        yy = np.polyval(fit, xx)
        global ax
        ax = self.figure.add_subplot(111)

        ax.plot(xx, yy, '-')


        ax.set_title('Inetrpolating function')
        ax.set_xlabel('x coordinates')
        ax.set_ylabel('f(x) ')

        self.draw()

        return (len(x),str(fct))




class Inter_OTG(QWidget):

    def __init__(self):
        self.x = []
        self.y = []
        super(Inter_OTG, self).__init__()
        self.canvas  = PlotCanvas
        self.setGeometry(160, 100, 815, 520)
        self.setWindowTitle("H.B Tayeb : Inter_OTG")
        self.grid = QGridLayout()
        self.grid2 = QGridLayout()
        self.allGB = QGroupBox("DATA IN/OUT")
        self.allGB.setLayout(self.grid2)
        # -------------------------------------------------
        self.fonct = QPlainTextEdit()
        self.fonct.adjustSize()


        self.qb = QGroupBox("Polynomial ")
        self.qf = QFormLayout()

        self.clear = QPushButton("Clear Data")

        # -------------------------------------------------
        self.qb1 = QGroupBox("Load DATA")  # --->
        self.plotfig = QGroupBox("the result graph")
        self.qV = QVBoxLayout()

        self.table = QTableWidget()

        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Xi", "Yi"])
        self.m = PlotCanvas(self, width=5, height=4)
        self.load = QPushButton("Load Data")

        # -------------------------------------------------
        self.getfct = QPushButton("get function")
        self.qb1.setLayout(self.qV)
        self.qV.addWidget(self.table)
        self.qV.addWidget(self.load)

        self.qf.addRow(self.clear)
        self.qf.addRow(self.fonct)
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


        self.load.clicked.connect(lambda: self.load_data_interpolate())



        self.clear.clicked.connect(lambda: self.clear_data())
        self.getfct.clicked.connect(lambda: self.get_fct())





    xi = []
    yi = []

    def load_data_interpolate(self):
        length,fct = self.m.interpolate()
        self.fonct.insertPlainText(fct)
        self.table.setRowCount(length)
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
        try:
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

        except (IOError,IndexError):
            print("files already deleted !")




if __name__ == '__main__':
    app = QApplication(sys.argv)  # definir l'application gloabal
    appp = Inter_OTG()  # notre application de type widget
    appp.show()  # afficher notre application
    sys.exit(app.exec_())  # exécuter
