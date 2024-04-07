import info
from comment1 import read
import sys
import pymysql
from PySide2.QtWidgets import QApplication, QMessageBox, QWidget, QShortcut, QSizePolicy, QListView, QVBoxLayout, \
    QComboBox, QPushButton
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile, Qt, QStringListModel

from PySide2.QtGui import QPixmap, QIcon
from func_timeout import func_set_timeout

class Window(QWidget):

    def __init__(self, t):

        super().__init__(t[0])
        self.s = None
        self.t0 = t
        qfile_stats = QFile("subwindow.ui")                                                             #加载dt designer制作的界面
        qfile_stats.open(QFile.ReadOnly)
        qfile_stats.close()

        self.clear = 0

        self.ui = QUiLoader().load(qfile_stats)

        self.ui.setGeometry(100, 100, 800, 600)

        self.list = []

        Time = '2024-04-07 13_59_33'
        filename = '热搜' + Time + '.csv'
        read(filename, Time)

        # 创建一个封装列表的数据源
        listmodel = QStringListModel()
        for i in info.read_hot_now(t[1]):                                                               #加载当前热搜
            text = str(i[3]) + ' ' + i[0]
            self.list.append(text)

        listmodel.setStringList(self.list)
        self.ui.hotview.setModel(listmodel)

        self.ui.hotview.doubleClicked.connect(self.clicked)                                             #双击当前热搜进行分析
        self.ui.search.clicked.connect(lambda: self.plot([self.ui.SearchBox.currentText(), self]))      #根据搜索框中热搜进行分析
        self.ui.renew.clicked.connect(lambda: self.renew(t[1]))                                         #更新搜索框中内容
        self.ui.ButtonReturn.clicked.connect(self.return_to_mainwindow)
        self.ui.rescan.clicked.connect(self.rescan)

    def clicked(self, item):
        #QMessageBox.information(self, "QListView", "选择了" + self.list[item.row()])
        text = self.list[item.row()]
        text = text[2:]                                                                                 #传递热搜名
        text = [text, self]
        self.plot(text)


    def plot(self, text):
        conn = pymysql.connect(host='172.29.25.151', port=3307, user='root', password='123456', database='nis',
                               charset='utf8')

        cur = conn.cursor()

        sql_exist = "SELECT EXISTS(SELECT * FROM hot WHERE name = %s);"                                 #判断搜索框中热搜是否存在

        cur.execute(sql_exist, text[0])

        fetch = cur.fetchone()

        conn.close()

        if fetch[0] == 0:                                                                               #更新数据
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("热搜不存在")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        else:
            import plotwindow
            self.ui.hide()
            self.s = plotwindow.LineChart(text)                                                         #打开作图窗口绘制趋势图
            self.s.show()

    def renew(self, plat):
        search_list = []

        text = self.ui.SearchBox.currentText()

        if text == '':
            return

        for i in info.select_hot_name(text, plat):                                                      #通过模糊查询获取相关热搜
            if i[0] not in search_list:
                search_list.append(i[0])
        self.ui.SearchBox.clear()
        self.ui.SearchBox.addItems(search_list)
        self.ui.SearchBox.setCurrentText(text)

    def return_to_mainwindow(self):
        self.ui.close()
        self.t0[0].ui.show()

    def rescan(self):
        read('热搜2024-04-07 13_59_33.csv')
