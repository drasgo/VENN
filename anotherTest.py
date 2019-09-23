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

    def dragMoveMainStruct(event):
        global tempBlock
        position = event.pos()
        # obj = event.source()
        # print("in dragmoveevent " + tempBlock.accessibleName())
        tempBlock.move(position)
        event.setDropAction(Qt.MoveAction)
        event.accept()

    def dropMainStruct(self, event, parent):
        global tempBlock

        if tempBlock.objectName() == "Blocks":
            global posit
            # print("in drop first block")

            global nBlocks
            # print("in dropmainstruct " + tempBlock.objectName())
            position = event.pos()
            newBlock = StructBlock(self, str(nBlocks) + "block", tempBlock)
            # print("creato nuovo blocco")
            newBlock.move(position - QtCore.QPoint(newBlock.width() / 2, newBlock.height() / 2))
            newBlock.show()
            layers.append(newBlock)
            nBlocks = nBlocks + 1
        else:
            posit = event.pos() - QtCore.QPoint(tempBlock.width() / 2, tempBlock.height() / 2)
            # print(str(posit))

        tempBlock.move(posit)
        event.setDropAction(Qt.MoveAction)
        event.accept()
        tempBlock = None

        if len(layers) != 0:
            parent.InsertFirstBlock.hide()

    def mouseMove(event, parent):
        mimeData = QMimeData()

        drag = QDrag(parent)
        drag.setMimeData(mimeData)
        drag.setHotSpot(event.pos())

        dropAction = drag.exec_(Qt.MoveAction)

    def mousePress(caller):
        # print("in mopuse press " + caller.objectName() + " " + str(QtCore.QPoint(1,     1)))
        global posit
        posit = caller.pos()
        global tempBlock
        tempBlock = caller
        # print(str(posit))


class TextInStructBox(QtWidgets.QLineEdit):
    defaultText = "** "

    def __init__(self, parent, text=defaultText):
        self.text = text
        super().__init__(self.defaultText + self.text, parent)

        self.setAccessibleName(self.text)
        self.setEnabled(False)
        self.setAlignment(Qt.AlignCenter)
        self.show()
    #
    # def mousePressEvent(self, e):
    #     print("in mousepressevent di " + self.accessibleName())
    #     if e.button() == Qt.RightButton and self.accessibleName() == "Neurons":
    #         self.setEnabled(True)
    #
    # def keyPressEvent(self, e):
    #     print("in key press event")
    #     if e.key() == Qt.Key_Return:
    #         self.setEnabled(False)
    #         print(" key press event dopo if")


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
        # print("in creazione struct block: " + str(self.accessibleName()) + " " + str(MainBlock.height()) + " " + str(MainBlock.width()) + " block stylesheet " + str(MainBlock.styleSheet()))
        # print("dimensioni nuovo blocco " + str(self.width()) + " " + str(self.height()) + " stylesheet " + str(self.styleSheet()))
        self.layer = TextInStructBox(self, "Layer")
        self.neurons = TextInStructBox(self, "Neurons")
        # self.view = QtWidgets.QGraphicsView
        self.layout.addWidget(self.layer)
        self.layout.addWidget(self.neurons)

        self.show()

    def mousePressEvent(self, e):
        if e.button() == Qt.RightButton or (e.type() == QtCore.QEvent.MouseButtonDblClick and e.buttons() == Qt.LeftButton):
            self.neurons.setEnabled(True)

        if e.buttons() == Qt.LeftButton:
            # print("moving")
            global tempBlock
            tempBlock = self

    def mouseMoveEvent(self, e):
        # print("in moousemoveevent nuovo blocco " + str(e.button()))
        if e.buttons() != Qt.LeftButton or (e.type() == QtCore.QEvent.MouseButtonDblClick and e.buttons() == Qt.LeftButton):
            return
        # print("in mousemoveevent nuovo blocco dopo if")
        SingleEvents.mouseMove(e, self.parent)

    def keyPressEvent(self, e):
        # print("in key press event")
        if e.key() == Qt.Key_Return and self.neurons.isEnabled():
            self.neurons.setEnabled(False)
            # print(" key press event dopo if")


class MainW(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MainW, self).__init__()
        self.setupUi(self)

        self.Blocks.mouseMoveEvent = lambda event: SingleEvents.mouseMove(event, self.MainStruct)
        self.Blocks.mousePressEvent = lambda event: SingleEvents.mousePress(self.Blocks)
        self.Blocks.setAccessibleName("Blocks")

        self.MainStruct.setAcceptDrops(True)
        self.MainStruct.dragEnterEvent = lambda event: SingleEvents.dragEnterMainStruct(event)
        self.MainStruct.dragMoveEvent = lambda event: SingleEvents.dragMoveMainStruct(event)
        self.MainStruct.dropEvent = lambda event: SingleEvents.dropMainStruct(self.MainStruct, event, self)

global posit
posit = None
global nBlocks
nBlocks = 0
global tempBlock
tempBlock = None
layers = []

app = QtWidgets.QApplication(sys.argv)

window = MainW()

window.show()

app.exec()
