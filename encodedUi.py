from qtpy import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    """ Class for the UI of the main window.

    This class is designed to provide the layout of the main user
    interface window. This window was written following the QtPy
    UI framework. The basic layout of this window contains several
    buttons in order to upload files to the server, open images that
    have been previously been uploaded as well as process the spots to
    understand the test results.

    """
    def setupUi(self, MainWindow):
        """ Method setting up the locations and layout of UI

        This method is utilized to set up the location and visualization
        of the main user interface. All buttons, labels, and functionalities
        are set here. This method can be called to set up the GUI upon calling
        the class.

        Args:
            MainWindow (class) = Class cooresponding to the main UI
                window.

        Returns:
            None

        """

        # Main window init/size
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 800)

        # Various button and plotting widgets
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.verticalLayout.setObjectName("verticalLayout")
        self.plotting_widget = QtWidgets.QWidget(self.centralwidget)
        self.plotting_widget.setObjectName("plotting_widget")
        self.verticalLayout.addWidget(self.plotting_widget)

        self.topDialogBox = QtWidgets.QLabel(self.centralwidget)
        self.topDialogBox.setObjectName("topDialogBox")
        self.topDialogBox.setAlignment(QtCore.Qt.AlignCenter)
        self.topDialogBox.setMaximumHeight(20)
        self.verticalLayout.addWidget(self.topDialogBox)

        self.bottomDialogBox = QtWidgets.QLabel(self.centralwidget)
        self.bottomDialogBox.setObjectName("bottomDialogBox")
        self.bottomDialogBox.setAlignment(QtCore.Qt.AlignCenter)
        self.bottomDialogBox.setMaximumHeight(45)
        self.verticalLayout.addWidget(self.bottomDialogBox)

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)

        self.readImgButton = QtWidgets.QPushButton(self.centralwidget)
        self.readImgButton.setObjectName("readImgButton")
        self.verticalLayout.addWidget(self.readImgButton)
        
        self.analyzeImgButton = QtWidgets.QPushButton(self.centralwidget)
        self.analyzeImgButton.setObjectName("analyzeImgButton")
        self.verticalLayout.addWidget(self.analyzeImgButton)

        self.saveImgButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveImgButton.setObjectName("saveImgButton")
        self.verticalLayout.addWidget(self.saveImgButton)

        self.horizontalLayout.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 17))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # Call retranslate method to add text labels
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        """ Method adding text onto the various widgets

        This method is designed to add text to the the various
        widgets that were defied in the Ui_MainWindow class. These
        buttons allow for user interactions with the server.

        Args:
            MainWindow (class) = Class cooresponding to the main UI
                window.

        Returns:
            None

        """
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate(
            "", "D4Scope Camera Software", None, -1))
        self.readImgButton.setText(QtWidgets.QApplication.translate(
            "", "Capture Image", None, -1))
        self.analyzeImgButton.setText(QtWidgets.QApplication.translate(
            "", "Analyze Image", None, -1))
        self.topDialogBox.setText(QtWidgets.QApplication.translate(
            "", "Press 'Capture Image' button", None, -1))
        self.saveImgButton.setText(QtWidgets.QApplication.translate(
            "", "Save Image", None, -1))