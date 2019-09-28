from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag
from PyQt5 import QtGui
from PyQt5 import QtCore
# from PyQt5.QtCore import QTimer
import sys
# import threading, time, random

from mainwindow import Ui_MainWindow


blockSelected = "background-color: black;"
blockUnSelected = "background-color: rgb(114, 159, 207);"


def CheckMultipleSelection(self):
    for widget in self.findChildren(QtWidgets.QFrame):
        if widget.geometry() in MultipleSelect[0].geometry() and widget.objectName() != "Blocks":
            SelectBlock(widget)
        else:
            UnselectBlock(widget)


def SelectBlock(widget):
    widget.setStyleSheet(blockSelected)
    if widget not in selectedMultipleLayer:
        selectedMultipleLayer.append(widget)


def UnselectBlock(wid=None):
    if wid is None:
        for widget in selectedMultipleLayer:
            widget.setStyleSheet(blockUnSelected)
            if widget.isSelected():
                widget.unselect()
        selectedMultipleLayer.clear()
    else:
        wid.setStyleSheet(blockUnSelected)
        if wid in selectedMultipleLayer:
            selectedMultipleLayer.remove(wid)


# Function for Mouse Press Event for multiple selection in MainStruct
def SelectionmousePressEvent(self, event):
    if event.buttons() == Qt.LeftButton:
        UnselectBlock()

        global MultipleSelect
        MultipleSelect[1] = QtCore.QPoint(event.pos())
        MultipleSelect[0].setGeometry(QtCore.QRect(MultipleSelect[1], QtCore.QSize()))
        MultipleSelect[0].show()


# Function for Mouse Move Event for multiple selection in MainStruct
def SelectionmouseMoveEvent(self, event):
    global MultipleSelect
    if not MultipleSelect[1].isNull():
        MultipleSelect[0].setGeometry(QtCore.QRect(MultipleSelect[1], event.pos()).normalized())
        CheckMultipleSelection(self)


# Function for Mouse Release Event for multiple selection in MainStruct
def SelectionmouseReleaseEvent(self, event):
    if event.button() == 1:
        global MultipleSelect

        MultipleSelect[0].hide()
        MultipleSelect[0].setGeometry(QtCore.QRect(QtCore.QPoint(), QtCore.QPoint()))


# Returns the number of generated layer blocks
def NumberofGeneratedBlocks():
    return len(layers)


# If number of generated layer blocks is equal to one it sets the Insert First Block to visible
def CheckNumbOfLayers(parent):
    if NumberofGeneratedBlocks() > 0:
        parent.InsertFirstBlock.hide()
    else:
        parent.InsertFirstBlock.show()


# Function for Drag Enter Event, mainly used by MainStruct (orange area)
def dragEnterMainStruct(event):
    event.accept()


# Function for Drag Move Event, mainly used by MainStruct (orange area)
# It updates the position of the block moved inside the widget (again mainly MainStruct)
def dragMoveMainStruct(event):
    global tempBlock
    position = event.pos()
    tempBlock.move(position)
    event.setDropAction(Qt.MoveAction)
    event.accept()


# Function for Drop Event, mainly used by MainStruct (orange area)
# it checks if the block dropped is the original layer block or a new block
# In the first case it creates a new block at that position and replace the original block to its original position
# In the other case it just moves the block
# Then it sets the checker variable of the used block to Null
# Lastly, it checks if the number of generated blocks is greater than 0 and in that case it removes the Inser First Block text
def dropMainStruct(self, event, parent):
    global tempBlock

    if tempBlock.objectName() == "Blocks":
        global posit
        position = event.pos()
        newBlock = StructBlock(self, str(NumberofGeneratedBlocks()) + "block", tempBlock)
        newBlock.move(position - QtCore.QPoint(newBlock.width() / 2, newBlock.height() / 2))
        newBlock.show()
        layers.append(newBlock)

    else:
        posit = event.pos() - QtCore.QPoint(tempBlock.width() / 2, tempBlock.height() / 2)

    tempBlock.move(posit)
    event.setDropAction(Qt.MoveAction)
    event.accept()
    tempBlock = None

    CheckNumbOfLayers(parent)


