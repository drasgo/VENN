import sys
from PyQt5.QtWidgets import QMainWindow,QPushButton, QApplication
from PyQt5.QtCore import QSize, Qt, QLine, QPoint
from PyQt5.QtGui import QPainter, QPen

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(300, 300))

        pybutton = QPushButton('button', self)
        pybutton.clicked.connect(self.draw_line)
        pybutton.resize(100,100)
        pybutton.move(100, 100)
        self.line = QLine()

    def draw_line(self):
        button = self.sender()
        self.line = QLine(QPoint(), button.pos())
        self.update()

    def paintEvent(self,event):
        QMainWindow.paintEvent(self, event)
        if not self.line.isNull():
            painter = QPainter(self)
            pen = QPen(Qt.red, 3)
            painter.setPen(pen)
            painter.drawLine(self.line)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())