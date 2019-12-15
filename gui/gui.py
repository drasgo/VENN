from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag
from PyQt5 import QtGui
from PyQt5 import QtCore
import gui.costants as costants
from gui.mainwindow import Ui_MainWindow
import nn.mainNN as mainNN
import os


# Selects every block/arch in the rubber multiple selection. Everything else is unselected
def CheckMultipleSelection(self):
    for widget in self.findChildren(QtWidgets.QFrame):
        if widget.geometry() in MultipleSelect[0].geometry() and widget.objectName() != "Blocks":
            SelectBlock(widget)
        else:
            UnselectBlock(widget)


# Performs the selection action: change color and add the block/arch to tu selectedMultipleLayer list
def SelectBlock(widget):
    widget.setStyleSheet(costants.blockSelected)
    if widget not in selectedMultipleLayer:
        selectedMultipleLayer.append(widget)


# Performs the unselection action: change color and remove the block/arch from the selectedMultipleLayer list. If
# no block/arch is passed, unselects every selected arch/block
def UnselectBlock(wid=None):
    if wid is None:
        for widget in selectedMultipleLayer:
            widget.unselect()
        selectedMultipleLayer.clear()
    else:
        if wid in selectedMultipleLayer:
            wid.unselect()
            selectedMultipleLayer.remove(wid)


# Function for Mouse Press Event for multiple selection in MainStruct. It defines the selection starting point, saving
# it in MultipleSelect[1].
def SelectionmousePressEvent(event):
    if event.buttons() == Qt.LeftButton:
        UnselectBlock()

        global MultipleSelect
        MultipleSelect[1] = QtCore.QPoint(event.pos())
        MultipleSelect[0].setGeometry(QtCore.QRect(MultipleSelect[1], QtCore.QSize()))
        MultipleSelect[0].show()


# Function for Mouse Move Event for multiple selection in MainStruct. It changes the dimension of the multiple selection
#  rectangle (aka the blue rubber band), checking the widgets inside it
def SelectionmouseMoveEvent(self, event):
    global MultipleSelect

    if not MultipleSelect[1].isNull():
        MultipleSelect[0].setGeometry(QtCore.QRect(MultipleSelect[1], event.pos()).normalized())
        CheckMultipleSelection(self)


# Function for Mouse Release Event for multiple selection in MainStruct. Removes the blue rubber band
def SelectionmouseReleaseEvent(event):
    if event.button() == 1:
        global MultipleSelect
        MultipleSelect[0].hide()
        MultipleSelect[0].setGeometry(QtCore.QRect(QtCore.QPoint(), QtCore.QPoint()))


# Returns the number of generated layer blocks
def NumberofGeneratedBlocks():
    return len(layers)


# Returns number of generated archs
def NumberofGeneratedArchs():
    return len(archs)


# If number of generated layer blocks is greater than 0 it sets the Insert First Block to hidden
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
        newBlock = StructBlock(self, MainBlock=tempBlock)
        newBlock.move(position - QtCore.QPoint(int(newBlock.width() / 2), int(newBlock.height() / 2)))
        UnselectBlock()

    else:
        posit = event.pos() - QtCore.QPoint(int(tempBlock.width() / 2), int(tempBlock.height() / 2))

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


# Changes every arch selected to the selected item in the activation functions combobox
def changeComboBox(self, pos):
    global selectedMultipleLayer
    item = self.model().item(pos)

    for arch in [arch for arch in selectedMultipleLayer if "arch" in arch.objectName()]:
        arch.changeColor(item.text(), self)

    UnselectBlock()


# When selected an arch which is different from what is selected in the activation function combobox, the selected item
# in the combobox changes to what the arch is
def changeArchChangeComboBox(combo, name):
    if combo is not None:
        combo.setCurrentText(name)


# Deletes every selected arch/block
def Cancel():
    for block in selectedMultipleLayer:
        if block in layers:
            layers.remove(block)

        elif block in archs:
            archs.remove(block)
        block.__del__()

    selectedMultipleLayer.clear()


