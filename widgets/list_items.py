from PySide.QtCore import *
from PySide.QtGui import *
import os, webbrowser
import settings, builders


class ItemList(QListWidget):
	list_updated = Signal()

	def __init__(self):
		super(ItemList, self).__init__()
		self.setDragDropMode(QAbstractItemView.DropOnly)
		self.setSelectionMode(QAbstractItemView.ExtendedSelection)

		self.key_ctrl = False

		# connects
		self.itemDoubleClicked.connect(self.open_item)

	def dragEnterEvent(self, event):
		if event.source() is self:
			event.ignore()
		else:
			if event.mimeData().hasUrls():
				event.accept()
			else:
				event.ignore()

	def dragMoveEvent(self, event):
		if event.source() is self:
			event.ignore()
		else:
			if event.mimeData().hasUrls():
				event.accept()
			else:
				event.ignore()

	def dropEvent(self, event):
		mime_data = event.mimeData()
		if mime_data.hasUrls():
			for file in mime_data.urls():
				self.add_items(file.toLocalFile())

	def mousePressEvent(self, event):
		if event.button() == Qt.MouseButton.RightButton:
			super(ItemList, self).mousePressEvent(event)
		if event.button() == Qt.MouseButton.MiddleButton:
			self.clearSelection()
		if event.button() == Qt.MouseButton.LeftButton:
			super(ItemList, self).mousePressEvent(event)

	def keyPressEvent(self, key_event):
		if key_event.key() == Qt.Key_Delete:
			self.delete_selected()
		if key_event == QKeySequence.SelectAll:
			self.selectAll()
		if key_event.key() == Qt.Key_Control:
			self.setProperty('ctrl', 'True')
			self.setStyleSheet('')
			self.key_ctrl = True

	def keyReleaseEvent(self, key_event):
		if key_event.key() == Qt.Key_Control:
			self.setProperty('ctrl', 'False')
			self.setStyleSheet('')
			self.key_ctrl = False

	def add_items(self, path):
		path = builders.correct_extensions(path)
		if path:
			with settings.SettingsManager() as data:
				if not data['items']:
					builders.build_item(self, path)
					data['items'] = [path]
				elif path not in data['items']:
					data['items'].append(path)
					data['items'].sort(key=lambda x: os.path.splitext(x)[-1])
					self.clear()
					for item in data['items']:
						builders.build_item(self, item)
		self.list_updated.emit()

	def delete_selected(self):
		with settings.SettingsManager() as data:
			for item in self.selectedItems():
				data['items'].remove(item.data(32))
				self.takeItem(self.indexFromItem(item).row())
				if not data['items']:
					data['items'] = None
		self.list_updated.emit()

	def open_item(self, item):
		if self.key_ctrl:
			tex_file = builders.older_tex(item.data(32))
			if isinstance(tex_file, str):
				if os.path.splitext(tex_file)[-1]:
					command = r'it "%s"' % tex_file
					self.setProperty('ctrl', 'False')
					self.setStyleSheet('')
					self.key_ctrl = False
					os.popen(command)
		else:
			path = item.data(32)
			webbrowser.open(path)
