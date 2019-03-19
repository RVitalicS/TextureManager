from PySide import QtCore, QtGui


class Ui_Error(object):
    def setupUi(self, Message):
        Message.setObjectName("Error")
        Message.resize(400, 200)
        self.verticalLayout = QtGui.QVBoxLayout(Message)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setContentsMargins(30, 30, 30, 20)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_complete = QtGui.QLabel(Message)
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(8)
        self.label_complete.setFont(font)
        self.label_complete.setText("")
        self.label_complete.setAlignment(QtCore.Qt.AlignLeft)
        self.label_complete.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label_complete.setObjectName("label_complete")
        self.verticalLayout.addWidget(self.label_complete)
        self.layout_button = QtGui.QHBoxLayout()
        self.layout_button.setSpacing(0)
        self.layout_button.setContentsMargins(-1, 0, -1, -1)
        self.layout_button.setObjectName("layout_button")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.layout_button.addItem(spacerItem)
        self.button_ok = QtGui.QPushButton(Message)
        self.button_ok.setMinimumSize(QtCore.QSize(80, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI Black")
        font.setPointSize(14)
        self.button_ok.setFont(font)
        self.button_ok.setFlat(True)
        self.button_ok.setObjectName("button_ok")
        self.layout_button.addWidget(self.button_ok)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.layout_button.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.layout_button)

        self.retranslateUi(Message)
        QtCore.QMetaObject.connectSlotsByName(Message)

    def retranslateUi(self, Message):
        Message.setWindowTitle(QtGui.QApplication.translate("Error", "Error", None, QtGui.QApplication.UnicodeUTF8))
        self.button_ok.setText(QtGui.QApplication.translate("Error", "OK", None, QtGui.QApplication.UnicodeUTF8))

