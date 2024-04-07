import time, func_timeout
from PySide2.QtWidgets import QApplication, QMessageBox, QWidget, QShortcut, QSizePolicy
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, Qt
from PySide2.QtGui import QPixmap
from func_timeout import func_set_timeout

class MainMenu(QWidget):

    def __init__(self):                                                                             #界面初始化

        super().__init__()
        self.s = None
        qfile_stats = QFile("mainwindow.ui")                                                             #加载dt designer制作的界面
        qfile_stats.open(QFile.ReadOnly)
        qfile_stats.close()

        self.clear = 0

        self.ui = QUiLoader().load(qfile_stats)

        #self.ui.setWindowTitle("Calculator")

        self.ui.setFixedWidth(900)
        self.ui.setFixedHeight(600)

        self.ui.ButtonWB.clicked.connect(lambda: self.Sub('wb'))                                   #计算器输入字符按键
        self.ui.ButtonZhiHu.clicked.connect(lambda: self.Sub('zh'))
        self.ui.ButtonDaily.clicked.connect(lambda: self.Sub('daily'))
    '''        self.ui.ActionGame.triggered.connect(self.Play)                                             #打开速算练习界面
        self.ui.ActionQuit.triggered.connect(self.Quit)
    '''

    def Sub(self, plat):
        import subwindow
        self.ui.hide()
        t = [self, plat]
        self.s = subwindow.Window(t)
        self.s.ui.show()

