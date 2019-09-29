import sys
from PyQt5.QtWidgets import QMainWindow,QPushButton, QApplication
from PyQt5.QtCore import QSize, Qt, QLine, QPoint
from PyQt5.QtGui import QPainter, QPen

global i
i = 0

class NewLine(QLine):

    def __init__(self, point):
        QLine.__init__(self)
        global i
        self.setPoints(QPoint(0,i), point)
        i = i + 5

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(300, 300))
        self.line = None
        pybutton = QPushButton('button', self)
        pybutton.clicked.connect(self.draw_line)
        pybutton.resize(100,100)
        pybutton.move(100, 100)

    def draw_line(self):
        button = self.sender()
        self.line = NewLine(button.pos())
        self.update()

    def paintEvent(self,event):
        QMainWindow.paintEvent(self, event)
        if not self.line is None:
            painter = QPainter(self)
            pen = QPen(Qt.red, 3)
            painter.setPen(pen)
            painter.drawLine(self.line)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())