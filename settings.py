import json, os

path_settings = 'settingsTEXconverter.json'
console_message = 'Use it as command line. Write keys only. It overrides all settings.'
directory_label = 'All items will be saved next to itself'


class Settings(object):
	def __init__(self):

		self.default_data = dict(
			arguments=['up-', 'black', 'diagonal', 'tiff', 'byte'],
			newer=False,
			txmake=None,
			directory=None,
			console=None,
			items=None
		)
		self.path = os.path.join(os.path.expanduser('~'), path_settings)
		if not os.path.exists(self.path):
			self.default_settings(self.path)

	def default_settings(self, path):
		with open(path, 'w') as file:
			json.dump(self.default_data, file, indent=4)

	def load(self):
		return json.load(open(self.path))

	def save(self, data):
		if data['console'] == console_message:
			data['console'] = None
		with open(self.path, 'w') as file:
			json.dump(data, file, indent=4)


class SettingsManager(object):
	def __enter__(self):
		self.data = Settings().load()
		return self.data

	def __exit__(self, exc_type, exc_val, exc_tb):
		Settings().save(self.data)