# Commits the structure to one of the frameworks
def frameworkCommit(parent):
    # Checks the input data validity
    if parent.InputText.toPlainText() != "":
        inputs = parent.InputText.toPlainText()
    elif parent.numberInputs.text() != "" and parent.numberInputs.text().isdigit():
        temp = parent.numberInputs.text()
        inputs = int(temp)
    else:
        print("No informations about input data was found. Insert input data or number of inputs")
        return

    # Checks the ouput data validity
    if parent.OutputText.toPlainText() != "":
        outputs = parent.OutputText.toPlainText()
    elif parent.numberOutputs.text() != "" and parent.numberOutputs.text().isdigit():
        temp = parent.numberOutputs.text()
        outputs = int(temp)
    else:
        print("No informations about output data was found. Insert output data or number of outputs")
        return

    structure = structureCommit(parent, True, inputs=inputs, outputs=outputs)

    if structure is not None:
        structure.setFramework(parent.Framework.currentText())
        structure.exportAs()

    else:
        print("Error exporting the structure")


# Commits the current structure into our json file, saving it
def structureCommit(parent, called=False, inputs=None, outputs=None):
    structure = mainNN.NNStructure(blocks=layers, arrows=archs,
                                   inputData=inputs, outputData=outputs)

    if parent.StructureFilename.text() != "":
        structure.setStructureFilename(parent.StructureFilename.text())

    if parent.LossFunction.currentText() != "":
        structure.setCostFunction(parent.LossFunction.currentText())

    if structure.checkTopology():
        structure.commitTopology()

        if called is True:
            return structure
        else:
            structure.saveTopology()

    else:
        print("qualcosa è andato starto")

        if called is True:
            return None


# It loads our json file, if existent, and recreate the saved structure
def structureLoad(parent, comboBox):
    global layers
    global archs

    structure = mainNN.NNStructure()

    if parent.StructureFilename.text() != "":
        structure.setStructureFilename(parent.StructureFilename.text())

    loadedData = structure.loadTopology()

    if loadedData is None:
        print("Error  opening previous structure")
    else:
        # Uncomment if previous blocks need to be deleted before loading other blocks
        for comp in layers + archs:
            comp.__del__()

        for block in [loadedData[x] for x in loadedData if loadedData[x]["block"] is True]:
            newBlock = StructBlock(parent.MainStruct, parent.Blocks, block)

        for arrow in [loadedData[x] for x in loadedData if loadedData[x]["block"] is False]:
            arrow["combo"] = comboBox
            newArrow = Arrow(parent.MainStruct, loaded=arrow)

        for block in [loadedData[x] for x in loadedData if loadedData[x]["block"] is True]:
            for comp in [x for x in layers if block["name"] == x.objectName()]:
                comp.addLoadedArchs(block["PrevArch"], prev=True)
                comp.addLoadedArchs(block["SuccArch"], prev=False)

        CheckNumbOfLayers(parent)


# Open the input/output file specified and loads the data into the input/output textbox
def inputData(parent, button):
    fileDial = QtWidgets.QFileDialog.getOpenFileName(button, "Input File", os.path.curdir, costants.INPUT_OUTPUT_DATA_FILE_EXTENSION)
    fileData = ""

    with open(fileDial[0], 'r') as fp:
        for line in fp.readline():
            fileData = fileData + line
    fileData.replace("\n", "")

    if button is parent.InputFi:
        parent.InputText.appendPlainText(fileData)
    else:
        parent.OutputText.appendPlainText(fileData)


# Label for multiple selection (this is the actual blue rectangle which is used for selecting multiple elements)
class Window(QtWidgets.QLabel):
    def __init__(self, parent=None):
        QtWidgets.QLabel.__init__(self, parent)
        self.rubberBand = QtWidgets.QRubberBand(QtWidgets.QRubberBand.Rectangle, self)


