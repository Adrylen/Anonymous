import datetime
import os


class File:
	def __init__(self, path):
		self.isDir = os.path.isdir(path)

		split = path.split(os.path.sep)
		if self.isDir and split[-1] == "":
			self.name = split[-2]
		else:
			self.name = split[-1]
		self.path = path
		self.size = os.stat(self.path).st_size
		self.date_f = os.path.getmtime(self.path)
		self.date = datetime.datetime.fromtimestamp(self.date_f)

	def __str__(self):
		return ("Path=" + self.path + ", Name=" + self.name + ", size=" + str(self.size) + ", date=" + self.date.strftime(
			"%Y-%m-%d %H:%M:%S"))

	def __eq__(self, other):
		return self.isDir == other.isDir and self.path == other.path and self.size == other.size and self.date == other.date

	def __ne__(self, other):
		return not self.__eq__(other)

	def __hash__(self):
		return hash(self.path + str(self.date_f) + str(self.size) + self.name + str(self.isDir))
