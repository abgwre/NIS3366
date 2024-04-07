import info
import sys
import pymysql
from PySide2.QtWidgets import QApplication, QMessageBox, QWidget, QShortcut, QSizePolicy, QListView, QVBoxLayout, \
    QComboBox, QPushButton
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, Qt, QStringListModel

from PySide2.QtGui import QPixmap, QIcon
from func_timeout import func_set_timeout

class Window(QWidget):

    def __init__(self, t):                                                                             #界面初始化

        super().__init__(t[0])
        self.s = None
        self.t0 = t
        qfile_stats = QFile("subwindow.ui")                                                             #加载dt designer制作的界面
        qfile_stats.open(QFile.ReadOnly)
        qfile_stats.close()

        self.clear = 0

        self.ui = QUiLoader().load(qfile_stats)

        self.list = []


        # 创建一个封装列表的数据源
        listmodel = QStringListModel()
        for i in info.read_hot_now(t[1]):
            text = str(i[3]) + ' ' + i[0]
            self.list.append(text)

        listmodel.setStringList(self.list)
        self.ui.hotview.setModel(listmodel)

        self.ui.hotview.doubleClicked.connect(self.clicked)
        self.ui.search.clicked.connect(lambda: self.plot([self.ui.SearchBox.currentText(), self]))
        self.ui.renew.clicked.connect(lambda: self.renew(t[1]))
        self.ui.ButtonReturn.clicked.connect(self.return_to_mainwindow)


        '''self.ui.setFixedWidth(900)
        self.ui.setFixedHeight(600)

        self.ui.ButtonWB.clicked.connect(lambda: self.Input('0'))   '''                                #计算器输入字符按键

    '''        self.ui.ActionGame.triggered.connect(self.Play)                                             #打开速算练习界面
        self.ui.ActionQuit.triggered.connect(self.Quit)'''
    def clicked(self, item):
        # self, 弹框名称， 弹框内容
        #QMessageBox.information(self, "QListView", "选择了" + self.list[item.row()])
        text = self.list[item.row()]
        text = text[2:]
        text = [text, self]
        self.plot(text)


    def plot(self, text):
        conn = pymysql.connect(host='172.29.25.151', port=3307, user='root', password='123456', database='nis',
                               charset='utf8')

        cur = conn.cursor()

        sql_exist = "SELECT EXISTS(SELECT * FROM hot WHERE name = %s);"

        cur.execute(sql_exist, text[0])

        fetch = cur.fetchone()

        conn.close()

        if fetch[0] == 0:  # 更新数据
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("热搜不存在")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        else:
            import plotwindow
            self.ui.hide()
            self.s = plotwindow.LineChart(text)
            self.s.show()

    def renew(self, plat):
        search_list = []

        text = self.ui.SearchBox.currentText()

        if text == '':
            return

        for i in info.select_hot_name(text, plat):
            if i[0] not in search_list:
                search_list.append(i[0])
        self.ui.SearchBox.clear()
        self.ui.SearchBox.addItems(search_list)
        self.ui.SearchBox.setCurrentText(text)

    def return_to_mainwindow(self):
        self.ui.close()
        self.t0[0].ui.show()