# Loaded in each block and specifies the block type
class BlockProperties(QtWidgets.QComboBox):

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setFixedWidth(self.parent().width() - self.parent().width() / 4)
        self.parent = parent

        for item in costants.BOX_PROPERTIES:
            self.addItem(item)

        self.currentIndexChanged.connect(self.textChanged)
        self.text = "LAYER"

    # Defines what happens when block property changes
    def textChanged(self):

        if self.text != "LAYER" and self.text != "BLANK" and self.text != "INPUT"\
                and (self.currentText() == "LAYER" or self.currentText() == "BLANK" or self.currentText() == "INPUT"):
            while len(self.parent.PrevArch) > 0:
                for arch in self.parent.PrevArch:
                    arch.__del__()

        elif self.currentText() == "OUTPUT":
            self.parent.neurons.hide()
            for arch in self.parent.SuccArch:
                arch.__del__()

        elif self.currentText() == "INPUT":
            self.parent.neurons.hide()

        self.text = self.currentText()


# Class for the two labels (layer number * and number of neurons) in each "LAYER" block
class TextInStructBox(QtWidgets.QLineEdit):
    defaultText = "** "

    def __init__(self, parent, text=defaultText):
        super().__init__(self.defaultText + text, parent)

        self.setObjectName(text)
        self.setEnabled(False)
        self.setAlignment(Qt.AlignCenter)
        self.show()


