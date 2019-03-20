from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import interface, settings, builders
import os


class TexConverter(interface.Interface):
	def __init__(self):
		super(TexConverter, self).__init__()

		# start
		self.button_arguments_connect()
		self.ui_load()
		self.items_update()

		# connects
		self.button_add.clicked.connect(self.add)
		self.button_remove.clicked.connect(self.remove)
		self.button_clear.clicked.connect(self.clear)
		self.button_defaults.clicked.connect(self.defaults)
		self.button_load.clicked.connect(self.load_txmake)
		self.button_save_locally.clicked.connect(self.save_locally)
		self.button_save_directly.clicked.connect(self.save_directly)
		self.button_switch.clicked.connect(self.switch)
		self.line_arguments.editingFinished.connect(self.console_write)
		self.item_list.itemSelectionChanged.connect(self.items_update)
		self.item_list.itemPressed.connect(self.focus_label)
		self.item_list.itemEntered.connect(self.focus_label)
		self.button_run.clicked.connect(self.convert)

		self.item_list.list_updated.connect(self.ui_update)

	def button_arguments_connect(self):
		for group in self.list_arguments:
			for button in group:
				button.pressed.connect(self.group_uncheck)
				button.released.connect(self.write_arguments)

	def ui_load(self):
		data = settings.Settings().load()
		if data['items']:
			for path in data['items']:
				builders.build_item(self.item_list, path)
		self.ui_update()

	def ui_update(self):
		data = settings.Settings().load()

		for group in self.list_arguments:
			for button in group:
				if button.text() in data['arguments']:
					button.setChecked(1)

		if data['newer']:
			self.ui_switch_on()
		else:
			self.ui_switch_off()

		if not data['console'] or not self.line_arguments.text():
			self.line_arguments.setText(settings.console_message)
			self.ui_console_off()
			self.ui_buttons_arg_on()
			self.settings_enable()
			self.line_arguments.cursorPositionChanged.connect(self.console_clean)
		else:
			self.line_arguments.setText(data['console'])
			self.ui_console_on()
			self.ui_buttons_arg_off()
			self.settings_disable()

		if data['directory']:
			self.label_directory.setText(data['directory'])
		else:
			self.label_directory.setText(settings.directory_label)

		if data['txmake']:
			self.ui_button_loaded()
			if not data['console']:
				self.ui_enable()
		else:
			self.ui_button_loaded_not()
			self.ui_disable()

		if data['items']:
			self.settings_enable()
			self.ui_buttons_arg_on()
		else:
			self.settings_disable()
			self.ui_buttons_arg_off()

	def group_uncheck(self):
		for group in self.list_arguments:
			for button in group:
				if button.isDown():
					for all_buttons in group:
						all_buttons.setChecked(0)

	def write_arguments(self):
		arguments = []
		for group in self.list_arguments:
			for button in group:
				if button.isChecked():
					arguments.append(button.text())
		with settings.SettingsManager() as data:
			data['arguments'] = arguments

	def console_clean(self):
		self.line_arguments.cursorPositionChanged.disconnect(self.console_clean)
		if not self.console:
			self.line_arguments.clear()
			self.ui_console_on()
			self.ui_buttons_arg_off()
			self.settings_disable()

	def console_write(self):
		with settings.SettingsManager() as data:
			arguments_new = builders.correct_name(self.line_arguments.text())
			self.line_arguments.setText(arguments_new)
			if arguments_new:
				data['console'] = arguments_new
			else:
				data['console'] = None
		self.ui_update()

	def add(self):
		path = os.path.expanduser('~')
		message = 'Select Files'
		explorer = QFileDialog.getOpenFileNames(self, message, path)
		if explorer[0]:
			for path in explorer[0]:
				self.item_list.add_items(path)

	def remove(self):
		self.item_list.delete_selected()

	def clear(self):
		with settings.SettingsManager() as data:
			data['items'] = None
		self.item_list.clear()
		self.ui_update()

	def defaults(self):
		default_data = settings.Settings().default_data
		with settings.SettingsManager() as data:
			data['console'] = default_data['console']
			data['arguments'] = default_data['arguments']
			data['newer'] = default_data['newer']
		for group in self.list_arguments:
			for button in group:
				button.setChecked(0)
		self.button_switch.setChecked(0)
		self.ui_update()

	def load_txmake(self):
		with settings.SettingsManager() as data:
			path = r'C:\Program Files\Pixar'
			message = 'Find txmake.exe'
			if data['txmake']:
				path = data['txmake']
				message = 'Change txmake.exe'
			if not os.path.exists(path):
				path = os.path.expanduser('~')
			_filter = 'txmake.exe'
			explorer = QFileDialog.getOpenFileName(self, message, path, _filter)[0]
			if explorer:
				data['txmake'] = explorer
		self.ui_update()

	def save_locally(self):
		with settings.SettingsManager() as data:
			data['directory'] = None
		self.ui_update()

	def save_directly(self):
		with settings.SettingsManager() as data:
			path = os.path.expanduser('~')
			if data['directory']:
				path = data['directory']
			message = 'Set Folder'
			explorer = QFileDialog.getExistingDirectory(self, message, path)
			if explorer:
				data['directory'] = explorer
		self.ui_update()

	def convert(self):
		self.label_size.clear()
		selection = [item.data(Qt.UserRole) for item in self.item_list.selectedItems()]
		if builders.convert(self.progress_bar, self.label_path, selection):
			self.ui_update()
			self.items_update()
			self.label_path.setText('<span style="color:#fbae17;"><b>DONE</b></span>')

	def settings_disable(self):
		for group in self.list_arguments:
			for button in group:
				button.setDisabled(1)
		self.button_switch.setDisabled(1)

	def settings_enable(self):
		for group in self.list_arguments:
			for button in group:
				button.setEnabled(1)
		self.button_switch.setEnabled(1)

	def switch(self):
		with settings.SettingsManager() as data:
			if self.button_switch.isChecked():
				data['newer'] = True
			else:
				data['newer'] = False
		self.items_update()
		self.ui_update()

	def ui_disable(self):
		self.settings_disable()
		self.ui_buttons_arg_off()
		for button in self.buttons_list_cmd:
			button.setDisabled(1)
		self.item_list.setDisabled(1)
		self.line_arguments.setDisabled(1)
		self.button_save_locally.setDisabled(1)
		self.button_save_directly.setDisabled(1)
		self.button_run.setDisabled(1)

	def ui_enable(self):
		self.settings_enable()
		self.ui_buttons_arg_on()
		for button in self.buttons_list_cmd:
			button.setEnabled(1)
		self.item_list.setEnabled(1)
		self.line_arguments.setEnabled(1)
		self.button_save_locally.setEnabled(1)
		self.button_save_directly.setEnabled(1)
		self.button_run.setEnabled(1)


if __name__ == '__main__':
	application = QApplication([])
	widget = TexConverter()
	widget.show()
	application.exec_()
