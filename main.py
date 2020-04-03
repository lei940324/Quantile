# -*- coding: utf-8 -*-

import sys
import pandas as pd
from func import Quantile_Granger, logging
import func

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QThread

from beauty_UI import beauty
from ui_MainWindow import Ui_MainWindow
from child_GUI.read_windows import read_Window
from child_GUI.QVAR_windows import QVAR

# 继承QThread


class Runthread(QThread):
    #  通过类成员对象定义信号对象
    _signal = pyqtSignal(str)

    def __init__(self, form):
        super(Runthread, self).__init__()
        self.form = form

    def __del__(self):
        self.wait()

    def run(self):
        form = self.form
        # 加载参数
        start = form.ui.doubleSpinBox.value()   # 区间起点
        end = form.ui.doubleSpinBox_2.value()   # 区间终点
        num = form.ui.spinBox.value()   # 区间个数
        sign = form.ui.comboBox_2.currentText()   # 模式选择
        max_lag = int(form.ui.comboBox.currentText())   # 最大滞后阶数选择，默认为5
        info_type = form.ui.comboBox_3.currentText()   # 信息准则选择
        WaldNum = form.ui.spinBox_3.value()   # 估计wald个数，默认1000个
        sign_num = int(form.ui.comboBox_4.currentText())   # 有效数字，默认为3
        AicNum = form.ui.spinBox_2.value()   # 估计各区间最优滞后阶数，默认50个
        # 开始计算
        qrange, qr_name = form.func.set_range(start, end, num)
        DataList = form.func.pattern(form.df, sign)
        INFO = [self._signal.emit]
        if form.ui.checkBox_2.isChecked():
            INFO.append(logging.info)
        form.func.calculate(DataList, qrange, qr_name,
                            max_lag, info_type, WaldNum, sign_num, AicNum, objects=INFO)


class QmyMainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)         # 调用父类构造函数，创建窗体
        self.ui = Ui_MainWindow()          # 创建UI对象
        self.ui.setupUi(self)            # 构造UI界面
        self.resize(700, 700)

        beauty(self)                     # 美化界面
        self.func = Quantile_Granger()   # 导入主函数
        self.init_parameter()            # 初始化各参数
        # 默认导入测试数据
        self.df = pd.read_excel(r'.\data\测试数据.xlsx')
        self.df = self.df.drop(self.df.columns[0], axis=1)

# ==============自定义功能函数========================
    def init_parameter(self):
        '''
        初始化各参数
        '''
        self.ui.doubleSpinBox.setValue(0.1)   # 区间起点为0.1
        self.ui.doubleSpinBox.setSingleStep(0.01)
        self.ui.doubleSpinBox_2.setValue(0.9)   # 区间终点为0.9
        self.ui.doubleSpinBox_2.setSingleStep(0.01)
        self.ui.spinBox.setValue(17)   # 个数默认为17个
        self.ui.spinBox_2.setValue(30)   # 滞后估计数默认30个
        self.ui.spinBox_3.setMinimum(10)
        self.ui.spinBox_3.setMaximum(1500)  # 设置上界
        self.ui.spinBox_3.setValue(1000)   # 设置估计wald的个数为1000
        self.ui.textEdit.setText(
            ' '*20+'使用说明:\n1.点击导入数据按钮加载xlsx数据；\n2.进行参数设定，具体参数信息请参见README.md文件；\n3.点击开始运行按钮，程序开始计算')
        self.ui.lineEdit.setText(
            '[0.10-0.15]、[0.15-0.20]...[0.50-0.55]...[0.80-0.85]、[0.85-0.90]')
        self.ui.checkBox.setChecked(True)   # 勾选日期
        self.ui.checkBox_2.setChecked(True)   # 勾选日志
        self.ui.comboBox_4.setCurrentIndex(3)   # 设置默认保留三位小数
        self.ui.comboBox.setCurrentIndex(4)   # 最大阶数默认为5
        self.ui.comboBox_3.setCurrentIndex(1)   # 信息准则默认为BIC
        self.ui.comboBox_2.setCurrentIndex(0)   # 模式设定默认为1

    def call_backlog(self, msg):
        self.ui.textEdit.append(msg)  # 将线程的参数传入


