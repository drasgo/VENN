from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag
from PyQt5 import QtGui
from PyQt5 import QtCore
import os
import importlib
import VENN.costants as costants
from VENN.gui.mainwindow import Ui_MainWindow
import VENN.nn.mainNN as mainNN


def CheckMultipleSelection(self):
    """ Selects every block/arch in the rubber multiple selection. Everything else is unselected"""
    for widget in self.findChildren(QtWidgets.QFrame):
        if widget.geometry() in MultipleSelect[0].geometry() and widget.objectName() != "Blocks":
            SelectBlock(widget)
        else:
            UnselectBlock(widget)


def SelectBlock(widget):
    """ Performs the selection action: change color and add the block/arch to tu selectedMultipleLayer list"""
    if widget not in selectedMultipleLayer and (isinstance(widget, Arrow) or isinstance(widget, StructBlock)):
        widget.setStyleSheet(costants.blockSelected)
        selectedMultipleLayer.append(widget)


def UnselectBlock(wid=None):
    """ Performs the unselection action: change color and remove the block/arch from the selectedMultipleLayer list.
    If no block/arch is passed, unselects every selected arch/block"""
    if wid is None:
        for widget in selectedMultipleLayer:
            widget.unselect()
        selectedMultipleLayer.clear()
    else:
        if wid in selectedMultipleLayer:
            wid.unselect()
            selectedMultipleLayer.remove(wid)


def SelectionmousePressEvent(event):
    """ Function for Mouse Press Event for multiple selection in MainStruct. It defines the selection starting point, saving
     it in MultipleSelect[1]."""
    if event.buttons() == Qt.LeftButton:
        UnselectBlock()

        global MultipleSelect
        MultipleSelect[1] = QtCore.QPoint(event.pos())
        MultipleSelect[0].setGeometry(QtCore.QRect(MultipleSelect[1], QtCore.QSize()))
        MultipleSelect[0].show()


def SelectionmouseMoveEvent(self, event):
    """ Function for Mouse Move Event for multiple selection in MainStruct. It changes the dimension of the multiple selection
      rectangle (aka the blue rubber band), checking the widgets inside it"""
    global MultipleSelect

    if not MultipleSelect[1].isNull():
        MultipleSelect[0].setGeometry(QtCore.QRect(MultipleSelect[1], event.pos()).normalized())
        CheckMultipleSelection(self)


def SelectionmouseReleaseEvent(event):
    """ Function for Mouse Release Event for multiple selection in MainStruct. Removes the blue rubber band"""
    if event.button() == 1:
        global MultipleSelect
        MultipleSelect[0].hide()
        MultipleSelect[0].setGeometry(QtCore.QRect(QtCore.QPoint(), QtCore.QPoint()))


def mouseMove(event, parent):
    """ Function for Mouse Move Event, used by original blocks and partially by generated blocks"""
    mimeData = QMimeData()

    drag = QDrag(parent)
    drag.setMimeData(mimeData)
    drag.setHotSpot(event.pos())

    drag.exec_(Qt.MoveAction)


def mousePress(caller):
    """ Function for Mouse Press Event, used both for original blocks
     It saves the original position of the block and defines which is the dragged block"""
    global posit
    posit = caller.pos()
    global tempBlock
    tempBlock = caller


def keyPress(event):
    """Bind ESC and Canc keys to the Cancel() function, which removes blocks and arrows selected"""
    if event.key() == QtCore.Qt.Key_Delete or event.key() == QtCore.Qt.Key_Escape:
        Cancel()


def NumberofGeneratedBlocks():
    """ Returns the number of generated layer blocks"""
    return len(layers)


def NumberofGeneratedArchs():
    """ Returns number of generated archs"""
    return len(archs)


def CheckNumbOfLayers(parent):
    """ If number of generated layer blocks is greater than 0 it sets the Insert First Block to hidden"""
    if NumberofGeneratedBlocks() > 0:
        parent.InsertFirstBlock.hide()
    else:
        parent.InsertFirstBlock.show()


def dragEnterMainStruct(event):
    """ Function for Drag Enter Event, mainly used by MainStruct (orange area)"""
    event.accept()


def dragMoveMainStruct(event):
    """ Function for Drag Move Event, mainly used by MainStruct (orange area)
     It updates the position of the block moved inside the widget (again mainly MainStruct)"""
    global tempBlock
    tempPos = event.pos() - QtCore.QPoint(int(tempBlock.width() / 2), int(tempBlock.height() / 2))
    tempBlock.move(tempPos)
    event.setDropAction(Qt.MoveAction)
    event.accept()


