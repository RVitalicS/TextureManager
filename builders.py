from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from subprocess import Popen, PIPE
import os, re
import settings, error


supported_types = [
	'.tif', '.exr', '.jpeg', '.jpg',
	'.sgi', '.tga', '.iff',
	'.dpx', '.bmp', '.hdr',
	'.png', '.gif', '.ppm', '.xpm']
uppercase = [x.upper() for x in supported_types]
for item in uppercase:
	supported_types.append(item)


def arguments_string():
	data = settings.Settings().load()['arguments']

	arguments = ' '.join([
		'-resize', data[0],
		'-mode', data[1],
		'-pattern', data[2],
		'-format', data[3],
		'-%s' % data[4]
	])

	if settings.Settings().load()['newer']:
		arguments += ' -newer'

	return arguments


def items_paths(selection=None):
	paths = []
	data = settings.Settings().load()['items']
	if selection:
		data = selection
	if data:
		for path in data:
			if os.path.splitext(path)[-1] in supported_types:
				paths.append(path)
			if not os.path.splitext(path)[-1]:
				folder_items = os.listdir(path)
				for item in folder_items:
					item = os.path.join(path, item)
					if os.path.splitext(item)[-1] in supported_types:
						paths.append(item)
	return paths


def convert(bar_object, lable_object, selection=None):

	data = settings.Settings().load()
	directory = data['directory']
	console = data['console']
	txmake = data['txmake']

	if console:
		arguments = console
	else:
		arguments = arguments_string()

	if items_paths(selection):
		bar_plus_value = 100/len(items_paths(selection))

		for enum, path_in in enumerate(items_paths(selection)):
			lable_object.setText(os.path.basename(path_in))
			bar_object.setValue(bar_object.value() + bar_plus_value)

			if directory:
				file = os.path.splitext(path_in)[0]+'.tex'
				file = os.path.basename(file)
				path_out = os.path.join(directory, file)
			else:
				path_out = os.path.splitext(path_in)[0]+'.tex'

			command = ' '.join([
				'"%s"' % txmake,
				arguments,
				'"%s"' % os.path.normpath(path_in),
				'"%s"' % os.path.normpath(path_out)])

			process = Popen(
				command,
				shell=True,
				stdout=PIPE, stderr=PIPE)

			process.wait()
			result = process.communicate()
			if process.returncode:
				bar_object.setValue(0)

				string = result[1].decode()
				message_error = error.Error()
				message_error.label_complete.setText(string)
				message_error.exec_()
				return

		bar_object.setValue(0)
		return True
	return False


def correct_name(name):
	if name:
		name = re.sub(r'[^a-z0-9\[\]\\/ -.]', "", name)

		while name[0] == ' ':
			name = name[1:]
			if not name:
				break
		if name:
			while name[-1] == ' ':
				name = name[:-1]

		return name


def correct_extensions(path):
	if not os.path.splitext(path)[-1]:
		return path
	if os.path.splitext(path)[-1] in supported_types:
		return path


def get_size(path_in, list_in):
	size_one = os.path.getsize(path_in)
	for (paths, dirs, files) in os.walk(path_in):
		for i in files:
			file = os.path.join(paths, i)
			size_one += os.path.getsize(file)

	size_all = 0
	for path in list_in:
		if os.path.splitext(path)[-1]:
			size_all += os.path.getsize(path)
		for (paths, dirs, files) in os.walk(path):
			for i in files:
				file = os.path.join(paths, i)
				size_all += os.path.getsize(file)

	if size_all == 0:
		size_all = size_one

	return "%0.2f / %0.2f MB" % ((size_one / (1024 * 1024.0)), (size_all / (1024 * 1024.0)))


def get_size_tex(path_in):
	directory = settings.Settings().load()['directory']
	size_tex = 0

	if os.path.splitext(path_in)[-1]:

		if directory:
			file = os.path.splitext(path_in)[0] + '.tex'
			file = os.path.basename(file)
			file_tex = os.path.join(directory, file)
		else:
			file_tex = os.path.splitext(path_in)[0] + '.tex'

		if os.path.exists(file_tex):
			size_tex += os.path.getsize(file_tex)

	else:
		list_img = os.listdir(path_in)

		if directory:
			list_img = [os.path.splitext(file)[0] + '.tex' for file in list_img]
			list_path = [os.path.join(directory, file) for file in list_img]
		else:
			list_path = [os.path.join(path_in, file) for file in list_img]

		tex_only = []
		for file in list_path:
			if os.path.splitext(file)[-1] == '.tex':
				tex_only.append(file)

		for file_tex in tex_only:
			if os.path.exists(file_tex):
				size_tex += os.path.getsize(file_tex)

	return "%0.2f" % (size_tex / (1024 * 1024.0))


def older_tex(path_in):
	directory = settings.Settings().load()['directory']

	if not os.path.splitext(path_in)[-1]:
		list_file = os.listdir(path_in)
		list_path = [os.path.join(path_in, file) for file in list_file]
		if directory:
			list_tex = [os.path.splitext(os.path.join(directory, file))[0] + '.tex' for file in list_file]
		else:
			list_tex = [os.path.splitext(os.path.join(path_in, file))[0] + '.tex' for file in list_file]
		img_tex = zip(list_path, list_tex)
		for img, tex in list(img_tex):
			if os.path.exists(tex):
				if not os.path.getmtime(img) <= os.path.getmtime(tex):
					return False
			else:
				return False
		if list_file:
			return True

	if directory:
		file = os.path.splitext(path_in)[0] + '.tex'
		file = os.path.basename(file)
		path_tex = os.path.join(directory, file)
	else:
		path_tex = os.path.splitext(path_in)[0] + '.tex'

	if os.path.exists(path_tex):
		if os.path.getmtime(path_in) <= os.path.getmtime(path_tex):
			return path_tex


def build_item(self_object, path):
	item = QListWidgetItem(self_object)
	item.setText(os.path.basename(path))

	if not os.path.splitext(path)[-1]:
		list_file = os.listdir(path)
		list_path = []
		for file in list_file:
			if os.path.splitext(file)[-1] in supported_types:
				list_path.append(os.path.normpath(file))

		item.setToolTip('\n'.join(list_path))

	item.setData(Qt.UserRole, path)
	item.setSelected(1)
	item.setSelected(0)
