from PyQt5.QtWidgets import *
import sys,pickle
from PyQt5 import uic, QtWidgets ,QtCore, QtGui
from data_visualise import data_
from table_display import DataFrameModel
from add_steps import add_steps
from Linear_RG import print_success


class UI(QMainWindow) :
    def __init__(self) :
        super(UI, self).__init__()
        uic.loadUi('main_Window.ui', self)

        global data, steps
        data = data_()
        steps = add_steps()

        self.Browse = self.findChild(QPushButton, "Browse")
        self.columns = self.findChild(QListWidget, "Column_List")
        self.tabel = self.findChild(QTableView, "tableView")
        self.data_shape = self.findChild(QLabel, "Shape")
        self.target_col = self.findChild(QLabel, "label_2")
        self.submit_btn = self.findChild(QPushButton, "Submit")
        self.cat_column = self.findChild(QComboBox, "cat_column")
        self.convert_btn = self.findChild(QPushButton, "Convert")
        self.drop_column = self.findChild(QComboBox, "drop_column")
        self.drop_btn = self.findChild(QPushButton, "Drop")
        self.empty_column = self.findChild(QComboBox, "empty_column")
        self.fill_mean_btn = self.findChild(QPushButton, "Fill_mean")
        self.fill_0_btn = self.findChild(QPushButton, "Fill_0")
        self.scaler = self.findChild(QComboBox, "Scaler") 
        self.scale_btn = self.findChild(QPushButton, "Scale_btn")
        self.scatter_x = self.findChild(QComboBox, "scatter_x")
        self.scatter_y = self.findChild(QComboBox, "scatter_y")
        self.scatter_btn = self.findChild(QPushButton, "Scatter_plot")
        self.colour = self.findChild(QComboBox, "colour")
        self.marker = self.findChild(QComboBox, "marker")
        self.plot_x = self.findChild(QComboBox, "plot_x")
        self.plot_y = self.findChild(QComboBox, "plot_y")
        self.plot_btn = self.findChild(QPushButton, "Line_plot")
        self.colour_2 = self.findChild(QComboBox, "colour_2")
        self.marker_2 = self.findChild(QComboBox, "marker_2")
        self.model_selection = self.findChild(QComboBox, "Model_Selection")
        self.train_btn = self.findChild(QPushButton, "Train_Btn")

        self.Browse.clicked.connect(self.get_csv)
        self.columns.clicked.connect(self.target)
        self.submit_btn.clicked.connect(self.set_target)
        self.convert_btn.clicked.connect(self.con_cat)
        self.drop_btn.clicked.connect(self.dropc)
        self.fill_mean_btn.clicked.connect(self.fillmean)
        self.fill_0_btn.clicked.connect(self.fill0)
        self.scale_btn.clicked.connect(self.scale_value)
        self.scatter_btn.clicked.connect(self.scatter_plot)
        self.plot_btn.clicked.connect(self.line_plot)
        self.train_btn.clicked.connect(self.train_func)

    def fillDetails(self, flag = 1) :
        if flag == 0 :
            self.df = data.read_file(str(self.filePath))

        self.columns.clear()
        self.column_list = data.get_column_list(self.df)
        print(self.column_list)

        for i, j in enumerate(self.column_list) :
            # print(i, j)
            stri = f"{j} ------ {str(self.df[j].dtype)}"
            # print(stri)
            self.columns.insertItem(i, stri)
        
        x , y  = data.get_shape(self.df)
        self.data_shape.setText(f'({x} ,{y})')
        self.fill_combo_box()

    def fill_combo_box(self) :
        self.cat_column.clear()
        self.cat_column.addItems(self.column_list)
        self.drop_column.clear()
        self.drop_column.addItems(self.column_list)
        self.empty_column.clear()
        self.empty_column.addItems(self.column_list)
        self.scatter_x.clear()
        self.scatter_x.addItems(self.column_list)
        self.scatter_y.clear()
        self.scatter_y.addItems(self.column_list)
        self.plot_x.clear()
        self.plot_x.addItems(self.column_list)
        self.plot_y.clear()
        self.plot_y.addItems(self.column_list)


        x = DataFrameModel(self.df)
        self.tabel.setModel(x)

    def get_csv(self) : 
        self.filePath, _ = QFileDialog.getOpenFileName(self, "Open file", "", "csv(*.csv)")
        self.columns.clear()
        # print(self.filePath)
        if self.filePath != "" :
            self.fillDetails(0)

    def target(self):
        self.item = self.columns.currentItem()

    def set_target(self):
        self.target_value = str(self.item.text()).split()[0]
        # print(self.target_value)
        steps.add_code(f"target=data[{self.target_value}]")
        self.target_col.setText(self.target_value)

    def con_cat(self) :

        selected = self.cat_column.currentText()
        # print(selected)
        self.df[selected], func_name = data.convert_category(self.df, selected)
        steps.add_text("Column "+ selected + " converted using LabelEncoder")
        steps.add_pipeline("LabelEncoder", func_name)
        self.fillDetails()

    def dropc(self) :
        selected = self.drop_column.currentText()
        self.df = data.drop_columns(self.df, selected)
        steps.add_code("data=data.drop('"+self.drop_column.currentText()+"',axis=1)")
        steps.add_text("Column "+ self.drop_column.currentText()+ " dropped")
        self.fillDetails()

    def fillmean(self) :
        selected = self.df[self.empty_column.currentText()]
        type = self.df[self.empty_column.currentText()].dtype
        if type != 'object' :
            self.df[self.empty_column.currentText()] = data.fillmean(self.df, self.empty_column.currentText())
            self.fillDetails()
            print("not object")
        else :
            print("datatype is object")
        # print(selected)


    def fill0(self) :
        self.df[self.empty_column.currentText()] = data.fillna(self.df, self.empty_column.currentText())
        self.fillDetails()

    def scale_value(self) :
        if self.scaler.currentText() == "StandardScale" :
            self.df, func_name = data_.StandardScale(self, self.df, self.target_value)
        elif self.scaler.currentText() == "MinMaxScale" :
            self.df, func_name = data_.MinMaxScale(self, self.df, self.target_value)
        elif self.scaler.currentText() == "PowerScale" :
            self.df, func_name = data_.PowerScale(self, self.df, self.target_value)

        steps.add_text(self.scaler.currentText()+" applied to data")
        steps.add_pipeline(self.scaler.currentText(),func_name)
        self.fillDetails()

    def scatter_plot(self) :
        data_.scatter_plot(self, self.df, self.scatter_x.currentText(), self.scatter_y.currentText(), self.colour.currentText(), self.marker.currentText())

    def line_plot(self) :
        data_.line_plot(self, self.df, self.plot_x.currentText(), self.plot_y.currentText(), self.colour_2.currentText(), self.marker_2.currentText())

    def train_func(self) :
        print_success()

if __name__ == "__main__" :
    app = QtWidgets.QApplication(sys.argv)
    window = UI()
    window.show()

    sys.exit(app.exec_())