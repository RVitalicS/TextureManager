from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from widgets import errorUI
from icons import resource


class Error(QDialog, errorUI.Ui_Error):
	def __init__(self):
		super(Error, self).__init__()
		self.setupUi(self)

		# UI
		self.setWindowIcon(QIcon(':/error.png'))

		self.setStyleSheet('''background-color: #3c3f41;''')

		self.label_complete.setStyleSheet('''color: #aaaaaa;''')

		self.button_ok.setStyleSheet('''
			QPushButton {
				border: 1px solid #aaaaaa;
				background-color:  #3c3f41;
				border-radius: 6px;
				color: #aaaaaa;
				}
			QPushButton::hover {
				border: none;
				background-color: #0099ff;
				border-radius: 6px;
				color: #ffffff;
				}
			QPushButton::pressed {
				border: none;
				background-color:  #0099ff;
				border-radius: 6px;
				color: #ffffff;
				}
			''')

		self.button_ok.clicked.connect(self.reject)
