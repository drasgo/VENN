import gui
import sys
from PyQt5 import QtWidgets


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)

    window = gui.MainW()
    window.show()

    app.exec()