def dropMainStruct(self, event, parent):
    """ Function for Drop Event, mainly used by MainStruct (orange area)
     it checks if the block dropped is the original layer block or a new block
     In the first case it creates a new block at that position and replace the original block to its original position
     In the other case it just moves the block
     Then it sets the checker variable of the used block to Null
     Lastly, it checks if the number of generated blocks is greater than 0 and in that case it removes the Inser First Block text"""
    global tempBlock

    if tempBlock.objectName() == "Blocks":
        global posit
        position = event.pos()
        if isinstance(tempBlock, StructBlock) or isinstance(tempBlock, QtWidgets.QFrame):
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


def changeComboBox(self, pos):
    """ Changes every arch selected to the selected item in the activation functions combobox"""
    global selectedMultipleLayer
    item = self.model().item(pos)

    for arch in [arch for arch in selectedMultipleLayer if "arch" in arch.objectName()]:
        arch.changeColor(item.text())

    UnselectBlock()


def changeArchChangeComboBox(name):
    """ When selected an arch which is different from what is selected in the activation function combobox, the selected item
     in the combobox changes to what the arch is"""
    global comboBox
    comboBox.setCurrentText(name)


def Cancel():
    """ Deletes every selected arch/block"""
    for block in selectedMultipleLayer:
        if block in layers:
            layers.remove(block)

        elif block in archs:
            archs.remove(block)
        block.__del__()

    selectedMultipleLayer.clear()


def frameworkRun(parent):
    """ TODO: Add tick box for testing: Run or Run + Test"""
    global structure

    if structure is None or structure.frameStruct is None or structure.framework != parent.Framework.currentText():
        frameworkCommit(parent)

    setupNNStructure(parent)

    result = structure.runAs()
    # resultTrain, resultTest = structure.runAs(parent.Test.getOption() ?

    logger(result)


def frameworkCommit(parent):
    """ Commits the structure to one of the frameworks"""
    global structure

    if structure is None:
        if structureCommit(parent, True) is False:
            logger("Error producing scheme of neural network for exporting. Aborting")
            return
    else:
        setupNNStructure(parent)

    structure.exportAs()


def structureCommit(parent, called=False):
    """ Commits the current structure into our json file, saving it"""
    global structure

    structure = mainNN.NNStructure()
    setupNNStructure(parent)

    if structure.checkTopology():
        structure.commitTopology()

        if called is not True:
            structure.saveTopology()
        else:
            return True

    else:
        logger("qualcosa è andato starto")

        if called is True:
            return False


def structureLoad(parent):
    """ It loads our json file, if existent, and recreate the saved structure"""
    global layers
    global archs
    global structure

    if structure is None:
        structure = mainNN.NNStructure()

    setupNNStructure(parent)

    loadedData = structure.loadTopology()

    if loadedData is None:
        logger("Error  opening previous structure")
    else:
        # Uncomment if previous blocks need to be deleted before loading other blocks
        for comp in layers:
            comp.__del__()

        del layers[:]
        del archs[:]

        for block in [loadedData[x] for x in loadedData if loadedData[x]["block"] is True]:
            StructBlock(parent.MainStruct, parent.Blocks, block)

        for arrow in [loadedData[x] for x in loadedData if loadedData[x]["block"] is False]:
            Arrow(parent.MainStruct, loaded=arrow)

        # Grab every block in the gui and checks which of the newly created blocks in the loaded structure is.
        # For each block then attach the previous and following arches
        for block in [loadedData[x] for x in loadedData if loadedData[x]["block"] is True]:
            for comp in [x for x in layers if block["name"] == x.objectName()]:
                comp.addLoadedArchs(block["PrevArch"], prev=True)
                comp.addLoadedArchs(block["SuccArch"], prev=False)

        CheckNumbOfLayers(parent)

        logger("Model loaded!")


