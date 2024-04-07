import time, func_timeout
from PySide2.QtWidgets import QApplication, QMessageBox, QWidget, QShortcut, QSizePolicy
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, Qt
from PySide2.QtGui import QPixmap
from func_timeout import func_set_timeout

class MainWindow(QWidget):

    def __init__(self):

        super().__init__()
        self.s = None
        qfile_stats = QFile("mainwindow.ui")                                                    #加载dt designer制作的界面
        qfile_stats.open(QFile.ReadOnly)
        qfile_stats.close()

        self.clear = 0

        self.ui = QUiLoader().load(qfile_stats)

        self.ui.setGeometry(100, 100, 800, 600)

        #self.ui.setWindowTitle("Calculator")

        self.ui.setFixedWidth(900)
        self.ui.setFixedHeight(600)

        self.ui.ButtonWB.clicked.connect(lambda: self.Sub('微博'))                                #显示不同平台热搜
        self.ui.ButtonZhiHu.clicked.connect(lambda: self.Sub('知乎'))
        self.ui.ButtonDaily.clicked.connect(lambda: self.Sub('今日头条'))

    def Sub(self, plat):                                                                        #打开子界面
        import subwindow
        self.ui.hide()
        t = [self, plat]
        self.s = subwindow.Window(t)
        self.s.ui.show()

