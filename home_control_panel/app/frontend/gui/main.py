from PyQt5 import QtWidgets

from gui.login_dialog import Ui_Login
from gui.main_window import Ui_MainWindow  # importing our generated file
import sys


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def open_dialog(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = Ui_Login()
        dialog.ui.setupUi(dialog)
        dialog.ui.progressBar.hide()
        dialog.exec_()
        dialog.show()
        return dialog


app = QtWidgets.QApplication([])
app.setStyle('Fusion')
application = MainWindow()
application.show()
application.open_dialog()
sys.exit(app.exec())
