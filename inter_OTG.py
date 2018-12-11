#####################################################
#              Auther : hatem ben tayeb             #
#              Email : hatemtayeb2@gmail.com        #
#              Script : analyse numerique           #
#              Subjet : interpolation               #
#####################################################

"""
        Cette application permet de generer une interpolation d'un ensembles des points données

 """
import sys
import qdarkstyle
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QGroupBox, QPushButton,\
    QVBoxLayout, QTableWidget, QTableWidgetItem, QSizePolicy


class PlotCanvas(FigureCanvas,QWidget):
    """
    la classe PlotCanvas permet de crée la figure

    """

    def __init__(self, parent=None, width=10, height=10, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.axes.grid()
        self.axes.set_xlim([-50, 50])
        self.axes.set_ylim([-50, 50])
        self.axes.set_aspect('auto')

        self.xpts = []  # x
        self.ypts = []  # y

        def onclick(event):
            """
                cette méthode permet de récupérer les coordonnés du curseur suite a une click sur la figure

                 :event: objet event contients les coordonnés (x,y) du cursuer

            """

            self.clear()

            self.xpts.append(np.round(event.xdata))
            self.ypts.append(np.round(event.ydata))
            circle = plt.Circle((event.xdata, event.ydata), 0.5, color='green')
            self.axes.add_patch(circle)
            fig.canvas.draw()
            self.interpolate()
            print(self.getxy())



        # exécution du la méthode onclick par le canvas
        cid = fig.canvas.mpl_connect('button_press_event', onclick)


    def interpolate(self ):
        """
            cette méthode permet de faire l'opération d'interpolation

            :self: donne la vision sur toute la classe

            output
            :len(x1): longeur du liste x1
            :self.xpts: la liste des points d'absisses
            :self.ypts: la liste des points d'ordonnés

            NB: cette methode retourne un affichage symbolique de polynome d'interpolation (sympy)

        """
       # self.clear()
        sp.init_printing()

        X = sp.symbols('x')
        x1 = np.array(self.xpts)
        yy = np.array(self.ypts)

        # x et y en rationel
        Rx = [sp.Rational(i) for i in x1]
        Ry = [sp.Rational(i) for i in yy]

        # rendre les deux listes en une seule liste des tuples
        res = list(zip(Rx, Ry))

        # interpolation avec sympy
        pol = sp.interpolate(res, X)

        sf = sp.simplify(pol)
        # print(pol)
        # print(sf)

        fit = np.polyfit(x1, yy, len(x1) - 1)
        xx = np.linspace(min(x1), max(x1))
        zz = np.polyval(fit, xx)

        global ax
        ax = self.figure.add_subplot(111)

        if(len(self.xpts)==1):
            ax.hlines(self.ypts,-50,50,color='red',lw=2)

        ax.plot(xx, zz, '-', label="polynome deg={}".format(sp.degree(sf, X)), color='red',lw=2)
        ax.scatter(self.xpts,self.ypts,color='blue',lw=1)
        for i in range(len(self.xpts)):
               ax.annotate(xy=[self.xpts[i], self.ypts[i]], text="({},{})".format(self.xpts[i], self.ypts[i]),color='green',size=5)

        ax.legend()

        ax.set_title('P(x)=$' + sp.latex(sf) + '$\n', color='blue',size=10)
        ax.set_xlabel('x coordinates', color='blue')
        ax.set_ylabel('f(x) ', color='blue')

        self.draw()

        return (len(x1), self.xpts, self.ypts)

    def getxy(self):
        if (len(self.xpts) != 0):
            return self.xpts[-1], self.ypts[-1]


        return None

    def clr(self):
        """
                vider la figure pour une nouvelle courbe
        """
        self.axes.cla()
        self.axes.grid()
        self.axes.set_xlim([-50, 50])
        self.axes.set_ylim([-50, 50])
        self.axes.set_aspect('equal')
        self.xpts = []
        self.ypts = []
        self.draw()

    def clear(self):
        self.axes.cla()
        self.axes.grid()
        self.axes.set_xlim([-50, 50])
        self.axes.set_ylim([-50, 50])
        self.axes.set_aspect('equal')
        self.draw()


class Inter_OTG(QWidget):
    """
        cette classe permet de crée les composantes du l'application( aspect graphique) avec pyqt5


    """
    def __init__(self):

        self.xpts = []
        self.ypts = []
        super(Inter_OTG, self).__init__()

        self.setGeometry(160, 100, 600, 600)
        self.setWindowTitle("H.B Tayeb : Inter_OTG")
        self.m = PlotCanvas(self, width=5, height=4)







        self.clear = QPushButton("clear GRAPH")


        # -------------------------------------------------



        # -------------------------------------------------
        self.plotfig = QGroupBox("The result graph")
        self.qV2 = QVBoxLayout()  # ---->
        self.qV2.addWidget(self.m)
        self.qV2.addWidget(self.clear)
        self.plotfig.setLayout(self.qV2)
        self.grid2 = QGridLayout()
        self.grid2.addWidget(self.plotfig, 0, 1)
        self.setLayout(self.grid2)
        # -------------------------------------------------

        self.style = qdarkstyle.load_stylesheet_pyqt5()
        self.setStyleSheet(self.style)
        self.clear.clicked.connect(lambda: self.clear_data())

        self.xypts = self.m.getxy()



    xi = []
    yi = []



    def test(self):
        pass

    def clear_data(self):
        """
            cette methode fait l'appelle a la méthode clr du class PlotCanvas

        """
        self.m.clr()

















if __name__ == '__main__':
    app = QApplication(sys.argv)  # definir l'application gloabal
    appp = Inter_OTG()  # notre application de type widget
    appp.show()  # afficher notre application
    sys.exit(app.exec_())  # exécuter