# =============================================================================
#    # 当把边框给隐藏掉，边框将无法拖动移动，这个可以通过重写函数来实现。
#    def mousePressEvent(self, event):
#       if event.button()==QtCore.Qt.LeftButton:
#          self.m_flag=True
#          self.m_Position=event.globalPos()-self.pos() #获取鼠标相对窗口的位置
#          event.accept()
#          self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))  #更改鼠标图标
#
#    def mouseMoveEvent(self, QMouseEvent):
#       if QtCore.Qt.LeftButton and self.m_flag:
#          self.move(QMouseEvent.globalPos()-self.m_Position)#更改窗口位置
#          QMouseEvent.accept()
#
#    def mouseReleaseEvent(self, QMouseEvent):
#       self.m_flag=False
#       self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
# =============================================================================

# ==========由connectSlotsByName()自动连接的槽函数============
    @pyqtSlot()
    def on_action_triggered(self):  # 导入数据按钮
        download_path = QFileDialog.getOpenFileName(None, "浏览", None,
                                                    "Text Files (*.xlsx);;Text Files (*.xls)")
        try:
            self.df = pd.read_excel(download_path[0])
            self.ui.textEdit.setText("\n    恭喜,数据读取成功!")
            if self.ui.checkBox.isChecked():
                # 判断date是否勾选，如果勾选，删除第一列日期数据
                self.df = self.df.drop(self.df.columns[0], axis=1)
        except:
            self.ui.textEdit.setText("\n    数据读取失败,请重新导入数据!")

    @pyqtSlot()
    def on_action_2_triggered(self):   # 开始运行按钮
        func.EXIT = False
        self.ui.textEdit.setText('')
        # 创建线程
        self.thread = Runthread(self)
        # 连接信号
        self.thread._signal.connect(self.call_backlog)  # 进程连接回传到GUI的事件
        # 开始线程
        self.thread.start()

    @pyqtSlot()
    def on_action_4_triggered(self):   # 初始化按钮
        self.init_parameter()
        self.ui.textEdit.setText(
            ' '*20+'使用说明:\n1.点击导入数据按钮加载xlsx数据；\n2.进行参数设定，具体参数信息请参见README.md文件；\n3.点击开始运行按钮，程序开始计算\n\n     初始化成功！')

    @pyqtSlot()
    def on_action_3_triggered(self):   # 最小化按钮
        self.showMinimized()

    @pyqtSlot()
    def on_action_5_triggered(self):   # 终止运行按钮
        func.EXIT = True

    @pyqtSlot()
    def on_pushButton_clicked(self):   # 生成区间按钮
        start = self.ui.doubleSpinBox.value()   # 区间起点
        end = self.ui.doubleSpinBox_2.value()   # 区间终点
        num = self.ui.spinBox.value()   # 区间个数
        _, qr_name = self.func.set_range(start, end, num)
        if len(qr_name) > 5:
            display = f"{qr_name[0]}、{qr_name[1]}...{qr_name[int(len(qr_name)/2)]}...{qr_name[-2]}、{qr_name[-1]}"
        else:
            display = '、'.join(qr_name)
        self.ui.lineEdit.setText(display)

    @pyqtSlot()
    def on_action_6_triggered(self):   # 查看数据
        read = read_Window(self)
        read.display(self.df)
        read.show()

    @pyqtSlot()
    def on_actionQVAR_triggered(self):   # QVAR估计
        QVARdata = self.func.pattern(self.df, self.ui.comboBox_2.currentText())
        QVAR_win = QVAR(QVARdata, self)
        QVAR_win.show()


# ============窗体测试程序 ================================
if __name__ == "__main__":
    app = QApplication(sys.argv)    # 创建GUI应用程序
    form = QmyMainWindow()          # 创建窗体
    form.show()
    sys.exit(app.exec_())