def setupNNStructure(parent):
    global structure

    structure.setBlocksArrows(layers, archs)

    if parent.StructureFilename.text() != "":
        structure.setStructureFilename(parent.StructureFilename.text())

    if parent.LossFunction.currentText() != "":
        structure.setCostFunction(parent.LossFunction.currentText())

    # Checks input output data
    if parent.InputText.toPlainText() != "" and parent.OutputText.toPlainText() != "":
        structure.setInputOutput(parent.InputText.toPlainText(), parent.OutputText.toPlainText())

    #  Checks input output data quantity
    elif (parent.numberInputs.text() != "" and parent.numberInputs.text().isdigit()) and \
            (parent.numberOutputs.text() != "" and parent.numberOutputs.text().isdigit()):
        temp = parent.numberInputs.text()
        temp1 = parent.numberOutputs.text()
        structure.setInputOutputNumber(int(temp), int(temp1))

    if parent.Framework.currentText() != "":
        structure.setFramework(parent.Framework.currentText())

    structure.setLogger(logger)

    # TODO: Add in the GUI the optimizer option and the epoch option
    # if parent.Optimizer.currentText() != "":
    #       structure.setOptimizer(parent.Optimizer.currentText())
    # if parent.Epoch.currentText() != "" and isinstance(parent.Epoch.currentText(), int):
    #     structure.setEpoch(parent.Epoch.currentText())
    # Also implement choice of input data: normal (aka matrix data for mlp and such), images for CNN, time series for RNN..


def inputData(parent, button):
    """ Open the input/output file specified and loads the data into the input/output textbox"""
    fileDial = QtWidgets.QFileDialog.getOpenFileName(button, "Input File", os.path.curdir,
                                                     costants.INPUT_OUTPUT_DATA_FILE_EXTENSION)
    fileData = ""

    with open(fileDial[0], 'r') as fp:
        for line in fp.readline():
            fileData = fileData + line
    fileData.replace("\n", "")

    if button is parent.InputFi:
        parent.InputText.appendPlainText(fileData)
    else:
        parent.OutputText.appendPlainText(fileData)


def logger(text="", color="black"):
    """ Hook the Log window for all the log printing"""
    global loggerWindow
    loggerWindow.setTextColor(QtGui.QColor(color))
    loggerWindow.append(text)


def resizeEvent(main, e):
    """For every element in the gui check the old and new dimensions of the window and scale accordingly width, height,
    x starting position and y starting position. This operation is also performed on the new blocks and arch created.
    """
    global layers
    global archs
    newVal = main.geometry()
    resizeElement(main.OutputFi, main.oldMax, newVal)
    resizeElement(main.LoadStr, main.oldMax, newVal)
    resizeElement(main.RunNN, main.oldMax, newVal)
    resizeElement(main.InputFi, main.oldMax, newVal)
    resizeElement(main.Input, main.oldMax, newVal)
    resizeElement(main.InputText, main.oldMax, newVal)
    resizeElement(main.horizontalLayoutWidget, main.oldMax, newVal)
    resizeElement(main.CommSave, main.oldMax, newVal)
    resizeElement(main.Output, main.oldMax, newVal)
    resizeElement(main.OutputText, main.oldMax, newVal)
    resizeElement(main.MainStruct, main.oldMax, newVal)
    resizeElement(main.Blocks, main.oldMax, newVal)
    resizeElement(main.ChooseArrow, main.oldMax, newVal)
    resizeElement(main.Delete, main.oldMax, newVal)
    resizeElement(main.InsertFirstBlock, main.oldMax, newVal)
    resizeElement(main.LossFunction, main.oldMax, newVal)
    resizeElement(main.label_4, main.oldMax, newVal)
    resizeElement(main.Log, main.oldMax, newVal)
    resizeElement(main.LogWindow, main.oldMax, newVal)
    resizeElement(main.Framework, main.oldMax, newVal)
    resizeElement(main.StructureFilename, main.oldMax, newVal)
    resizeElement(main.label, main.oldMax, newVal)
    resizeElement(main.FrameworkCommit, main.oldMax, newVal)
    resizeElement(main.label_2, main.oldMax, newVal)
    resizeElement(main.numberInputs, main.oldMax, newVal)
    resizeElement(main.label_3, main.oldMax, newVal)
    resizeElement(main.numberOutputs, main.oldMax, newVal)
    for elem in layers:
        resizeElement(elem, main.oldMax, newVal)
    for elem in archs:
        resizeElement(elem, main.oldMax, newVal)
    main.oldMax = newVal


def resizeElement(elem, oldMax, newMax):
    """Here is performed the actual rescale operation of a generic element, which is called for every element."""
    newWidth = int(((elem.width()) * newMax.width()) / oldMax.width())
    newHeight = int(((elem.height()) * newMax.height()) / oldMax.height())
    newX = int((elem.x() * newMax.width()) / oldMax.width())
    newY = int((elem.y() * newMax.height()) / oldMax.height())
    elem.resize(newWidth, newHeight)
    elem.move(newX, newY)


