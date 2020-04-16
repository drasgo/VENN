from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag
from PyQt5 import QtGui
from PyQt5 import QtCore
import os
import importlib
import re
import VENN.costants as costants
from VENN.gui.mainwindow import Ui_MainWindow
import VENN.nn.mainNN as mainNN


# TODO
# TODO
# TODO
# Implement Pooling, Dropout, CNN, RNN and multiple inputs

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


def dragMoveMainStruct(self, event):
    """ Function for Drag Move Event, mainly used by MainStruct (orange area)
     It updates the position of the block moved inside the widget (again mainly MainStruct)"""
    global tempBlock
    global insideMainStruct

    tempPos = event.pos() - QtCore.QPoint(int(tempBlock.width() / 2), int(tempBlock.height() / 2))
    tempPos2 = event.pos() + QtCore.QPoint(int(tempBlock.width() / 2), int(tempBlock.height() / 2))
    if tempBlock.objectName() == "Blocks" and (
            self.rect().contains(tempPos) is False or self.rect().contains(tempPos2) is False):

        global posit
        tempBlock.move(posit)
        insideMainStruct = False

    else:
        insideMainStruct = True
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
        if isinstance(tempBlock, StructBlock) or isinstance(tempBlock, QtWidgets.QFrame) and insideMainStruct is True:
            newBlock = StructBlock(self, MainBlock=tempBlock)
            newBlock.move(position - QtCore.QPoint(int(newBlock.width() / 2), int(newBlock.height() / 2)))

    else:
        posit = event.pos() - QtCore.QPoint(int(tempBlock.width() / 2), int(tempBlock.height() / 2))

    tempBlock.move(posit)
    event.setDropAction(Qt.MoveAction)
    event.accept()
    tempBlock = None
    UnselectBlock()

    CheckNumbOfLayers(parent)


def changeComboBox(self, pos):
    """ Changes every arch selected to the selected item in the activation functions combobox"""
    global selectedMultipleLayer
    item = self.model().item(pos)

    for arch in [arch for arch in selectedMultipleLayer if "arch" in arch.objectName()]:
        arch.changeColor(item.text())

    UnselectBlock()


def changeArchChangeComboBox(name):
    """ When selected an arch which is different from what is selected in the activation function combobox, the selected
     item in the combobox changes to what the arch is"""
    global comboBox
    for activ in costants.ACTIVATION_FUNCTIONS:
        if name in activ:
            comboBox.setCurrentText(activ)
            break


def Cancel():
    """ Deletes every selected arch/block"""
    for block in selectedMultipleLayer:
        if block in layers:
            layers.remove(block)

        elif block in archs:
            archs.remove(block)
        block.__del__()

    selectedMultipleLayer.clear()


def frameworkRunTest(button, parent):
    global structure

    if frameworkCommit(parent) is False:
        return

    if button is parent.RunNN:
        result, color = structure.runAs()
        logger(result, color)
    else:
        resultTrain, resultTest = structure.runAs(True)
        logger(resultTrain, resultTest)
    logger()


def frameworkCommit(parent):
    """ Commits the structure to one of the frameworks"""
    global structure

    if structureCommit(parent, True) is False:
        logger("Error creating model structure for framework export. Check the structure correctness.")
        logger()
        return False

    structure.exportAs()
    logger()


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
        logger("Structure error. Check that the structure follows the rules.", "red")
        if called is True:
            return False
    logger()


def structureLoad(parent):
    """ It loads our json file, if existent, and recreate the saved structure"""
    global layers
    global archs
    global structure

    if structure is None:
        structure = mainNN.NNStructure()

    fileDial = QtWidgets.QFileDialog.getOpenFileName(parent, "Load Structure", os.path.curdir,
                                                     costants.STRUCTURE_DATA_FILE_EXTENSION)
    if fileDial[0] == "":
        logger("No structure file chosen")
        logger()
        return

    if os.path.exists(fileDial[0]):
        loadingFilename = fileDial[0]
    else:
        logger("Error opening structure file: it doesn't exist!")
        logger()
        return

    setupNNStructure(parent, loadingFilename)

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
    logger()


