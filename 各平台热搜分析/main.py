import menu

app = menu.QApplication([])
stats = menu.MainMenu()
stats.ui.show()
app.exec_()