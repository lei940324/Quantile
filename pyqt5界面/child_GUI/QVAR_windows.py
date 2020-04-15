# -*- coding: utf-8 -*-

import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import pyqtSlot
from func import Quantile_Granger

##from PyQt5.QtCore import  pyqtSlot,pyqtSignal,Qt

# from PyQt5.QtWidgets import

# from PyQt5.QtGui import

# from PyQt5.QtSql import

# from PyQt5.QtMultimedia import

# from PyQt5.QtMultimediaWidgets import


from pyqt5界面.child_GUI.ui_QVAR import Ui_QVAR


class QVAR(QMainWindow):

    def __init__(self, QVARdata, parent=None):
        super().__init__(parent)   # 调用父类构造函数，创建窗体
        self.QVARdata = QVARdata

        self.ui = Ui_QVAR()          # 创建UI对象
        self.ui.setupUi(self)      # 构造UI界面
        self.resize(400, 300)

        self.quantile = [self.ui.doubleSpinBox, self.ui.doubleSpinBox_2, self.ui.doubleSpinBox_3, self.ui.doubleSpinBox_4, self.ui.doubleSpinBox_5, self.ui.doubleSpinBox_6, self.ui.doubleSpinBox_7,
                         self.ui.doubleSpinBox_8, self.ui.doubleSpinBox_9, self.ui.doubleSpinBox_10]
        self.init_parameter()

# ==============自定义功能函数========================
    def init_parameter(self):
        # 初始化各参数
        for widget in self.quantile[5:]:   # 后五个默认不可见
            widget.setVisible(False)
        for widget in self.quantile:   # 设置步长
            widget.setSingleStep(0.05)
        self.ui.doubleSpinBox.setValue(0.1)
        self.ui.doubleSpinBox_2.setValue(0.25)
        self.ui.doubleSpinBox_3.setValue(0.5)
        self.ui.doubleSpinBox_4.setValue(0.75)
        self.ui.doubleSpinBox_5.setValue(0.9)
        self.ui.spinBox.setValue(1)
        self.ui.spinBox_2.setValue(1)

# ==========由connectSlotsByName()自动连接的槽函数============
    @pyqtSlot()
    def on_pushButton_clicked(self):   # 添加按钮
        for widget in self.quantile:
            if not widget.isVisible():
                widget.setVisible(True)
                break

    @pyqtSlot()
    def on_pushButton_2_clicked(self):   # 减少按钮
        for widget in self.quantile[::-1]:
            if widget.isVisible():
                widget.setValue(0)
                widget.setVisible(False)
                break

    @pyqtSlot()
    def on_pushButton_3_clicked(self):   # 开始运行按钮
        Granger = Quantile_Granger()
        # 获取参数
        p = self.ui.spinBox.value()
        q = self.ui.spinBox_2.value()
        quantiles = [x.value() for x in self.quantile if x.value() != 0]
        for key in self.QVARdata:
            relation = key
            X = self.QVARdata[key].iloc[:, 0]
            Y = self.QVARdata[key].iloc[:, 1]
            data = Granger.lag_list(Y, X, p, q)
            print(data)


        # ============窗体测试程序 ================================
if __name__ == "__main__":  # 用于当前窗体测试
    import pandas as pd
    df = pd.read_excel(r'..\data\测试数据.xlsx')
    df = df.drop(df.columns[0], axis=1)

    app = QApplication(sys.argv)  # 创建GUI应用程序
    form = QVAR(df)  # 创建窗体
    form.show()
    sys.exit(app.exec_())
