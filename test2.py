from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag
from PyQt5 import QtGui
from PyQt5 import QtCore

import sys

from mainwindow import Ui_MainWindow


class ButtonInBox(QtWidgets.QPushButton):
    def __init__(self, parent, title):
        super().__init__(title, parent)


    def mousePressEvent(self, e):
        print("nuovo bottone in box")

#
# class StructBox(QtWidgets.QWidget):
#
#     def __init__(self, parent):
#         super().__init__(parent)
#
#         self.setGeometry(10,10,500,600)
#
#     def mouseMoveEvent(self, e):
#         if e.buttons() == Qt.RightButton:
#             mime = QMimeData()
#
#             drag = QDrag(self)
#             drag.setMimeData(mime)
#             drag.setHotSpot(e.pos() - self.rect().topLeft())
#
#             drop = drag.exec(Qt.MoveAction)

# !!

class MainW(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MainW, self).__init__()
        self.setupUi(self)
        # self.box = StructBox(self)

    #
    # def commPressed(self):
    #     NewWindow = QtWidgets.QDialog()
    #     NewWindow.exec()
    #     print("shown")

def mouseMoveEvent(self, e):
    if e.buttons() != Qt.LeftButton:
        return

    mimeData = QMimeData()

    drag = QDrag(self)
    drag.setMimeData(mimeData)
    drag.setHotSpot(e.pos())
    # - self.rect().topLeft())
    dropAction = drag.exec_(Qt.MoveAction)

def mousePressEvent(self, e):

    if e.button() == Qt.RightButton:
        print('press')
    else:
        global posit
        posit = self.pos()

def dragEnterEvent(self, e):
    # if self is window.MainStruct:
    #     dragMainStruct = True
    print("in drag")
    e.accept()

def dragMoveEvent(self, e, obj):
    position = e.pos()
    obj.move(position)
    e.setDropAction(Qt.MoveAction)
    e.accept()

def dropEvent(self, e, obj):
    # if self is window.MainStruct:
    #     dragMainStruct = False
    position = e.pos()
    button = ButtonInBox(self, "nuovo bottone")
    button.move(position - QtCore.QPoint(button.width()/2, button.height()/2))
    button.show()
    global posit
    obj.move(posit)
    print("in drop")
    e.setDropAction(Qt.MoveAction)
    e.accept()
    posit = None

#
# def dragLeaveEvent(self, e):
#     if self is window.MainStruct:
#         dragMainStruct = False
#
# def mouseMoveEvent2(self, e):
#     if dragMainStruct is True and e.button() == Qt.RightButton:


#
# global dragMainStruct
# dragMainStruct = False

global posit

app = QtWidgets.QApplication(sys.argv)

window = MainW()

window.show()

# window.CommSave.pressed.connect(window.commPressed)

window.CommSave.mouseMoveEvent = lambda event: mouseMoveEvent(window.CommSave, event)
window.CommSave.mousePressEvent = lambda event: mousePressEvent(window.CommSave, event)

# window.tab.setAcceptDrops(True)
window.MainStruct.setAcceptDrops(True)

# window.tab.dragEnterEvent = lambda event: dragEnterEvent(window.tab, event)
# window.tab.dropEvent = lambda event: dropEvent(window.tab, event, window.CommSave)
window.MainStruct.dragEnterEvent = lambda event: dragEnterEvent(window.MainStruct, event)
window.MainStruct.dropEvent = lambda event: dropEvent(window.MainStruct, event, window.CommSave)
window.MainStruct.dragMoveEvent = lambda event: dragMoveEvent(window.MainStruct, event, window.CommSave)

# window.MainStruct.mouseMoveEvent = lambda event: mouseMoveEvent2(window.MainStruct, event)
# window.MainStruct.dragLeaveEvent = lambda event: dragLeaveEvent(window.MainStruct, event)

# # window.MainStruct.
# window.MainStruct.setDropIndicatorShown(True)
# window.MainStruct.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
app.exec()