# Class for the arches
class Arrow(QtWidgets.QFrame):

    # When manually created, is created when two blocks are selected sequentially, and it will appear between them.
    # If loaded, it gets its position and the two blocks
    def __init__(self, parent, initBlock=None, finalBlock=None, loaded=None):
        QtWidgets.QFrame.__init__(self, parent=parent)

        self.activationFunc = QtWidgets.QLineEdit()
        self.stylesheet = costants.arrow_stylesheet()
        # Get None as default name from default color "white" into activation function dictionary
        self.name = costants.ARROW_DEFAULT_FUNC

        self.horizontalLayout = True
        self.upRightLayout = True
        self.startPoint = QtCore.QPoint()
        self.endPoint = QtCore.QPoint()
        self.initPoint = QtCore.QPoint()
        self.lineWidth = costants.LINE_WIDTH

        self.initBlock = None
        self.finalBlock = None

        self.block = False
        self.selected = False
        self.combo = None

        if loaded is not None:
            self.loaded(loaded)

        else:
            self.initBlock = initBlock
            self.finalBlock = finalBlock

            temp = str(NumberofGeneratedArchs()) + "arch"
            while any(x.objectName() == temp for x in archs):
                temp = str(NumberofGeneratedArchs() + 1) + "arch"

            self.setObjectName(temp)

        self.color = costants.ACTIVATION_FUNCTIONS[self.name]
        self.setStyleSheet(self.stylesheet)

        self.activationFunc.setText(self.name)
        self.activationFunc.setEnabled(False)
        self.activationFunc.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        self.activationFunc.setStyleSheet("border-color: " + self.color + ";")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.activationFunc, alignment=Qt.AlignTop)
        self.layout.setContentsMargins(0, self.lineWidth / 10, 0, self.lineWidth / 10)

        archs.append(self)
        self.show()

    def loaded(self, loaded):
        self.setObjectName(str(loaded["name"]))
        self.name = loaded["activFunc"]
        self.initBlock = next(init for init in layers if init.objectName() == loaded["initBlock"])
        self.finalBlock = next(fin for fin in layers if fin.objectName() == loaded["finalBlock"])
        self.setGeometry(loaded["position"][0], loaded["position"][1], loaded["position"][2], loaded["position"][3])
        self.stylesheet = costants.arrow_stylesheet(costants.ACTIVATION_FUNCTIONS[self.name])

    def __del__(self):
        self.hide()
        self.setParent(None)

        if self in self.initBlock.SuccArch:
            self.initBlock.SuccArch.remove(self)
        if self in self.finalBlock.PrevArch:
            self.finalBlock.PrevArch.remove(self)

        del self

    def Update(self, block):
        if block.objectName() == self.initBlock.objectName():
            self.initBlock = block
        else:
            self.finalBlock = block
        self.drawArrow()

    # TODO recursive connections
    def drawRecursiveArrow(self):
        # print("in recursive draw arrow. arrow: " + str(self.objectName()))
        if abs(self.initBlock.y() < self.finalBlock.y()):
            self.endPoint = QtCore.QPoint(self.finalBlock.x() + self.finalBlock.width() / 2, self.finalBlock.y())
            self.initPoint = QtCore.QPoint(
                (self.finalBlock.x() + self.finalBlock.width() / 2 - costants.LINE_WIDTH / 2),
                self.initBlock.y() + self.initBlock.height())
            self.upRightLayout = True
            self.setGeometry(self.initPoint.x(), self.endPoint.y(), costants.LINE_WIDTH,
                             self.initPoint.y() - self.endPoint.y())
        else:
            self.endPoint = QtCore.QPoint(self.finalBlock.x() + self.finalBlock.width() / 2,
                                          self.finalBlock.y() + self.finalBlock.height())
            self.initPoint = QtCore.QPoint(
                (self.finalBlock.x() + self.finalBlock.width() / 2 - costants.LINE_WIDTH / 2), self.initBlock.y())
            self.upRightLayout = False
            self.setGeometry(self.initPoint.x(), self.initPoint.y(), costants.LINE_WIDTH,
                             self.endPoint.y() - self.initPoint.y())

        self.initBlock.updatePosition(self, self.initPoint, finalRec=True)

    # It checks the position of the initial and final blocks and it will be drawn relatively  to those two
    def drawArrow(self):
        if abs(self.initBlock.y() - self.finalBlock.y()) <= abs(self.initBlock.x() - self.finalBlock.x()):
            self.lineWidth = costants.LINE_WIDTH
            yIn = self.initBlock.y() + self.initBlock.height() / 2 - costants.LINE_WIDTH / 2
            self.horizontalLayout = True

            if self.initBlock.x() < self.finalBlock.x():
                self.upRightLayout = False
                xIn = self.initBlock.x() + self.initBlock.width()
                xFin = self.finalBlock.x() - xIn
                self.endPoint = QtCore.QPoint(self.finalBlock.x(), yIn + self.lineWidth / 2)

            else:
                self.upRightLayout = True
                xIn = self.finalBlock.x() + self.finalBlock.width()
                xFin = self.initBlock.x() - xIn
                self.endPoint = QtCore.QPoint(self.finalBlock.x() + self.finalBlock.width(), yIn + self.lineWidth / 2)

        else:
            self.horizontalLayout = False
            xIn = self.initBlock.x() + self.initBlock.width() / 2 - costants.LINE_WIDTH / 2
            xFin = costants.LINE_WIDTH

            if self.initBlock.y() > self.finalBlock.y():
                self.upRightLayout = True
                yIn = self.finalBlock.y() + self.finalBlock.height()
                self.lineWidth = self.initBlock.y() - (self.finalBlock.y() + self.finalBlock.height())
                self.endPoint = QtCore.QPoint(xIn + costants.LINE_WIDTH / 2,
                                              self.finalBlock.y() + self.finalBlock.height())

            else:
                self.upRightLayout = False
                yIn = self.initBlock.y() + self.initBlock.height()
                self.lineWidth = self.finalBlock.y() - (self.initBlock.y() + self.initBlock.height())
                self.endPoint = QtCore.QPoint(xIn + costants.LINE_WIDTH / 2, self.finalBlock.y())

        self.startPoint = QtCore.QPoint(xIn, yIn)

        self.setGeometry(xIn, yIn, xFin, self.lineWidth)

        self.finalBlock.updatePosition(self, self.endPoint)

        UnselectBlock()

    def isSelected(self):
        return self.selected

    def mousePressEvent(self, e):
        if e.buttons() == Qt.LeftButton:
            self.selected = True
            SelectBlock(self)
            changeArchChangeComboBox(self.combo, self.name)

    # Changes the color of the arch depending the cactivation function combobox
    def changeColor(self, name, combo):
        self.name = name
        self.color = str(costants.ACTIVATION_FUNCTIONS[name])
        self.activationFunc.setText(self.name)
        self.combo = combo
        self.stylesheet = "border-color: " + self.color + "; background-color: " + self.color + ";"
        self.setStyleSheet(self.stylesheet)

    def unselect(self):
        self.setStyleSheet(self.stylesheet)
        self.selected = False


