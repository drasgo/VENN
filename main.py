import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow

import VENN.gui.gui as gui


class MW(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

if __name__ == '__main__':
    # try:
    app = QtWidgets.QApplication(sys.argv)
    window = gui.MainW()
    window.show()

    sys.exit(app.exec_())
    # except (Exception, KeyboardInterrupt) as exc:
    #     print(exc)
    #     quit()
