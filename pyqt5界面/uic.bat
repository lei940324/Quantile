echo off

rem ����Ŀ¼ GUI �µ�MainWindow.ui�ļ����Ƶ���ǰĿ¼�£����ұ���
copy .\GUI\MainWindow.ui  MainWindow.ui
pyuic5 -o ui_MainWindow.py  MainWindow.ui


rem ���벢������Դ�ļ�
pyrcc5 .\GUI\res.qrc -o res_rc.py


rem �鿴���ݴ���
copy .\child_GUI\Qtapp\read_data.ui  .\child_GUI\read_data.ui
pyuic5 -o .\child_GUI\ui_read_data.py  .\child_GUI\read_data.ui


rem QVAR����
copy .\child_GUI\Qtapp\QVAR.ui  .\child_GUI\QVAR.ui
pyuic5 -o .\child_GUI\ui_QVAR.py  .\child_GUI\QVAR.ui

rem ���벢������Դ�ļ�
pyrcc5 .\child_GUI\Qtapp\icon.qrc -o icon_rc.py