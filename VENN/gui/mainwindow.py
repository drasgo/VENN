from PyQt5 import QtCore, QtGui, QtWidgets


# TODO
# Add whatsthis tooltip to every sensible label/combobox


class Ui_MainWindow(object):

    def __init__(self):
        self.centralwidget = None
        self.LoadStr = None
        self.RunNN = None
        self.InputFi = None
        self.CommSave = None
        self.OutputFi = None
        self.MainStruct = None
        self.Blocks = None
        self.ChooseArrow = None
        self.Delete = None
        self.InsertFirstBlock = None
        self.LossFunction = None
        self.Log = None
        self.LogWindow = None
        self.Framework = None
        self.FrameworkCommit = None
        self.label = None
        self.numberInputs = None
        self.numberOutputs = None
        self.StructureFilename = None
        self.nOutputs = None
        self.nInputs = None
        self.Loss = None
        self.TestNN = None
        self.Epochs = None
        self.numberEpochs = None
        self.OptimizerFunction = None
        self.Optmizer = None
        self.InputFile = None
        self.OutputFile = None
        self.AdvancedOptions = None
        self.NumberOutputs = None
        self.NumberInputs = None
        self.line_2 = None
        self.line_3 = None
        self.line_4 = None
        self.line_5 = None
        self.line_6 = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1261, 607)
        MainWindow.setMinimumSize(QtCore.QSize(1261, 607))
        MainWindow.setWindowOpacity(0.0)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.FrameworkCommit = QtWidgets.QPushButton(self.centralwidget)
        self.FrameworkCommit.setGeometry(QtCore.QRect(850, 430, 171, 31))
        self.FrameworkCommit.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.FrameworkCommit.setStyleSheet("border: 1px solid black; \n"
                                           "border-radius: 10px;")
        self.FrameworkCommit.setObjectName("FrameworkCommit")
        self.Log = QtWidgets.QLabel(self.centralwidget)
        self.Log.setGeometry(QtCore.QRect(10, 460, 67, 19))
        self.Log.setObjectName("Log")
        self.nOutputs = QtWidgets.QLabel(self.centralwidget)
        self.nOutputs.setGeometry(QtCore.QRect(11, 181, 139, 71))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.nOutputs.setFont(font)
        self.nOutputs.setScaledContents(False)
        self.nOutputs.setWordWrap(True)
        self.nOutputs.setObjectName("nOutputs")
        self.LoadStr = QtWidgets.QPushButton(self.centralwidget)
        self.LoadStr.setEnabled(True)
        self.LoadStr.setGeometry(QtCore.QRect(570, 430, 251, 31))
        self.LoadStr.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.LoadStr.setStyleSheet("border: 1px solid black; \n"
                                   "border-radius: 10px;\n"
                                   "")
        self.LoadStr.setObjectName("LoadStr")
        self.LogWindow = QtWidgets.QTextEdit(self.centralwidget)
        self.LogWindow.setGeometry(QtCore.QRect(10, 480, 651, 111))
        self.LogWindow.setObjectName("LogWindow")
        self.nInputs = QtWidgets.QLabel(self.centralwidget)
        self.nInputs.setGeometry(QtCore.QRect(11, 50, 130, 71))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.nInputs.setFont(font)
        self.nInputs.setScaledContents(False)
        self.nInputs.setWordWrap(True)
        self.nInputs.setObjectName("nInputs")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(880, 560, 121, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.CommSave = QtWidgets.QPushButton(self.centralwidget)
        self.CommSave.setGeometry(QtCore.QRect(300, 430, 261, 31))
        self.CommSave.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.CommSave.setStyleSheet("border: 1px solid black; \n"
                                    "border-radius: 10px;")
        self.CommSave.setObjectName("CommSave")
        self.OutputFi = QtWidgets.QPushButton(self.centralwidget)
        self.OutputFi.setGeometry(QtCore.QRect(11, 147, 111, 21))
        self.OutputFi.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.OutputFi.setStyleSheet("border: 1px solid black; \n"
                                    "border-radius: 10px;")
        self.OutputFi.setObjectName("OutputFi")
        self.MainStruct = QtWidgets.QWidget(self.centralwidget)
        self.MainStruct.setGeometry(QtCore.QRect(300, 10, 931, 411))
        self.MainStruct.setAcceptDrops(False)
        self.MainStruct.setAutoFillBackground(False)
        self.MainStruct.setStyleSheet("border: 1px solid black; \n"
                                      "border-radius: 10px;\n"
                                      "")
        self.MainStruct.setObjectName("MainStruct")
        self.Blocks = QtWidgets.QFrame(self.MainStruct)
        self.Blocks.setGeometry(QtCore.QRect(10, 340, 120, 61))
        self.Blocks.setStyleSheet("background-color: rgb(114, 159, 207);\n"
                                  "border: 1px solid black; \n"
                                  "border-radius: 10px;")
        self.Blocks.setLineWidth(15)
        self.Blocks.setObjectName("Blocks")
        self.ChooseArrow = QtWidgets.QComboBox(self.MainStruct)
        self.ChooseArrow.setGeometry(QtCore.QRect(150, 350, 321, 37))
        self.ChooseArrow.setStyleSheet("border: 1px solid black; \n"
                                       "border-radius: 6px;\n"
                                       "selection-color: rgb(136, 138, 133);\n"
                                       "background-color: rgb(186, 189, 182);")
        self.ChooseArrow.setObjectName("ChooseArrow")
        self.Delete = QtWidgets.QPushButton(self.MainStruct)
        self.Delete.setGeometry(QtCore.QRect(490, 350, 41, 36))
        self.Delete.setObjectName("Delete")
        self.InsertFirstBlock = QtWidgets.QLineEdit(self.MainStruct)
        self.InsertFirstBlock.setEnabled(False)
        self.InsertFirstBlock.setGeometry(QtCore.QRect(280, 180, 381, 51))
        font = QtGui.QFont()
        font.setPointSize(32)
        self.InsertFirstBlock.setFont(font)
        self.InsertFirstBlock.setStyleSheet("border-color: rgb(255, 255, 255);\n"
                                            "color: rgb(46, 52, 54);")
        self.InsertFirstBlock.setObjectName("InsertFirstBlock")
        self.StructureFilename = QtWidgets.QLineEdit(self.centralwidget)
        self.StructureFilename.setGeometry(QtCore.QRect(1010, 550, 221, 36))
        self.StructureFilename.setStyleSheet("border: 1px solid black; \n"
                                             "border-radius: 10px;")
        self.StructureFilename.setObjectName("StructureFilename")
        self.RunNN = QtWidgets.QPushButton(self.centralwidget)
        self.RunNN.setEnabled(True)
        self.RunNN.setGeometry(QtCore.QRect(680, 480, 261, 36))
        self.RunNN.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.RunNN.setStyleSheet("border: 1px solid black; \n"
                                 "border-radius: 10px;\n"
                                 "")
        self.RunNN.setObjectName("RunNN")
        self.Framework = QtWidgets.QComboBox(self.centralwidget)
        self.Framework.setGeometry(QtCore.QRect(1030, 430, 201, 31))
        self.Framework.setStyleSheet("border: 1px solid black; \n"
                                     "border-radius: 6px;")
        self.Framework.setObjectName("Framework")
        self.Framework.addItem("")
        self.InputFi = QtWidgets.QPushButton(self.centralwidget)
        self.InputFi.setGeometry(QtCore.QRect(11, 18, 111, 21))
        self.InputFi.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.InputFi.setMouseTracking(True)
        self.InputFi.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.InputFi.setStyleSheet("border: 1px solid black; \n"
                                   "border-radius: 10px;")
        self.InputFi.setObjectName("InputFi")
        self.LossFunction = QtWidgets.QComboBox(self.centralwidget)
        self.LossFunction.setGeometry(QtCore.QRect(130, 350, 161, 23))
        self.LossFunction.setStyleSheet("border: 1px solid black; \n"
                                        "border-radius: 6px;\n"
                                        "")
        self.LossFunction.setObjectName("LossFunction")
        self.Loss = QtWidgets.QLabel(self.centralwidget)
        self.Loss.setGeometry(QtCore.QRect(10, 340, 111, 51))
        font = QtGui.QFont()
        font.setFamily("Cantarell")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.Loss.setFont(font)
        self.Loss.setObjectName("Loss")
        self.TestNN = QtWidgets.QPushButton(self.centralwidget)
        self.TestNN.setEnabled(True)
        self.TestNN.setGeometry(QtCore.QRect(970, 480, 261, 36))
        self.TestNN.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.TestNN.setStyleSheet("border: 1px solid black; \n"
                                  "border-radius: 10px;")
        self.TestNN.setObjectName("TestNN")
        self.Epochs = QtWidgets.QLabel(self.centralwidget)
        self.Epochs.setGeometry(QtCore.QRect(11, 263, 128, 61))
        font = QtGui.QFont()
        font.setFamily("Cantarell")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.Epochs.setFont(font)
        self.Epochs.setScaledContents(False)
        self.Epochs.setWordWrap(True)
        self.Epochs.setObjectName("Epochs")
        self.numberEpochs = QtWidgets.QLineEdit(self.centralwidget)
        self.numberEpochs.setGeometry(QtCore.QRect(159, 273, 131, 27))
        self.numberEpochs.setStyleSheet("border: 1px solid black; \n"
                                        "border-radius: 10px;\n"
                                        "")
        self.numberEpochs.setObjectName("numberEpochs")
        self.Optmizer = QtWidgets.QLabel(self.centralwidget)
        self.Optmizer.setGeometry(QtCore.QRect(6, 398, 141, 51))
        font = QtGui.QFont()
        font.setFamily("Cantarell")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.Optmizer.setFont(font)
        self.Optmizer.setObjectName("Optmizer")
        self.OptimizerFunction = QtWidgets.QComboBox(self.centralwidget)
        self.OptimizerFunction.setGeometry(QtCore.QRect(153, 409, 141, 23))
        self.OptimizerFunction.setStyleSheet("border: 1px solid black; \n"
                                             "border-radius: 6px;\n"
                                             "\n"
                                             "")
        self.OptimizerFunction.setObjectName("OptimizerFunction")
        self.InputFile = QtWidgets.QLineEdit(self.centralwidget)
        self.InputFile.setGeometry(QtCore.QRect(127, 15, 161, 27))
        self.InputFile.setStyleSheet("border: 1px solid black; \n"
                                     "border-radius: 10px;\n"
                                     "")
        self.InputFile.setText("")
        self.InputFile.setObjectName("InputFile")
        self.OutputFile = QtWidgets.QLineEdit(self.centralwidget)
        self.OutputFile.setGeometry(QtCore.QRect(127, 144, 161, 27))
        self.OutputFile.setStyleSheet("border: 1px solid black; \n"
                                      "border-radius: 10px;\n"
                                      "")
        self.OutputFile.setText("")
        self.OutputFile.setObjectName("OutputFile")
        self.AdvancedOptions = QtWidgets.QPushButton(self.centralwidget)
        self.AdvancedOptions.setEnabled(False)
        self.AdvancedOptions.setGeometry(QtCore.QRect(680, 540, 171, 51))
        self.AdvancedOptions.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.AdvancedOptions.setStyleSheet("border: 1px solid black; \n"
                                           "border-radius: 10px;\n"
                                           "")
        self.AdvancedOptions.setObjectName("AdvancedOptions")
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setGeometry(QtCore.QRect(11, 320, 281, 16))
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.NumberOutputs = QtWidgets.QLineEdit(self.centralwidget)
        self.NumberOutputs.setGeometry(QtCore.QRect(159, 197, 131, 27))
        self.NumberOutputs.setStyleSheet("border: 1px solid black; \n"
                                         "border-radius: 10px;\n"
                                         "")
        self.NumberOutputs.setText("")
        self.NumberOutputs.setObjectName("NumberOutputs")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(11, 121, 281, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_5 = QtWidgets.QFrame(self.centralwidget)
        self.line_5.setGeometry(QtCore.QRect(11, 386, 271, 16))
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setGeometry(QtCore.QRect(11, 250, 281, 16))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.NumberInputs = QtWidgets.QLineEdit(self.centralwidget)
        self.NumberInputs.setGeometry(QtCore.QRect(159, 68, 131, 27))
        self.NumberInputs.setStyleSheet("border: 1px solid black; \n"
                                        "border-radius: 10px;\n"
                                        "")
        self.NumberInputs.setText("")
        self.NumberInputs.setObjectName("NumberInputs")
        self.line_6 = QtWidgets.QFrame(self.centralwidget)
        self.line_6.setGeometry(QtCore.QRect(10, 450, 271, 16))
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "VENN- Visual Editor of Neural Networks"))
        self.FrameworkCommit.setText(_translate("MainWindow", "Commit Model with"))
        self.Log.setText(_translate("MainWindow", "Logger:"))
        self.nOutputs.setText(_translate("MainWindow", "<b>or insert number of outputs</b>"))
        self.LoadStr.setText(_translate("MainWindow", "Load Structure"))
        self.nInputs.setText(_translate("MainWindow", "<b>or insert number of inputs:</b>"))
        self.label.setText(_translate("MainWindow", "Structure Name"))
        self.CommSave.setText(_translate("MainWindow", "Commit n\' Save Structure"))
        self.OutputFi.setText(_translate("MainWindow", "Output File"))
        self.Delete.setText(_translate("MainWindow", "Delete"))
        self.InsertFirstBlock.setText(_translate("MainWindow", "Insert first block!"))
        self.StructureFilename.setText(_translate("MainWindow", "NNStructure"))
        self.RunNN.setText(_translate("MainWindow", "Train Model"))
        self.Framework.setItemText(0, _translate("MainWindow", "No Framework Found"))
        self.InputFi.setText(_translate("MainWindow", "Input File"))
        self.Loss.setText(_translate("MainWindow", "<b>Loss Function:</b>"))
        self.TestNN.setText(_translate("MainWindow", "Train + Test Model"))
        self.Epochs.setText(_translate("MainWindow", "<b>Number of epochs:</b>"))
        self.numberEpochs.setText(_translate("MainWindow", "1"))
        self.Optmizer.setText(_translate("MainWindow", "<b>Optimizer Function:</b>"))
        self.AdvancedOptions.setText(_translate("MainWindow", "Advanced Options"))
