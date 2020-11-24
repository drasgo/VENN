import sys
from PyQt5 import QtWidgets
import VENN.gui.gui as gui

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    window = gui.MainW()
    window.show()
    window.setWindowOpacity(1)
    sys.exit(app.exec_())
