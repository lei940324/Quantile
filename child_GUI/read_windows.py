# -*- coding: utf-8 -*-

import sys
import numpy as np
from PyQt5.QtWidgets import  QApplication, QMainWindow, QTableWidgetItem
from PyQt5.QtCore import Qt

##from PyQt5.QtCore import  pyqtSlot,pyqtSignal,Qt

##from PyQt5.QtWidgets import  

##from PyQt5.QtGui import

##from PyQt5.QtSql import 

##from PyQt5.QtMultimedia import

##from PyQt5.QtMultimediaWidgets import


from child_GUI.ui_read_data import Ui_MainWindow
# from ui_read_data import Ui_MainWindow

class read_Window(QMainWindow): 

   def __init__(self, parent=None):
      super().__init__(parent)   # 调用父类构造函数，创建窗体
      self.ui=Ui_MainWindow()    # 创建UI对象
      self.ui.setupUi(self)      # 构造UI界面
      self.setGeometry(400, 150, 700, 600)

##  ==============自定义功能函数========================
   def display(self, input_table):
      self.ui.tableWidget.setAlternatingRowColors(True)  # 设置交替行背景颜色
      ###===========读取表格，转换表格，===========================================
      input_table_rows = input_table.shape[0]
      input_table_colunms = input_table.shape[1]
      input_table_header = input_table.columns.values.tolist()

      ###===========读取表格，转换表格，============================================
      ###======================给tablewidget设置行列表头============================

      self.ui.tableWidget.setColumnCount(input_table_colunms)
      self.ui.tableWidget.setRowCount(input_table_rows)
      self.ui.tableWidget.setHorizontalHeaderLabels(input_table_header)

      ###================遍历表格每个元素，同时添加到tablewidget中========================
      for i in range(input_table_rows):
            input_table_rows_values = input_table.iloc[[i]]
            input_table_rows_values_array = np.array(input_table_rows_values)
            input_table_rows_values_list = input_table_rows_values_array.tolist()[0]
            for j in range(input_table_colunms):
               input_table_items_list = input_table_rows_values_list[j]

               ###==============将遍历的元素添加到tablewidget中并显示=======================

               input_table_items = str(input_table_items_list)
               newItem = QTableWidgetItem(input_table_items)
               newItem.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
               self.ui.tableWidget.setItem(i, j, newItem)


##  ==============event处理函数==========================
        
        
##  ==========由connectSlotsByName()自动连接的槽函数============        
        
        
##  =============自定义槽函数===============================        


   
##  ============窗体测试程序 ================================
if  __name__ == "__main__":        #用于当前窗体测试

   import pandas as pd
   df = pd.read_excel(r'..\data\测试数据.xlsx')
   df = df.drop(df.columns[0], axis=1)


   app = QApplication(sys.argv)    #创建GUI应用程序
   form=read_Window()            #创建窗体
   form.display(df)
   form.show()
   sys.exit(app.exec_())