class BlockProperties(QtWidgets.QComboBox):
    """ Loaded in each block and specifies the block type"""

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setFixedWidth(self.parent().width() - self.parent().width() / 4)
        self.parent = parent

        for item in costants.BOX_PROPERTIES:
            self.addItem(item)

        self.currentIndexChanged.connect(self.textChanged)

    def textChanged(self):
        """ Defines what happens when block property changes"""

        # if self.text != "LAYER" and self.text != "BLANK" and self.text != "INPUT"\
        #         and (self.currentText() == "LAYER" or self.currentText() == "BLANK" or self.currentText() == "INPUT"):

        if self.currentText() == "DENSE" or self.currentText() == "CNN" or self.currentText() == "POOLING" or \
                self.currentText() == "DROPOUT" or self.currentText() == "BLANK":

            if self.currentText() != "BLANK":
                self.parent.neurons.show()
            else:
                self.parent.neurons.hide()

            if len(self.parent.PrevArch) > 1:
                for arch in self.parent.PrevArch:
                    arch.__del__()
        else:
            self.parent.neurons.hide()

            if self.currentText() == "OUTPUT":
                for arch in self.parent.SuccArch:
                    arch.__del__()

            elif self.currentText() == "INPUT":
                for arch in self.parent.PrevArch:
                    arch.__del__()

            elif self.currentText() == "SUM" or self.currentText() == "SUB" or self.currentText() == "MULT":
                for arch in self.parent.PrevArch:
                    arch.changeColor()


class TextInStructBox(QtWidgets.QLineEdit):
    """ Class for the two labels (layer number * and number of neurons) in each "DENSE" block"""
    defaultText = "** "

    def __init__(self, parent, text=defaultText):
        super().__init__(self.defaultText + text, parent)

        self.setObjectName(text)
        self.setEnabled(False)
        self.setAlignment(Qt.AlignCenter)
        self.show()


class Arrow(QtWidgets.QFrame):
    """ Class for the arches"""

    def __init__(self, parent, initBlock=None, finalBlock=None, loaded=None):
        """ When manually created, is created when two blocks are selected sequentially, and it will appear between them.
         If loaded, it gets its position and the two blocks"""
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
            while any(x.objectName() == temp for x in archs) and len(archs) > 0:
                temp = str(NumberofGeneratedArchs() + 1) + "arch"
                # print(str(temp) + ", " + str([x.objectName() for x in archs]))

            self.setObjectName(temp)

        self.color = costants.ACTIVATION_FUNCTIONS[self.name]
        self.setStyleSheet(self.stylesheet)

        self.activationFunc.setText(self.name)
        self.activationFunc.setEnabled(False)
        self.activationFunc.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        self.activationFunc.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.activationFunc.setStyleSheet("background:transparent;")

        self.layout = QtWidgets.QStackedLayout(self)
        self.layout.addWidget(self.activationFunc)
        self.layout.setContentsMargins(0, self.lineWidth / 10, 0, self.lineWidth / 10)
        self.layout.setStackingMode(QtWidgets.QStackedLayout.StackAll)

        archs.append(self)

        self.repaint()
        self.show()

    def __del__(self):
        self.hide()
        self.setParent(None)

        if self in self.initBlock.SuccArch:
            self.initBlock.SuccArch.remove(self)
        if self in self.finalBlock.PrevArch:
            self.finalBlock.PrevArch.remove(self)

        del self

    def loaded(self, loaded):
        self.setObjectName(str(loaded["name"]))
        self.name = loaded["activFunc"]
        self.initBlock = next(init for init in layers if init.objectName() == loaded["initBlock"])
        self.finalBlock = next(fin for fin in layers if fin.objectName() == loaded["finalBlock"])
        self.setGeometry(loaded["position"][0], loaded["position"][1], loaded["position"][2], loaded["position"][3])
        self.stylesheet = costants.arrow_stylesheet(costants.ACTIVATION_FUNCTIONS[self.name])
        self.checkOrientation()

    def checkOrientation(self):
        if self.initBlock.y() == self.finalBlock.y():
            self.horizontalLayout = True
        else:
            self.horizontalLayout = False

        if self.initBlock.x() < self.finalBlock.x() or self.finalBlock.y() < self.initBlock.y():
            self.upRightLayout = True
        else:
            self.upRightLayout = False

    def isSelected(self):
        return self.selected

    def mousePressEvent(self, e):
        if e.buttons() == Qt.LeftButton:
            self.selected = True
            changeArchChangeComboBox(self.name)
            SelectBlock(self)

    def changeColor(self, name=""):
        """ Changes the color of the arch depending the cactivation function combobox"""
        if self.finalBlock.layer.currentText() == "SUM" or self.finalBlock.layer.currentText() == "SUB" or \
                self.finalBlock.layer.currentText() == "MULT":
            name = "None"
        self.name = name
        self.color = str(costants.ACTIVATION_FUNCTIONS[name])
        self.activationFunc.setText(self.name)
        self.stylesheet = "border-color: black; background-color: " + self.color + ";"
        self.setStyleSheet(self.stylesheet)
        self.repaint()

    def unselect(self):
        self.setStyleSheet(self.stylesheet)
        self.selected = False

    def paintEvent(self, e):
        init = QtGui.QPainter()
        init.begin(self)
        init.setPen(QtGui.QPen(Qt.black, 10, Qt.SolidLine))
        # If the arrow is horizontal
        if self.horizontalLayout is True:
            # If the arrow is pointing towards right
            if self.upRightLayout is False:
                init.drawEllipse(QtCore.QPoint(0, int(self.height() / 2)), int(self.height() / 2), 15)
            # If the arrow is pointing towards left
            else:
                init.drawEllipse(QtCore.QPoint(self.width(), int(self.height() / 2)), int(self.height() / 2), 15)
        # If the arrow is vertical
        else:
            # If the arrow is pointing towards down
            if self.upRightLayout is False:
                init.drawEllipse(QtCore.QPoint(int(self.width() / 2), 0), 15, int(self.width() / 2))
            # If the arrow is pointing towards up
            else:
                init.drawEllipse(QtCore.QPoint(int(self.width() / 2), self.height()), 15, int(self.width() / 2))
        init.end()

    def drawArrow(self, All=True, split=False):
        """ It checks the position of the initial and final blocks and it will be drawn relatively  to those two"""
        prevGeom = self.geometry()
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

        UnselectBlock()

        if (prevGeom != self.geometry() and All is True) or len(self.finalBlock.SuccArch) == 0:
            self.finalBlock.updatePosition(self, self.endPoint, split)


