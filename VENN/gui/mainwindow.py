from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def __init__(self):
        self.centralwidget = None
        self.tabWidget = None
        self.tab = None
        self.tab_2 = None
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
        MainWindow.setObjectName("VENN")
        MainWindow.resize(1262, 655)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1261, 611))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.OutputFi = QtWidgets.QPushButton(self.tab)
        self.OutputFi.setGeometry(QtCore.QRect(20, 350, 104, 36))
        self.OutputFi.setObjectName("OutputFi")
        self.LoadStr = QtWidgets.QPushButton(self.tab)
        self.LoadStr.setEnabled(True)
        self.LoadStr.setGeometry(QtCore.QRect(670, 440, 251, 36))
        self.LoadStr.setObjectName("LoadStr")
        self.RunNN = QtWidgets.QPushButton(self.tab)
        self.RunNN.setEnabled(False)
        self.RunNN.setGeometry(QtCore.QRect(960, 440, 281, 36))
        self.RunNN.setObjectName("RunNN")
        self.InputFi = QtWidgets.QPushButton(self.tab)
        self.InputFi.setGeometry(QtCore.QRect(20, 170, 104, 36))
        self.InputFi.setObjectName("InputFi")
        self.Input = QtWidgets.QGroupBox(self.tab)
        self.Input.setGeometry(QtCore.QRect(20, 10, 281, 151))
        self.Input.setObjectName("Input")
        self.InputText = QtWidgets.QPlainTextEdit(self.Input)
        self.InputText.setGeometry(QtCore.QRect(3, 19, 271, 131))
        self.InputText.setLineWidth(15)
        self.InputText.setObjectName("InputText")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.tab)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 420, 251, 120))
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
        self.CommSave = QtWidgets.QPushButton(self.tab)
        self.CommSave.setGeometry(QtCore.QRect(310, 440, 331, 36))
        self.CommSave.setObjectName("CommSave")
        self.Output = QtWidgets.QGroupBox(self.tab)
        self.Output.setGeometry(QtCore.QRect(20, 210, 281, 141))
        self.Output.setObjectName("Output")
        self.OutputText = QtWidgets.QPlainTextEdit(self.Output)
        self.OutputText.setGeometry(QtCore.QRect(0, 20, 271, 111))
        self.OutputText.setLineWidth(15)
        self.OutputText.setObjectName("OutputText")
        self.MainStruct = QtWidgets.QWidget(self.tab)
        self.MainStruct.setGeometry(QtCore.QRect(310, 30, 931, 391))
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
        self.ChooseArrow.setStyleSheet("border-radius: 3px;")
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
        self.LossFunction.setObjectName("LossFunction")
        self.label_4 = QtWidgets.QLabel(self.MainStruct)
        self.label_4.setGeometry(QtCore.QRect(590, 350, 121, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.LogWindow = QtWidgets.QTextEdit(self.tab)
        self.LogWindow.setGeometry(QtCore.QRect(310, 499, 611, 61))
        self.LogWindow.setObjectName("LogWindow")
        self.Log = QtWidgets.QLabel(self.tab)
        self.Log.setGeometry(QtCore.QRect(310, 480, 67, 19))
        self.Log.setObjectName("Log")
        self.Framework = QtWidgets.QComboBox(self.tab)
        self.Framework.setGeometry(QtCore.QRect(1040, 480, 201, 37))
        self.Framework.setObjectName("Framework")
        self.Framework.addItem("")
        self.StructureFilename = QtWidgets.QLineEdit(self.tab)
        self.StructureFilename.setGeometry(QtCore.QRect(1020, 520, 221, 36))
        self.StructureFilename.setObjectName("StructureFilename")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(930, 530, 91, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.FrameworkCommit = QtWidgets.QPushButton(self.tab)
        self.FrameworkCommit.setGeometry(QtCore.QRect(930, 480, 101, 36))
        self.FrameworkCommit.setObjectName("FrameworkCommit")
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(130, 160, 91, 51))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_2.setFont(font)
        self.label_2.setScaledContents(False)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.numberInputs = QtWidgets.QLineEdit(self.tab)
        self.numberInputs.setGeometry(QtCore.QRect(220, 170, 71, 36))
        self.numberInputs.setObjectName("numberInputs")
        self.label_3 = QtWidgets.QLabel(self.tab)
        self.label_3.setGeometry(QtCore.QRect(130, 340, 91, 51))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_3.setFont(font)
        self.label_3.setScaledContents(False)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.numberOutputs = QtWidgets.QLineEdit(self.tab)
        self.numberOutputs.setGeometry(QtCore.QRect(220, 350, 71, 36))
        self.numberOutputs.setObjectName("numberOutputs")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.textBrowser = QtWidgets.QTextBrowser(self.tab_2)
        self.textBrowser.setGeometry(QtCore.QRect(40, 40, 1171, 391))
        self.textBrowser.setObjectName("textBrowser")
        self.tabWidget.addTab(self.tab_2, "")
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
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.OutputFi.setText(_translate("MainWindow", "Output File"))
        self.LoadStr.setText(_translate("MainWindow", "Load Structure"))
        self.RunNN.setText(_translate("MainWindow", "Run NN"))
        self.InputFi.setText(_translate("MainWindow", "Input File"))
        self.Input.setTitle(_translate("MainWindow", "Input"))
        self.Classes.setText(_translate("MainWindow", "Classes"))
        self.FuncAppr.setText(_translate("MainWindow", "Function Aproximation"))
        self.Image.setText(_translate("MainWindow", "Image"))
        self.TimeSe.setText(_translate("MainWindow", "Time-Series"))
        self.CommSave.setText(_translate("MainWindow", "Commit n\' Save Structure"))
        self.Output.setTitle(_translate("MainWindow", "Output"))
        self.Delete.setText(_translate("MainWindow", "Delete"))
        self.InsertFirstBlock.setText(_translate("MainWindow", "Insert first block!"))
        self.label_4.setText(_translate("MainWindow", "Loss Function:"))
        self.Log.setText(_translate("MainWindow", "Log:"))
        self.Framework.setItemText(0, _translate("MainWindow", "No Framework Found"))
        self.label.setText(_translate("MainWindow", "Structure Name"))
        self.FrameworkCommit.setText(_translate("MainWindow", "Commit with"))
        self.label_2.setText(_translate("MainWindow", "or insert number of inputs:"))
        self.numberInputs.setText(_translate("MainWindow", "10"))
        self.label_3.setText(_translate("MainWindow", "or insert number of outputs:"))
        self.numberOutputs.setText(_translate("MainWindow", "10"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Let\'s Roll"))
        self.textBrowser.setHtml(_translate("MainWindow",
                                            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                            "p, li { white-space: pre-wrap; }\n"
                                            "</style></head><body style=\" font-family:\'Cantarell\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">How it works</p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">...</p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Next on the TODO list</p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">...</p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Who I am</p>\n"
                                            "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">...</p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "QA"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
