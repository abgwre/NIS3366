import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates
import numpy as np
import datetime
import info
from pandas import to_datetime

class LineChart(QMainWindow):
    def __init__(self, text):
        super().__init__()

        self.t0 = text[1]

        self.setWindowTitle(text[0])
        self.setGeometry(100, 100, 800, 600)

        self.Button = QPushButton('return')
        self.Button.clicked.connect(self.return_to_subwindow)

        self.setupUI(text)



    def setupUI(self, text):
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        layout = QVBoxLayout(self.main_widget)

        self.fig = Figure()

        self.ax1 = self.fig.add_subplot(211)
        self.ax2 = self.fig.add_subplot(212)

        hot_name = text[0]
        plat = text[1].t0[1]
        time = []
        emotion = []
        ranking = []

        for i in info.read_certain_info(hot_name, plat):
            emotion.append(i[1])
            time.append(i[2])
            ranking.append(i[3])

        x = np.array(time)
        y1 = np.array(emotion)
        y2 = np.array(ranking)
        x = to_datetime(x)

        '''x = [datetime.datetime(2022, 1, 1) + datetime.timedelta(days=i) for i in range(10)]
        y = np.random.randint(1, 10, 10)'''

        self.ax1.plot(x, y1)
        self.ax1.set_title('热搜情感趋势', fontproperties='SimHei', fontsize=10)
        self.ax1.set_xticks(self.ax1.get_xticks()[::2])                                             #以2天为单位显示横坐标

        self.ax2.plot(x, y2)
        self.ax2.set_title('热搜排行变化', fontproperties='SimHei', fontsize=10)
        self.ax2.set_xticks(self.ax2.get_xticks()[::2])

        self.ax2.invert_yaxis()
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)

        self.button = QPushButton('返回', self)
        self.button.clicked.connect(self.return_to_subwindow)
        layout.addWidget(self.button)

    def return_to_subwindow(self):
        self.close()
        self.t0.ui.show()