class StructBlock(QtWidgets.QFrame):
    """ Class for generating new layer blocks. Inside it has two labels: one for layer number and one for number of neurons"""

    def __init__(self, parent, MainBlock, loaded=None):
        """ It initializes its informations: its parent, its prefab, its geometry and the property if created manually.
        If not it will require its informations, like position, property and so on"""

        QtWidgets.QWidget.__init__(self, parent=parent)

        self.setStyleSheet(MainBlock.styleSheet())
        self.layout = QtWidgets.QVBoxLayout(self)
        self.resize(MainBlock.width(), MainBlock.height())

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

    def __del__(self):
        self.hide()
        self.setParent(None)

        for arch in self.PrevArch + self.SuccArch:
            arch.__del__()
        del self

    def loaded(self, loaded):
        """ Loads everything from the saved structure, except its arches"""
        self.setObjectName(str(loaded["name"]))
        self.resize(loaded["size"][0], loaded["size"][1])
        self.move(loaded["pos"][0], loaded["pos"][1])
        self.layer.setCurrentText(loaded["type"])
        if loaded["type"] == "DENSE":
            self.neurons.setText(loaded["neurons"] + self.neurons.text().replace("**", ""))
        else:
            self.neurons.hide()

    def addLoadedArchs(self, arch, prev):
        """ Loads its arches from the saved structure"""
        global archs
        for arrow in arch:
            if prev is True:
                self.PrevArch.append([ar for ar in archs if ar.objectName() == arrow][0])
            else:
                self.SuccArch.append([ar for ar in archs if ar.objectName() == arrow][0])

    def mousePressEvent(self, e):
        """ Mouse Press Event function: if its right button or double-click left button it allows changing label for the number of neurons
         If it's single left button it starts saving itself as moving block, because it is starting the dragging event"""
        self.unselect()

        if e.type() == QtCore.QEvent.MouseButtonDblClick and e.buttons() == Qt.LeftButton:
            self.neurons.setEnabled(True)

        elif e.buttons() == Qt.LeftButton:
            global tempBlock
            tempBlock = self

        elif e.buttons() == Qt.RightButton:
            self.selected()

    def mouseMoveEvent(self, e):
        """ Mouse Move Event function: if it single left button it calls the original block Mouse Move Event function
         Unless it does nothing"""
        if e.buttons() != Qt.LeftButton:
            return

        mouseMove(e, self.parent())

        if len(self.SuccArch) > 0:
            while len(self.PrevArch) != 0:
                for arch in self.PrevArch:
                    arch.__del__()
            self.updateArches(True, split=True)
        else:
            self.updateArches()

    def removeArches(self, arch=None):
        while len(self.PrevArch) > 1:
            for arch1 in self.PrevArch:
                if arch is not None and arch is not arch1:
                    arch1.__del__()
        self.updateArches(True, split=True)

    def keyPressEvent(self, e):
        """ Key Press Event funciton: If the number of neurons label was active than if it is pressed the enter key it will be disabled"""
        if e.key() == Qt.Key_Return and self.neurons.isEnabled():
            self.neurons.setEnabled(False)

    def isSelected(self):
        return self.select

    def unselect(self):
        self.setStyleSheet(costants.blockUnSelected)
        self.select = False

    def selected(self):
        """ When it is selected it defines what to do. If it wasn't the first block manually selected it checks if it is
         allowed to have multiple prev arches. If so it proceeds."""
        self.neurons.setEnabled(False)
        SelectBlock(widget=self)
        self.select = True

        for block in layers:

            if block.objectName() != self.objectName() and block.isSelected():

                if (len(self.PrevArch) == 0 and self.layer.currentText() != "INPUT") or \
                        self.layer.currentText() == "SUM" or self.layer.currentText() == "SUB" or \
                        self.layer.currentText() == "MULT":
                    prevArch = Arrow(self.parent(), block, self)
                    block.SuccArch.append(prevArch)
                    self.PrevArch.append(prevArch)
                    prevArch.drawArrow()
                    self.updateArches()

                else:
                    self.select = False
                    block.select = False
                    UnselectBlock()
                # self.updatePosition(prevArch, prevArch.endPoint)

    def updatePosition(self, arch, point, split=False):
        """ Updates its position according to where its previous arch is"""
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

        if len(self.SuccArch) == 0:
            pass
        else:
            if len(self.PrevArch) > 1:
                self.updateArches(arch=arch)

            self.updateArches(True)

        if split is True:
            self.removeArches(arch)

    def updateArches(self, succ=False, arch=None, split=False):
        """ It updates the next or the previous arch"""
        # Called if block is moved and there are no more succ blocks
        if succ is False:
            for arch in self.PrevArch:
                arch.drawArrow(All=False)
        # Called if another block is created and every other next block's position is updated
        else:
            for arch in self.SuccArch:
                arch.drawArrow(split=split)

        if arch is not None:
            for arch1 in self.PrevArch:
                if arch1 is not arch:
                    arch1.drawArrow(All=False)


