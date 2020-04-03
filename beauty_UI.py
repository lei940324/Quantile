from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette

def beauty(obj):
    obj.setWindowOpacity(0.9) # 设置窗口透明度
    # obj.setWindowFlag(QtCore.Qt.FramelessWindowHint) # 隐藏边框
    # 美化界面
    edit_style = '''
        QWidget{
            width:100px;
            border-radius:10px;
            padding:2px 4px;
        }
        '''
    obj.setStyleSheet(edit_style)
    
    # 设置圆形按钮
    obj.ui.pushButton_2.setStyleSheet('''QPushButton{background:#F76677;border-radius:5px;}
QPushButton:hover{background:red;}''')
    obj.ui.pushButton_3.setStyleSheet('''QPushButton{background:#F7D674;border-radius:5px;}
QPushButton:hover{background:yellow;}''')
    obj.ui.pushButton_4.setStyleSheet('''QPushButton{background:#6DDF6D;border-radius:5px;}
QPushButton:hover{background:green;}''')

    # 设置生成区间按钮
    obj.ui.pushButton.setStyleSheet('''QPushButton{border:1px solid gray;border-radius:5px}''')