# Function for Mouse Move Event, used by original blocks and partially by generated blocks
def mouseMove(event, parent):
    mimeData = QMimeData()

    drag = QDrag(parent)
    drag.setMimeData(mimeData)
    drag.setHotSpot(event.pos())

    dropAction = drag.exec_(Qt.MoveAction)


# Function for Mouse Press Event, used both for original blocks
# It saves the original position of the block and defines which is the dragged block
def mousePress(caller):
    global posit
    posit = caller.pos()
    global tempBlock
    tempBlock = caller


def Cancel(e):
    for block in selectedMultipleLayer:
        layers.remove(block)
        block.__del__()
    selectedMultipleLayer.clear()


# Label for multiple selection (this is the actual blue rectangle which is used for selecting multiple elements)
class Window(QtWidgets.QLabel):
    def __init__(self, parent=None):
        QtWidgets.QLabel.__init__(self, parent)
        self.rubberBand = QtWidgets.QRubberBand(QtWidgets.QRubberBand.Rectangle, self)


# Class for the two labels (layer number * and number of neurons) in each generated block
class TextInStructBox(QtWidgets.QLineEdit):
    defaultText = "** "

    def __init__(self, parent, text=defaultText):
        self.text = text
        super().__init__(self.defaultText + self.text, parent)

        self.setObjectName(self.text)
        self.setEnabled(False)
        self.setAlignment(Qt.AlignCenter)
        self.show()


# TODO
class Arrow:

    def __init__(self, parent, initBlock, finalBlock):
        self.parent = parent
        # QtCore.QLine.__init__(self)
        # self.setStyleSheet(self.parent.MainArrow.styleSheet())

        print(self.parent.objectName())
        self.activationFunc = None
        self.initBlock = initBlock
        self.finalBlock = finalBlock
        # self.setP1(QtCore.QPoint(400,100))
        # self.setP2(QtCore.QPoint(100,100))
        self.line = QtCore.QLine(QtCore.QPoint(400,100), QtCore.QPoint(100,100))
        # self.setLine(400,100,100,100)
        # self.setLine(self.xArrow(self.initBlock, self.finalBlock), self.yArrow(self.initBlock, self.finalBlock), self.xArrow(self.finalBlock, self.initBlock), self.yArrow(self.finalBlock, self.initBlock))
        painter = QtGui.QPainter(self.parent)
        pen = QtGui.QPen(Qt.red, 3)
        painter.setPen(pen)
        painter.drawLine(self.line)

    def yArrow(self, block1, block2):
        print("in yArrow")
        print(str(block1.objectName()) + " y: " + str(block1.y()))
        print(str(block2.objectName()) + " y: " + str(block2.y()))
        if block1.y() > block2.y():
            return block1.y()
        elif (block1.y() + block1.height()) < block2.y():
            return block1.y() + block1.height()
        else:
            return block1.y() + block1.height()/2

    def xArrow(self, block1, block2):
        print("in xArrow")
        print(str(block1.objectName()) + " x: " + str(block1.x()))
        print(str(block2.objectName()) + " x: " + str(block2.x()))
        if block1.x() > (block2.x() + block2.width()):
            return block1.x()
        elif (block1.x() + block1.width()) < block2.x():
            return block1.x() + block1.width()
        else:
            return block1.x() + block1.width()/2

    # def paintEvent(self, e):
    #     print("in painting arrow")
    #     #
    #     # painter = QtGui.QPainter()
    #     # painter.begin(self)
    #     # painter.setRenderHint(QtGui.QPainter.Antialiasing)
    #     # painter.setPen(QtCore.Qt.red)
    #     # painter.setBrush(QtCore.Qt.white)
    #     self.setLine(self.xArrow(self.initBlock, self.finalBlock), self.yArrow(self.initBlock, self.finalBlock), self.xArrow(self.finalBlock, self.initBlock), self.yArrow(self.finalBlock, self.initBlock))

        # painter.drawLine(400,100,100,100)
        # painter.drawLine(150, 150, 100, 100)
        # painter.drawLine(150, 50, 100, 100)
        # painter.end()

