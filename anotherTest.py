from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag
from PyQt5 import QtGui
from PyQt5 import QtCore

import sys

from mainwindow import Ui_MainWindow


class SingleEvents:

    def dragEnterMainStruct(event):
        event.accept()

    def dragMoveMainStruct(event, obj):
        position = event.pos()
        
        obj.move(position)
        event.setDropAction(Qt.MoveAction)
        event.accept()

    def dropMainStruct(caller, event, obj):
        if obj.objectName() == "Blocks":
            global posit
            print("in drop first block")

            global nBlocks
            print("in dropmainstruct " + obj.objectName())
            position = event.pos()
            newBlock = StructBlock(caller, str(nBlocks) + "block", obj)
            print("creato nuovo blocco")
            newBlock.move(position - QtCore.QPoint(newBlock.width() / 2, newBlock.height() / 2))
            newBlock.show()
            layers.append(newBlock)
            nBlocks = nBlocks + 1
        else:
            posit = event.pos() - QtCore.QPoint(obj.width() / 2, obj.height() / 2)
            print(str(posit))

        obj.move(posit)
        event.setDropAction(Qt.MoveAction)
        event.accept()

    def mouseMove(event, parent):
        mimeData = QMimeData()
        drag = QDrag(parent)
        drag.setMimeData(mimeData)
        drag.setHotSpot(event.pos())

        dropAction = drag.exec_(Qt.MoveAction)

    def mousePress(caller):
        print("in mopuse press " + caller.objectName() + " " + str(QtCore.QPoint(1,     1)))
        global posit
        posit = caller.pos()
        print(str(posit))


class TextInStructBox(QtWidgets.QLineEdit):
    defaultText = "** "

    def __init__(self, parent, text=defaultText):
        self.text = text
        self.setAccessibleName(self.text)
        super().__init__(self.defaultText + self.text, parent)
        self.setEnabled(False)
        self.setAlignment(Qt.AlignCenter)
        self.show()

    def mousePressEvent(self, e):
        if e.button() == Qt.RightButton and self.accessibleName() == "Neurons":
            self.setEnabled(True)

    def keyPressEvent(self, e):
        print("in key press event")
        if e.key() == Qt.Key_Return:
            self.setEnabled(False)
            print(" key press event dopo if")


class StructBlock(QtWidgets.QFrame):

    def __init__(self, parent, name, MainBlock):
        self.parent = parent
        self.name = name
        QtWidgets.QWidget.__init__(self, parent=parent)
        self.setAccessibleName(self.name)
        self.setStyleSheet(MainBlock.styleSheet())
        # self.setStyleSheet("background-color: rgb(50, 50, 50);")
        self.layout = QtWidgets.QVBoxLayout(self)

        self.setFixedWidth(MainBlock.width())
        self.setFixedHeight(MainBlock.height())
        # self.setGeometry(MainBlock.geometry())
        print("in creazione struct block: " + str(self.accessibleName()) + " " + str(MainBlock.height()) + " " + str(MainBlock.width()) + " block stylesheet " + str(MainBlock.styleSheet()))
        print("dimensioni nuovo blocco " + str(self.width()) + " " + str(self.height()) + " stylesheet " + str(self.styleSheet()))
        self.layer = TextInStructBox(self, "Layer")
        self.neurons = TextInStructBox(self, "Neurons")
        # self.view = QtWidgets.QGraphicsView
        self.layout.addWidget(self.layer)
        self.layout.addWidget(self.neurons)

        self.show()

    def mousePressEvent(self, e):
    #     if e.button() == Qt.LeftButton:
    #         self.neurons.setEnabled(True)

        if e.button() == Qt.LeftButton:
            print("moving")

    def mouseMoveEvent(self, e):
        if e.button() == Qt.LeftButton:
            print("in mousemoveevent nuovo blocco")
            SingleEvents.mouseMove(e, self.parent)
    #
    # def keyPressEvent(self, e):
    #     print("in key press event")
    #     if e.key() == Qt.Key_Return and self.neurons.isEnabled():
    #         self.neurons.setEnabled(False)
    #         print(" key press event dopo if")


class MainW(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MainW, self).__init__()
        self.setupUi(self)

        self.Blocks.mouseMoveEvent = lambda event: SingleEvents.mouseMove(event, self.MainStruct)
        self.Blocks.mousePressEvent = SingleEvents.mousePress(self.Blocks)

        self.MainStruct.setAcceptDrops(True)
        self.MainStruct.dragEnterEvent = lambda event: SingleEvents.dragEnterMainStruct(event)
        self.MainStruct.dragMoveEvent = lambda event: SingleEvents.dragMoveMainStruct(event, self.Blocks)
        self.MainStruct.dropEvent = lambda event: SingleEvents.dropMainStruct(self.MainStruct, event, self.Blocks)


global posit
posit = None
global nBlocks
nBlocks = 0
layers = []

app = QtWidgets.QApplication(sys.argv)

window = MainW()

window.show()

app.exec()