def setupNNStructure(parent, name=""):
    global structure

    structure.setBlocksArrows(layers, archs)

    # Set the name of the current structure (the name of how it is going to be saved)
    if parent.StructureFilename.text() != "":
        structure.setStructureFilename(parent.StructureFilename.text())

    if name != "":
        structure.setLoadingStructureFilename(name)

    # Set input output files
    if parent.InputFile.text() != "" and parent.OutputFile.text() != "":
        structure.setInputOutput(parent.InputFile.text(), parent.OutputFile.text())

    # Set input output data quantity (Note: if input/output files are available, the dimension in those file will rule)
    elif any(x in costants.NUMBERS for x in parent.NumberInputs.text()) \
            and any(x in costants.NUMBERS for x in parent.NumberInputs.text()):
        nInput = "".join(list(filter(lambda x: x in costants.NUMBERS, parent.NumberInputs.text())))
        nOutput = "".join(list(filter(lambda x: x in costants.NUMBERS, parent.NumberInputs.text())))
        structure.setInputOutputNumber(int(nInput), int(nOutput))

    # Set which frameworks needs to be used for commit with/run/test
    if parent.Framework.currentText() != "":
        structure.setFramework(parent.Framework.currentText())

    # Set the logger reference
    structure.setLogger(logger)

    # Set the loss function for the run/test options (if available)
    if parent.LossFunction.currentText() != "":
        structure.setLossFunction(parent.LossFunction.currentText())

    # Set the optimizer function for the run/test options (if available)
    if parent.OptimizerFunction.currentText() != "":
        structure.setOptimizer(parent.Optimizer.currentText())

    # Set the number of epochs for the run/test options (if available)
    if any(x in costants.NUMBERS for x in parent.NumberInputs.text()):
        nEpochs = "".join(list(filter(lambda x: x in costants.NUMBERS, list(y for y in parent.numberEpochs.text()))))
        structure.setEpochs(int(nEpochs))


def inputData(parent, button):
    """ Open the input/output file specified and loads the data into the input/output textbox"""
    name = "Input File" if button is parent.InputFi else "Output File"
    fileDial = QtWidgets.QFileDialog.getOpenFileName(button, name, os.path.curdir,
                                                     costants.INPUT_OUTPUT_DATA_FILE_EXTENSION)
    if fileDial[0] == "":
        if button is parent.InputFi:
            logger("No input file chosen")
            logger()
        else:
            logger("No output file chosen")
            logger()
        return

    if os.path.exists(fileDial[0]):

        if button is parent.InputFi:
            parent.InputFile.setText(fileDial[0])
        else:
            parent.OutputFile.setText(fileDial[0])


def logger(text="", color="black"):
    """ Hook the Log window for all the log printing"""
    global loggerWindow
    if text == "":
        global loggerCounter
        loggerCounter = loggerCounter + 1
        text = str(loggerCounter) + ".  _____________________________________________"
    loggerWindow.setTextColor(QtGui.QColor(color))
    loggerWindow.append(str(text))


def clearLogger():
    global loggerWindow
    global loggerCounter
    loggerCounter = 0
    loggerWindow.setText("")


def resizeEvent(main):
    """For every element in the gui check the old and new dimensions of the window and scale accordingly width, height,
    x starting position and y starting position. This operation is also performed on the new blocks and arch created.
    """
    global layers
    global archs
    newVal = main.geometry()
    # Resize every preexisting component created in qtcreator
    resizeElement(
        [main.OutputFi, main.LoadStr, main.RunNN, main.TestNN, main.AdvancedOptions, main.InputFi, main.CommSave,
         main.MainStruct, main.ChooseArrow, main.Delete, main.InsertFirstBlock, main.Loss,
         main.LossFunction, main.Log, main.LogWindow, main.Framework, main.label, main.FrameworkCommit,
         main.NumberInputs, main.NumberOutputs, main.nInputs, main.nOutputs, main.StructureFilename,
         main.Epochs, main.numberEpochs, main.Optimizer, main.OptimizerFunction, main.InputFile, main.OutputFile,
         main.line_2, main.line_3, main.line_4, main.line_5, main.line_6, main.ClearLogger], main.oldMax, newVal)
    # Resize every procedurally created componenent (aka blocks and arrows)
    resizeElement(layers + archs + [main.Blocks], main.oldMax, newVal)
    # Reset the current window size
    main.oldMax = newVal


