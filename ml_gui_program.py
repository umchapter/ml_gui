from PyQt5.QtWidgets import *
import sys, pickle
from PyQt5 import uic, QtWidgets ,QtCore, QtGui
from pandas import DataFrame
from data_visualise import data_

class UI(QMainWindow) :
    def __init__(self) :
        super(UI, self).__init__()
        uic.loadUi('main_Window.ui', self)

        global data
        data = data_()

        self.Browse = self.findChild(QPushButton, "Browse")
        self.columns = self.findChild(QListWidget, "Column_list")
        self.tabel = self.findChild(QTableView, "tabelView")

        self.Browse.clicked.connect(self.get_csv)

    def fillDetails(self, flag = 1) :
        if flag ==0 :
            self.df = data.read_file(set(self.filePath))

        # self.columns.clear()
        self.column_list = data.get_column_list(self.df)
        print(self.column_list)

        for i, j in enumerate(self.column_list) :
            # print(i, j)
            stri = f"{j}------{str(self.df[j].dtype)}"
            # print(stri)
            self.columns.insertItem(i, stri)
        
        df_shape = data.get_shape(self.df)
        self.data_shape.setText("a lot")
        self.fill_combo_box()

    def fill_combo_box(self) :
        x = DataFrameModel(self.df)
        self.tabel.setModel(x)

    def get_csv(self) : 
        self.filePath, _ = QFileDialog.getOpenFileName(self, "Open file", "", "csv(*.csv)")
        # self.columns.clear()
        print(self.filePath)
        if self.filePath != "" :
            self.fillDetails(0)




if __name__ == "__main__" :
    app = QtWidgets.QApplication(sys.argv)
    window = UI()
    window.show()

    sys.exit(app.exec_())