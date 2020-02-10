from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):

    def __init__(self):
        self.centralwidget = None
        self.OutputFi = None
        self.LoadStr = None
        self.RunNN = None
        self.Input = None
        self.InputFi = None
        self.InputText = None
        self.horizontalLayoutWidget = None
        self.DataType = None
        self.Classes = None
        self.FuncAppr = None
        self.TimeSe = None
        self.Image = None
        self.CommSave = None
        self.Output = None
        self.OutputFi = None
        self.OutputText = None
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
        self.label_2 = None
        self.label_3 = None
        self.label_4 = None
        self.numberInputs = None
        self.numberOutputs = None
        self.textBrowser = None
        self.StructureFilename = None
        self.statusbar = None
        self.menubar = None
        self.toolBar = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1261, 654)
        MainWindow.setStyleSheet("background-color: white;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.FrameworkCommit = QtWidgets.QPushButton(self.centralwidget)
        self.FrameworkCommit.setGeometry(QtCore.QRect(920, 470, 101, 36))
        self.FrameworkCommit.setObjectName("FrameworkCommit")
        self.numberInputs = QtWidgets.QLineEdit(self.centralwidget)
        self.numberInputs.setGeometry(QtCore.QRect(210, 160, 71, 36))
        self.numberInputs.setObjectName("numberInputs")
        self.Log = QtWidgets.QLabel(self.centralwidget)
        self.Log.setGeometry(QtCore.QRect(300, 470, 67, 19))
        self.Log.setObjectName("Log")
        self.numberOutputs = QtWidgets.QLineEdit(self.centralwidget)
        self.numberOutputs.setGeometry(QtCore.QRect(210, 340, 71, 36))
        self.numberOutputs.setObjectName("numberOutputs")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 410, 251, 120))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.DataType = QtWidgets.QVBoxLayout(self.horizontalLayoutWidget)
        self.DataType.setContentsMargins(0, 0, 0, 0)
        self.DataType.setObjectName("DataType")
        self.Classes = QtWidgets.QRadioButton(self.horizontalLayoutWidget)
        self.Classes.setEnabled(False)
        self.Classes.setObjectName("Classes")
        self.DataType.addWidget(self.Classes)
        self.FuncAppr = QtWidgets.QRadioButton(self.horizontalLayoutWidget)
        self.FuncAppr.setEnabled(False)
        self.FuncAppr.setObjectName("FuncAppr")
        self.DataType.addWidget(self.FuncAppr)
        self.Image = QtWidgets.QRadioButton(self.horizontalLayoutWidget)
        self.Image.setEnabled(False)
        self.Image.setObjectName("Image")
        self.DataType.addWidget(self.Image)
        self.TimeSe = QtWidgets.QRadioButton(self.horizontalLayoutWidget)
        self.TimeSe.setEnabled(False)
        self.TimeSe.setObjectName("TimeSe")
        self.DataType.addWidget(self.TimeSe)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(120, 330, 91, 51))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_3.setFont(font)
        self.label_3.setScaledContents(False)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.LoadStr = QtWidgets.QPushButton(self.centralwidget)
        self.LoadStr.setEnabled(True)
        self.LoadStr.setGeometry(QtCore.QRect(660, 430, 251, 36))
        self.LoadStr.setObjectName("LoadStr")
        self.LogWindow = QtWidgets.QTextEdit(self.centralwidget)
        self.LogWindow.setGeometry(QtCore.QRect(300, 489, 611, 111))
        self.LogWindow.setObjectName("LogWindow")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(120, 150, 91, 51))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_2.setFont(font)
        self.label_2.setScaledContents(False)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(920, 520, 91, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.CommSave = QtWidgets.QPushButton(self.centralwidget)
        self.CommSave.setGeometry(QtCore.QRect(300, 430, 331, 36))
        self.CommSave.setObjectName("CommSave")
        self.Input = QtWidgets.QGroupBox(self.centralwidget)
        self.Input.setGeometry(QtCore.QRect(10, 0, 281, 151))
        self.Input.setObjectName("Input")
        self.InputText = QtWidgets.QPlainTextEdit(self.Input)
        self.InputText.setGeometry(QtCore.QRect(3, 19, 271, 131))
        self.InputText.setLineWidth(15)
        self.InputText.setObjectName("InputText")
        self.OutputFi = QtWidgets.QPushButton(self.centralwidget)
        self.OutputFi.setGeometry(QtCore.QRect(10, 340, 104, 36))
        self.OutputFi.setObjectName("OutputFi")
        self.MainStruct = QtWidgets.QWidget(self.centralwidget)
        self.MainStruct.setGeometry(QtCore.QRect(300, 20, 931, 391))
        self.MainStruct.setAcceptDrops(False)
        self.MainStruct.setAutoFillBackground(False)
        self.MainStruct.setStyleSheet("border: 1px solid black; \n"
                                      "border-radius: 10px;\n"
                                      "")
        self.MainStruct.setObjectName("MainStruct")
        self.Blocks = QtWidgets.QFrame(self.MainStruct)
        self.Blocks.setGeometry(QtCore.QRect(10, 320, 120, 61))
        self.Blocks.setStyleSheet("background-color: rgb(114, 159, 207);\n"
                                  "border: 1px solid black; \n"
                                  "border-radius: 10px;")
        self.Blocks.setLineWidth(15)
        self.Blocks.setObjectName("Blocks")
        self.ChooseArrow = QtWidgets.QComboBox(self.MainStruct)
        self.ChooseArrow.setGeometry(QtCore.QRect(160, 330, 321, 37))
        self.ChooseArrow.setStyleSheet("selection-color: black;\n"
                                       "background-color: rgb(186, 189, 182);")
        self.ChooseArrow.setObjectName("ChooseArrow")
        self.Delete = QtWidgets.QPushButton(self.MainStruct)
        self.Delete.setGeometry(QtCore.QRect(510, 330, 41, 36))
        self.Delete.setObjectName("Delete")
        self.InsertFirstBlock = QtWidgets.QLineEdit(self.MainStruct)
        self.InsertFirstBlock.setEnabled(False)
        self.InsertFirstBlock.setGeometry(QtCore.QRect(250, 160, 381, 51))
        font = QtGui.QFont()
        font.setPointSize(35)
        self.InsertFirstBlock.setFont(font)
        self.InsertFirstBlock.setStyleSheet("border-color: rgb(255, 255, 255);\n"
                                            "color: rgb(46, 52, 54);")
        self.InsertFirstBlock.setObjectName("InsertFirstBlock")
        self.LossFunction = QtWidgets.QComboBox(self.MainStruct)
        self.LossFunction.setGeometry(QtCore.QRect(710, 340, 201, 37))
        self.LossFunction.setStyleSheet("selection-color: rgb(136, 138, 133);")
        self.LossFunction.setObjectName("LossFunction")
        self.label_4 = QtWidgets.QLabel(self.MainStruct)
        self.label_4.setGeometry(QtCore.QRect(590, 350, 121, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.StructureFilename = QtWidgets.QLineEdit(self.centralwidget)
        self.StructureFilename.setGeometry(QtCore.QRect(1010, 510, 221, 36))
        self.StructureFilename.setObjectName("StructureFilename")
        self.RunNN = QtWidgets.QPushButton(self.centralwidget)
        self.RunNN.setEnabled(False)
        self.RunNN.setGeometry(QtCore.QRect(950, 430, 281, 36))
        self.RunNN.setObjectName("RunNN")
        self.Framework = QtWidgets.QComboBox(self.centralwidget)
        self.Framework.setGeometry(QtCore.QRect(1030, 470, 201, 37))
        self.Framework.setObjectName("Framework")
        self.Framework.addItem("")
        self.Framework.setStyleSheet("selection-color: black;")
        self.InputFi = QtWidgets.QPushButton(self.centralwidget)
        self.InputFi.setGeometry(QtCore.QRect(10, 160, 104, 36))
        self.InputFi.setObjectName("InputFi")
        self.Output = QtWidgets.QGroupBox(self.centralwidget)
        self.Output.setGeometry(QtCore.QRect(10, 200, 281, 141))
        self.Output.setObjectName("Output")
        self.OutputText = QtWidgets.QPlainTextEdit(self.Output)
        self.OutputText.setGeometry(QtCore.QRect(0, 20, 271, 111))
        self.OutputText.setLineWidth(15)
        self.OutputText.setObjectName("OutputText")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1261, 29))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.FrameworkCommit.setText(_translate("MainWindow", "Commit with"))
        self.numberInputs.setText(_translate("MainWindow", "10"))
        self.Log.setText(_translate("MainWindow", "Log:"))
        self.numberOutputs.setText(_translate("MainWindow", "10"))
        self.Classes.setText(_translate("MainWindow", "Classes"))
        self.FuncAppr.setText(_translate("MainWindow", "Function Aproximation"))
        self.Image.setText(_translate("MainWindow", "Image"))
        self.TimeSe.setText(_translate("MainWindow", "Time-Series"))
        self.label_3.setText(_translate("MainWindow", "or insert number of outputs:"))
        self.LoadStr.setText(_translate("MainWindow", "Load Structure"))
        self.label_2.setText(_translate("MainWindow", "or insert number of inputs:"))
        self.label.setText(_translate("MainWindow", "Structure Name"))
        self.CommSave.setText(_translate("MainWindow", "Commit n\' Save Structure"))
        self.Input.setTitle(_translate("MainWindow", "Input"))
        self.OutputFi.setText(_translate("MainWindow", "Output File"))
        self.Delete.setText(_translate("MainWindow", "Delete"))
        self.InsertFirstBlock.setText(_translate("MainWindow", "Insert first block!"))
        self.label_4.setText(_translate("MainWindow", "Loss Function:"))
        self.RunNN.setText(_translate("MainWindow", "Run NN"))
        self.Framework.setItemText(0, _translate("MainWindow", "No Framework Found"))
        self.InputFi.setText(_translate("MainWindow", "Input File"))
        self.Output.setTitle(_translate("MainWindow", "Output"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