def resizeElement(listaElem, oldMax, newMax):
    """Here is performed the actual rescale operation of a generic element, which is called for every element."""
    for elem in listaElem:
        newWidth = int(((elem.width()) * newMax.width()) / oldMax.width())
        newHeight = int(((elem.height()) * newMax.height()) / oldMax.height())
        newX = int((elem.x() * newMax.width()) / oldMax.width())
        newY = int((elem.y() * newMax.height()) / oldMax.height())

        if elem in archs:
            elem.drawArrow()

        else:
            if "block" not in elem.objectName().lower():
                elem.resize(newWidth, newHeight)
            elem.move(newX, newY)


class BlockProperties(QtWidgets.QComboBox):
    """ Loaded in each block and specifies the block type"""

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setFixedWidth(self.parent().width() - self.parent().width() / 4)
        self.parent = parent

        for prop in costants.BOX_PROPERTIES:
            # self.resizeFont()
            # self.addItem(item)
            item = QtGui.QStandardItem(str(prop))
            # item.setForeground(QtGui.QColor(str(costants.ACTIVATION_FUNCTIONS[transFunc])))

            self.resizeFont(item)
            mod = self.model()
            mod.appendRow(item)

        self.currentIndexChanged.connect(self.textChanged)

    def resizeFont(self, bl):
        if self.currentText() == "":
            return 1

        size = 1
        while True:
            font = QtGui.QFont()
            font.setPointSize(size)
            rect = QtGui.QFontMetrics(font).boundingRect(self.currentText())

            if rect.height() <= self.height() * 0.6 and rect.width() <= self.width() * 0.5:
                size = size + 1

            else:
                break

        font.setPointSize(size)
        bl.setFont(font)

    def textChanged(self):
        """ Defines what happens when block property changes"""
        # self.resizeFont(self)

        if self.currentText() == "DENSE" or self.currentText() == "CNN" or self.currentText() == "POOLING" or \
                self.currentText() == "DROPOUT":
            self.parent.neurons.changeText(self.currentText())
            self.parent.neurons.show()

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

    def __init__(self, parent, text=costants.BLOCK_LABELS["DENSE"]):
        super().__init__(text, parent)
        self.setObjectName(text)
        self.setEnabled(False)
        self.setAlignment(Qt.AlignCenter)
        self.show()

    def changeText(self, text, num=""):
        try:
            self.setText(costants.BLOCK_LABELS[text] + str(num))
        except KeyError:
            logger("Error setting text in block", "red")


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
            self.activationFunc.setText(self.name)

        self.setStyleSheet(self.stylesheet)

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
        self.resize(loaded["size"][0], loaded["size"][1])
        self.move(loaded["pos"][0], loaded["pos"][1])

        tempName = self.name

        if any(activ == self.name for activ in costants.ACTIVATION_FUNCTIONS):
            if "(" in self.name or ")" in self.name:
                tempName = re.search("\(([^)]+)", self.name).group(1)
        else:
            logger("Error Loading structure: activation function of arch " + self.objectName() + " not supported",
                   "red")
            self.__del__()

        self.activationFunc.setText(tempName)

        self.color = costants.ACTIVATION_FUNCTIONS[self.name]
        self.stylesheet = costants.arrow_stylesheet(self.color)
        self.checkOrientation()

    def checkOrientation(self):
        if self.initBlock.y() == self.finalBlock.y():
            self.horizontalLayout = True
        else:
            self.horizontalLayout = False

        if self.initBlock.x() < self.finalBlock.x() or self.finalBlock.y() > self.initBlock.y():
            self.upRightLayout = False
        else:
            self.upRightLayout = True

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
            name = ""
            logger("Careful, arches before SUM, SUB or MULT blocks must be blank!")
            logger()

        self.color = str(costants.ACTIVATION_FUNCTIONS[name])
        text = name
        if "(" in name or ")" in name:
            text = re.search("\(([^)]+)", name).group(1)
        self.name = name
        self.activationFunc.setText(text)
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
        self.neurons = TextInStructBox(self)

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
        try:
            self.hide()
            self.setParent(None)

            for arch in self.PrevArch + self.SuccArch:
                arch.__del__()
            del self
        except RuntimeError:
            pass

    def loaded(self, loaded):
        """ Loads everything from the saved structure, except its arches"""
        self.setObjectName(str(loaded["name"]))
        self.resize(loaded["size"][0], loaded["size"][1])
        self.move(loaded["pos"][0], loaded["pos"][1])
        self.layer.setCurrentText(loaded["type"])
        if loaded["type"] in costants.BLOCK_LABELS:
            self.neurons.changeText(loaded["type"], loaded["neurons"])
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
        self.resizeEvent = lambda e: resizeEvent(self)
        self.setStyleSheet("""QPushButton:hover {background-color: grey;
                                color: #fff;}
                                QMainWindow {background-color:white;}""")

        MultipleSelect[0] = QtWidgets.QRubberBand(QtWidgets.QRubberBand.Rectangle, self.MainStruct)
        MultipleSelect[1] = QtCore.QPoint()

        self.keyPressEvent = lambda event: keyPress(event=event)

        self.Blocks.mouseMoveEvent = lambda event: mouseMove(event, self.MainStruct)
        self.Blocks.mousePressEvent = lambda event: mousePress(self.Blocks)
        self.Blocks.setObjectName("Blocks")

        self.MainStruct.keyPressEvent = lambda event: keyPress(event=event)
        self.MainStruct.setAcceptDrops(True)
        self.MainStruct.dragEnterEvent = lambda event: dragEnterMainStruct(event)
        self.MainStruct.dragMoveEvent = lambda event: dragMoveMainStruct(self.MainStruct, event)
        self.MainStruct.dropEvent = lambda event: dropMainStruct(self.MainStruct, event, self)
        self.MainStruct.mousePressEvent = lambda event: SelectionmousePressEvent(event)
        self.MainStruct.mouseMoveEvent = lambda event: SelectionmouseMoveEvent(self.MainStruct, event)
        self.MainStruct.mouseReleaseEvent = lambda event: SelectionmouseReleaseEvent(event)

        self.Delete.clicked.connect(Cancel)

        self.ChooseArrow.currentIndexChanged.connect(
            lambda: changeComboBox(self.ChooseArrow, self.ChooseArrow.currentIndex()))

        self.CommSave.clicked.connect(lambda: structureCommit(parent=self))
        self.LoadStr.clicked.connect(lambda: structureLoad(parent=self))

        self.InputFi.clicked.connect(lambda: inputData(parent=self, button=self.InputFi))
        self.OutputFi.clicked.connect(lambda: inputData(parent=self, button=self.OutputFi))

        self.FrameworkCommit.clicked.connect(lambda: frameworkCommit(parent=self))
        self.RunNN.clicked.connect(lambda: frameworkRunTest(button=self.RunNN, parent=self))
        self.TestNN.clicked.connect(lambda: frameworkRunTest(button=self.TestNN, parent=self))

        self.ClearLogger.clicked.connect(clearLogger)

        # Setting up combo boxes (frameworks, activation functions, loss functions and optimizer functions) with
        # elements from costants.py
        for frame in costants.FRAMEWORKS:

            if importlib.util.find_spec(costants.FRAMEWORKS[frame]) is None or \
                    os.path.isfile("../nn/otherFrameworks/" + costants.FRAMEWORKS[frame]):
                continue

            if self.Framework.currentText() == "No Framework Found":
                self.Framework.removeItem(0)

            item = QtGui.QStandardItem(str(frame))
            mod = self.Framework.model()
            mod.appendRow(item)

        for transFunc in costants.ACTIVATION_FUNCTIONS:
            item = QtGui.QStandardItem(str(transFunc))
            item.setForeground(QtGui.QColor(str(costants.ACTIVATION_FUNCTIONS[transFunc])))
            mod = self.ChooseArrow.model()
            mod.appendRow(item)

        for cost in costants.COST_FUNCTION:
            item = QtGui.QStandardItem(str(cost))
            mod = self.LossFunction.model()
            mod.appendRow(item)

        for optim in costants.OPTIMIZERS:
            item = QtGui.QStandardItem(str(optim))
            mod = self.OptimizerFunction.model()
            mod.appendRow(item)

        loggerWindow = self.LogWindow
        comboBox = self.ChooseArrow


# Global variables for original position of a moved widget and block which is dropped after a drag event
posit = None
tempBlock = None
structure = None
loggerWindow = None
comboBox = None
insideMainStruct = True
MultipleSelect = {}
archs = []
layers = []
selectedMultipleLayer = []
loggerCounter = 0