# Class for generating new layer blocks. Inside it has two labels: one for layer number and one for number of neurons
class StructBlock(QtWidgets.QFrame):

    # It initializes its informations: its parent, its prefab, its geometry and the property if created manually.
    # If not it will require its informations, like position, property and so on
    def __init__(self, parent, MainBlock, loaded=None):

        QtWidgets.QWidget.__init__(self, parent=parent)

        self.setStyleSheet(MainBlock.styleSheet())
        self.layout = QtWidgets.QVBoxLayout(self)
        self.setFixedWidth(MainBlock.width())
        self.setFixedHeight(MainBlock.height())

        self.block = True
        self.PrevArch = []
        self.SuccArch = []
        self.select = False
        self.initRecursion = None

        self.layer = BlockProperties(self)
        self.neurons = TextInStructBox(self, "Neurons")

        if loaded is not None:
            self.loaded(loaded)

        else:
            temp = str(NumberofGeneratedBlocks()) + "block"
            while any(x.objectName() == temp for x in layers):
                temp = str(NumberofGeneratedBlocks() + 1) + "block"

            self.setObjectName(temp)

        self.layout.addWidget(self.layer, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.neurons, alignment=Qt.AlignCenter)

        layers.append(self)
        self.show()

    # Loads everything from the saved structure, except its arches
    def loaded(self, loaded):
        self.setObjectName(str(loaded["name"]))
        self.setGeometry(loaded["position"][0], loaded["position"][1], loaded["position"][2], loaded["position"][3])
        self.layer.setCurrentText(loaded["type"])
        if loaded["type"] == "LAYER":
            self.neurons.setText(loaded["neurons"] + self.neurons.text().replace("**", ""))
        else:
            self.neurons.hide()

    # Loads its arches from the saved structure
    def addLoadedArchs(self, arch, prev):
        global archs
        for arrow in arch:
            if prev is True:
                self.PrevArch.append([ar for ar in archs if ar.objectName() == arrow][0])
            else:
                self.SuccArch.append([ar for ar in archs if ar.objectName() == arrow][0])

    def __del__(self):
        self.hide()
        self.setParent(None)

        for arch in self.PrevArch + self.SuccArch:
            arch.__del__()
        del self

    def isSelected(self):
        return self.select

    # When it is selected it defines what to do. If it wasn't the first block manually selected it checks if it is
    # allowed to have multiple prev arches. If so it proceeds.
    def selected(self):
        self.neurons.setEnabled(False)
        SelectBlock(widget=self)
        self.select = True

        for block in layers:

            if block.objectName() != self.objectName() and block.isSelected():
                if ((self.layer.text == "LAYER" or self.layer.text == "BLANK") and len(self.PrevArch) == 0) \
                        or self.layer.text != "LAYER" or self.layer.text != "BLANK":
                    prevArch = Arrow(self.parent(), block, self)
                    block.SuccArch.append(prevArch)
                    self.PrevArch.append(prevArch)
                    prevArch.drawArrow()
                    self.updateArches()

                elif (self.layer.text == "LAYER" or self.layer.text == "BLANK") and len(self.PrevArch) > 0:
                    self.select = False
                    block.select = False
                    UnselectBlock()
                # self.updatePosition(prevArch, prevArch.endPoint)

    # Updates its position according to where its previous arch is
    def updatePosition(self, arch, point, finalRec=False):
        if finalRec is True:

            if arch.upRightLayout:
                self.move(point - QtCore.QPoint(int(self.width() / 2), self.height()))
            else:
                self.move(point - QtCore.QPoint(int(self.width() / 2), 0))

        elif self.initRecursion is None:
            if arch.horizontalLayout:

                if arch.upRightLayout:
                    self.move(point - QtCore.QPoint(self.width(), int(self.height() / 2)))

                else:
                    self.move(point - QtCore.QPoint(0, int(self.height() / 2)))

            else:

                if arch.upRightLayout:
                    self.move(point - QtCore.QPoint(int(self.width() / 2), self.height()))

                else:
                    self.move(point - QtCore.QPoint(int(self.width() / 2), 0))

            self.initRecursion = arch
            self.updateArches(True)

        else:
            self.updateArches(True, True)

    def unselect(self):
        self.setStyleSheet(costants.blockUnSelected)
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

    # It updates the next arch
    def updateArches(self, succ=False, recursion=False):
        # Called if block is moved and there are no more succ blocks
        if succ is False:
            for arch in self.PrevArch:
                arch.Update(self)
        # Called if another block is created and every other next block's position is updated
        else:
            if recursion is False:
                for arch in self.SuccArch:
                    arch.Update(self)
            else:
                self.initRecursion.drawRecursiveArrow()
        self.initRecursion = None

    # Mouse Move Event function: if it single left button it calls the original block Mouse Move Event function
    # Unless it does nothing
    def mouseMoveEvent(self, e):
        if e.buttons() != Qt.LeftButton:
            return

        mouseMove(e, self.parent())

        if len(self.SuccArch) > 0:
            for arch in self.PrevArch:
                arch.__del__()

        self.updateArches()
        self.updateArches(True)

    # Key Press Event funciton: If the number of neurons label was active than if it is pressed the enter key it will be disabled
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Return and self.neurons.isEnabled():
            self.neurons.setEnabled(False)