class MainW(QtWidgets.QMainWindow, Ui_MainWindow):
    """ It loads everything up"""

    def __init__(self):
        super(MainW, self).__init__()
        self.setupUi(self)

        global loggerWindow
        global MultipleSelect
        global comboBox

        self.oldMax = self.geometry()
        self.resizeEvent = lambda event: resizeEvent(self, event)

        MultipleSelect[0] = QtWidgets.QRubberBand(QtWidgets.QRubberBand.Rectangle, self.MainStruct)
        MultipleSelect[1] = QtCore.QPoint()

        self.keyPressEvent = lambda event: keyPress(event=event)

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
        self.LoadStr.clicked.connect(lambda: structureLoad(self))

        self.InputFi.clicked.connect(lambda: inputData(self, self.InputFi))
        self.OutputFi.clicked.connect(lambda: inputData(self, self.OutputFi))

        for frame in costants.FRAMEWORKS:

            if frame == "TensorFlow":
                if importlib.util.find_spec("tensorflow") is None:
                    continue

            elif frame == "PyTorch":
                if importlib.util.find_spec("torch") is None:
                    continue

            elif frame == "Keras":
                if importlib.util.find_spec("keras") is None:
                    continue

            # elif frame == "FastAI":
            #     if importlib.util.find_spec("fastai") is None:
            #         continue

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

        loggerWindow = self.LogWindow
        comboBox = self.ChooseArrow


# Global variables for original position of a moved widget and block which is dropped after a drag event
posit = None
tempBlock = None
structure = None
loggerWindow = None
comboBox = None
MultipleSelect = {}
archs = []
layers = []
selectedMultipleLayer = []
