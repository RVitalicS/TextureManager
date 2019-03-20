from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from widgets import mainUI, listUI
from icons import resource
import builders, settings
import os

style = os.path.join(os.path.dirname(__file__), 'style.css')


class Interface(QMainWindow, mainUI.Ui_TextureManager):
	def __init__(self):
		super(Interface, self).__init__()
		self.setupUi(self)

		self.setStyleSheet(open(style).read())

		self.focused_data = None
		self.newer_switch = False
		self.list_arguments = [
			[
				self.button_none,
				self.button_disabled,
				self.button_up,
				self.button_up_,
				self.button_down,
				self.button_down_,
				self.button_round,
				self.button_round_
			],
			[
				self.button_black,
				self.button_clamp,
				self.button_periodic
			],
			[
				self.button_single,
				self.button_diagonal,
				self.button_all
			],
			[
				self.button_tiff,
				self.button_pixar,
				self.button_openexr
			],
			[
				self.button_byte,
				self.button_short,
				self.button_half,
				self.button_float
			]
		]

		self.buttons_list_cmd = [
			self.button_add,
			self.button_remove,
			self.button_clear,
			self.button_defaults
		]

		# UI
		self.setWindowIcon(QIcon(':/icon_16x16.png'))
		self.button_switch.setIconSize(QSize(32, 20))

		self.item_list = listUI.ItemList()
		self.item_list.setViewportMargins(25, 15, 5, 18)
		self.item_list.setFrameShape(QFrame.NoFrame)

		font = QFont()
		font.setFamily("Segoe UI")
		font.setPointSize(11)
		self.item_list.setFont(font)
		self.layout_list_main.addWidget(self.item_list)

		self.layout_labels = QHBoxLayout()
		self.layout_labels.setSpacing(0)
		self.layout_labels.setContentsMargins(0, 0, 0, 0)
		self.layout_list_main.addLayout(self.layout_labels)

		self.label_path = QLabel()
		self.label_path.setIndent(18)
		self.label_path.setMargin(10)
		font.setPointSize(10)
		self.label_path.setObjectName('label_path')
		self.label_path.setFont(font)
		self.label_path.setAlignment(Qt.AlignVCenter)
		self.layout_labels.addWidget(self.label_path)

		self.label_size = QLabel()
		self.label_size.setIndent(10)
		self.label_size.setMargin(10)
		self.label_size.setText('')
		font.setPointSize(8)
		self.label_size.setObjectName('label_size')
		self.label_size.setFont(font)
		self.label_size.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
		self.layout_labels.addWidget(self.label_size)

		self.button_run.setObjectName('start')

		# connects
		self.button_switch.pressed.connect(self.ui_switch_on)
		self.button_switch.clicked.connect(self.ui_switch_off)

		# start
		self.ui_buttons_arg_on()
		self.ui_buttons_list()
		self.ui_button_loaded_not()
		self.ui_console_off()

	def ui_switch_on(self):
		self.button_switch.setIcon(QIcon(':/switch_on.png'))
		self.newer_switch = True

	def ui_switch_off(self):
		if not self.button_switch.isChecked():
			self.button_switch.setIcon(QIcon(':/switch_off.png'))
			self.newer_switch = False

	def ui_console_on(self):
		self.console = True
		self.line_arguments.setFixedHeight(30)
		with open(os.path.normpath(os.path.join(os.path.dirname(__file__), 'doc\help.txt'))) as file:
			help_arg = file.read()
		self.line_arguments.setToolTip('''{}'''.format(help_arg))
		self.line_arguments.setObjectName('console_on')
		self.line_arguments.setStyleSheet('')

	def ui_console_off(self):
		self.console = False
		self.line_arguments.setFixedHeight(20)
		self.line_arguments.setObjectName('console_off')
		self.line_arguments.setStyleSheet('')
		self.line_arguments.setToolTip(None)

	def ui_buttons_arg_on(self):
		self.button_disabled.setDisabled(1)
		for group in self.list_arguments:
			for button in group:
				button.setDisabled(0)
				button.setObjectName('button_arg_on')
				button.setStyleSheet('')

	def ui_buttons_arg_off(self):
		self.button_disabled.setDisabled(1)
		for group in self.list_arguments:
			for button in group:
				button.setDisabled(1)
				button.setObjectName('button_arg_off')
				button.setStyleSheet('')

	def ui_button_loaded(self):
		self.button_load.setText('txmake.exe')
		self.button_load.setObjectName('txmake_loaded')
		self.button_load.setStyleSheet('')

	def ui_button_loaded_not(self):
		self.button_load.setText('Find txmake.exe')
		self.button_load.setObjectName('txmake_loaded_not')
		self.button_load.setStyleSheet('')

	def ui_buttons_list(self):
		for button in self.buttons_list_cmd:
			button.setObjectName('command_button')
			button.setStyleSheet('')

	def focus_label(self, item):
		if item:
			if self.item_list.hasFocus():
				if os.path.exists(item.data(Qt.UserRole)):
					self.label_path.setText(item.data(Qt.UserRole))
					self.focused_data = item.data(Qt.UserRole)
				self.items_update()

	def items_update(self):
		selected_items = self.item_list.selectedItems()
		selected_data = [i.data(Qt.UserRole) for i in selected_items]

		item_in = 0
		if settings.Settings().load()['items']:
			item_in = len(settings.Settings().load()['items'])

		for row in range(self.item_list.count()):
			item = self.item_list.item(row)

			if not os.path.exists(item.data(Qt.UserRole)):
				with settings.SettingsManager() as data:
					if item.data(Qt.UserRole) in data['items']:
						data['items'].remove(item.data(Qt.UserRole))
				self.focused_data = None

			elif os.path.splitext(item.data(Qt.UserRole))[-1]:
				if self.newer_switch and builders.older_tex(item.data(Qt.UserRole)):
					item.setIcon(QIcon(':/image_has_tex.png'))
					item.setData(Qt.ForegroundRole, QColor('#aaaaaa'))
				else:
					item.setIcon(QIcon(':/image.png'))
					item.setData(Qt.ForegroundRole, QColor('#3c3f41'))

			else:
				if self.newer_switch and builders.older_tex(item.data(Qt.UserRole)):
					item.setIcon(QIcon(':/folder_has_tex.png'))
					item.setData(Qt.ForegroundRole, QColor('#aaaaaa'))
				else:
					item.setIcon(QIcon(':/folder.png'))
					item.setData(Qt.ForegroundRole, QColor('#3c3f41'))

		item_out = 0
		if settings.Settings().load()['items']:
			item_out = len(settings.Settings().load()['items'])

		for item in selected_items:
			if os.path.splitext(item.data(Qt.UserRole))[-1]:
				item.setIcon(QIcon(':/image_selected.png'))
			else:
				item.setIcon(QIcon(':/folder_selected.png'))

		if self.focused_data:
			size = builders.get_size(self.focused_data, selected_data)
			size_tex = builders.get_size_tex(self.focused_data)
			if size_tex and self.newer_switch and builders.older_tex(self.focused_data):
				size = '<span style="color:#aaaaaa;">%s</span> &nbsp; %s' % (size_tex, size)
			self.label_size.setText(size)

		if not selected_items:
			self.item_list.clearFocus()
			self.label_path.setText('')
			self.label_size.setText('')
			self.button_run.setProperty('selected', 'False')
			self.button_run.setStyleSheet('')
		else:
			self.button_run.setProperty('selected', 'True')
			self.button_run.setStyleSheet('')

		if item_in > item_out:
			self.item_list.clear()
			self.ui_load()


if __name__ == '__main__':
	application = QApplication([])
	widget = Interface()
	widget.show()
	application.exec_()