# It loads everything up
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
        self.MainStruct.mousePressEvent = lambda event: SelectionmousePressEvent(event)
        self.MainStruct.mouseMoveEvent = lambda event: SelectionmouseMoveEvent(self.MainStruct, event)
        self.MainStruct.mouseReleaseEvent = lambda event: SelectionmouseReleaseEvent(event)

        self.Delete.clicked.connect(Cancel)

        self.ChooseArrow.currentIndexChanged.connect(
            lambda: changeComboBox(self.ChooseArrow, self.ChooseArrow.currentIndex()))

        for transFunc in costants.ACTIVATION_FUNCTIONS:
            item = QtGui.QStandardItem(str(transFunc))
            item.setForeground(QtGui.QColor(str(costants.ACTIVATION_FUNCTIONS[transFunc])))
            mod = self.ChooseArrow.model()
            mod.appendRow(item)

        self.CommSave.clicked.connect(lambda: structureCommit(self))
        self.LoadStr.clicked.connect(lambda: structureLoad(self, self.ChooseArrow))

        self.InputFi.clicked.connect(lambda: inputData(self, self.InputFi))
        self.OutputFi.clicked.connect(lambda: inputData(self, self.OutputFi))

        for frame in costants.FRAMEWORKS:

            if frame == "TensorFlow":
                try:
                    import tensorflow
                except ImportError:
                    continue
            elif frame == "PyTorch":
                try:
                    import torch
                except ImportError:
                    continue
            elif frame == "Keras":
                try:
                    import keras
                except ImportError:
                    continue
            elif frame == "Scikit-Learn":
                try:
                    #  TODO change to fastai
                    import sklearn
                except ImportError:
                    continue

            if self.Framework.currentText() == "No Framework Found":
                self.Framework.removeItem(0)

            item = QtGui.QStandardItem(str(frame))
            mod = self.Framework.model()
            mod.appendRow(item)

        for cost in costants.COST_FUNCTION:
            item = QtGui.QStandardItem(str(cost))
            mod = self.LossFunction.model()
            mod.appendRow(item)

        self.FrameworkCommit.clicked.connect(lambda: frameworkCommit(self))


# Global variables for original position of a moved widget and block which is dropped after a drag event
posit = None
tempBlock = None
MultipleSelect = {}
archs = []
layers = []
selectedMultipleLayer = []
