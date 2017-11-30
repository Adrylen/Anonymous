import os
import sys
import logging
import logging.config

from utils.File import File


class Snapshot:
	def __init__(self, path):
		self.data = []
		self.path = path
		logging.config.fileConfig(os.path.join(os.getcwd(), "log.conf"))
		self.main_logger = logging.getLogger("root")

	def scan(self, level):
		if level != 0:
			for root, dirs, files in os.walk(self.path):
				path = root.replace(self.path, "").split(os.path.sep)
				if path[-1] == "":
					path = []
				if len(path) <= level:
					self.data.append(File(root))
				if len(path) < level:
					for file in files:
						self.data.append(File(root + os.path.sep + file))
		else:
			self.data.append(File(self.path))
		return self

	def diff(self, other):
		return set(self.data).symmetric_difference(set(other.data))

	def print(self):
		for d in self.data:
			self.main_logger.info(str(d))

	def __eq__(self, other):
		if len(self.data) != len(other.data):
			return False
		for e1, e2 in self.data, other.data:
			if e1 != e2:
				return False
		return True

	def __ne__(self, other):
		return not self.__eq__(other)


if __name__ == "__main__":
	print(sys.version)
