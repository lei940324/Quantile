echo off

rem 将子目录 GUI 下的MainWindow.ui文件复制到当前目录下，并且编译
copy .\GUI\MainWindow.ui  MainWindow.ui
pyuic5 -o ui_MainWindow.py  MainWindow.ui


rem 编译并复制资源文件
pyrcc5 .\GUI\res.qrc -o res_rc.py


rem 查看数据窗口
copy .\child_GUI\Qtapp\read_data.ui  .\child_GUI\read_data.ui
pyuic5 -o .\child_GUI\ui_read_data.py  .\child_GUI\read_data.ui


rem QVAR窗口
copy .\child_GUI\Qtapp\QVAR.ui  .\child_GUI\QVAR.ui
pyuic5 -o .\child_GUI\ui_QVAR.py  .\child_GUI\QVAR.ui

rem 编译并复制资源文件
pyrcc5 .\child_GUI\Qtapp\icon.qrc -o icon_rc.py