import menu

app = menu.QApplication([])
stats = menu.MainWindow()
stats.ui.show()
app.exec_()