# Class for generating new layer blocks. Inside it has two labels: one for layer number and one for number of neurons
class StructBlock(QtWidgets.QFrame):

    # It initializes its informations: its parent, its prefab, its geometry and its two labels
    def __init__(self, parent, name, MainBlock):
        self.PrevArch = None
        self.SuccArch = None
        self.select = False

        QtWidgets.QWidget.__init__(self, parent=parent)
        self.setObjectName(name)
        self.setStyleSheet(MainBlock.styleSheet())
        self.layout = QtWidgets.QVBoxLayout(self)

        self.setFixedWidth(MainBlock.width())
        self.setFixedHeight(MainBlock.height())
        self.layer = TextInStructBox(self, "Layer")
        self.neurons = TextInStructBox(self, "Neurons")
        self.layout.addWidget(self.layer, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.neurons, alignment=Qt.AlignCenter)

        self.show()

    def __del__(self):
        self.hide()

    def isSelected(self):
        return self.select

    def selected(self):
        self.neurons.setEnabled(False)
        SelectBlock(widget=self)
        self.select = True

        # TODO
        for block in layers:
            if block.objectName() != self.objectName() and block.isSelected():
                print("in pre chiamata a creazione arrow")
                # print(str(block.objectName()) + " self: " + str(self.objectName()))
                self.PrevArch = Arrow(self.parent(), block, self)
                block.SuccArch = self.PrevArch

    def unselect(self):
        self.setStyleSheet(blockUnSelected)
        self.select = False

    # Mouse Press Event function: if its right button or double-click left button it allows changing label for the number of neurons
    # If it's single left button it starts saving itself as moving block, because it is starting the dragging event
    def mousePressEvent(self, e):
        self.unselect()

        if e.type() == QtCore.QEvent.MouseButtonDblClick and e.buttons() == Qt.LeftButton:
            self.neurons.setEnabled(True)

        elif e.buttons() == Qt.LeftButton:
            global tempBlock
            tempBlock = self

        elif e.buttons() == Qt.RightButton:
            self.selected()

    # Mouse Move Event function: if it single left button it calls the original block Mouse Move Event function
    # Unless it does nothing
    def mouseMoveEvent(self, e):
        if e.buttons() != Qt.LeftButton or (e.type() == QtCore.QEvent.MouseButtonDblClick and e.buttons() == Qt.LeftButton):
            pass
        mouseMove(e, self.parent())

    # Key Press Event funciton: If the number of neurons label was active than if it is pressed the enter key it will be disabled
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return and self.neurons.isEnabled():
            self.neurons.setEnabled(False)


class MainW(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MainW, self).__init__()
        self.setupUi(self)

        global MultipleSelect
        MultipleSelect[0] = QtWidgets.QRubberBand(QtWidgets.QRubberBand.Rectangle, self.MainStruct)
        MultipleSelect[1] = QtCore.QPoint()

        self.Blocks.mouseMoveEvent = lambda event: mouseMove(event, self.MainStruct)
        self.Blocks.mousePressEvent = lambda event: mousePress(self.Blocks)
        self.Blocks.setObjectName("Blocks")

        self.MainStruct.setAcceptDrops(True)
        self.MainStruct.dragEnterEvent = lambda event: dragEnterMainStruct(event)
        self.MainStruct.dragMoveEvent = lambda event: dragMoveMainStruct(event)
        self.MainStruct.dropEvent = lambda event: dropMainStruct(self.MainStruct, event, self)
        self.MainStruct.mousePressEvent = lambda event: SelectionmousePressEvent(self.MainStruct, event)
        self.MainStruct.mouseMoveEvent = lambda event: SelectionmouseMoveEvent(self.MainStruct, event)
        self.MainStruct.mouseReleaseEvent = lambda event: SelectionmouseReleaseEvent(self.MainStruct, event)

        self.Delete.mousePressEvent = lambda event: Cancel(event)


# Global variables for original position of a moved widget and block which is dropped after a drag event
posit = None
tempBlock = None
MultipleSelect = {}
layers = []
selectedMultipleLayer = []

app = QtWidgets.QApplication(sys.argv)

window = MainW()
window.show()

app.exec()
