from PyQt5.QtWidgets import *
import sys, pickle
from PyQt5 import uic, QtWidgets ,QtCore, QtGui


class UI(QMainWindow) :
    def __init__(self) :
        super(UI, self).__init__()
        uic.loadUi('main_Window.ui', self)

        # self.show()


if __name__ == "__main__" :
    app = QtWidgets.QApplication(sys.argv)
    window = UI()
    window.show()

    sys.exit(app.exec_())