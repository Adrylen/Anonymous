import os
import sys

from utils.File import File


class Snapshot:
	def __init__(self, path):
		self.data = []
		self.path = path

	def scan(self, level):
		if level != 0:
			for root, dirs, files in os.walk(self.path):
				path = root.replace(self.path, "").split(os.path.sep)
				if path[-1] == "":
					path = []
				if len(path)-1 <= level:
					self.data.append(File(root))
				if len(path) < level:
					for file in files:
						self.data.append(File(root + os.path.sep + file))
		else:
			self.data.append(File(self.path))
		return self

	def diff(self, other):
		result = []
		updates = []
		diffs = set(self.data).symmetric_difference(set(other.data))
		for el in diffs:
			update = [file for file in diffs if file.path == el.path and file not in updates]
			if len(update) > 1:
				tmp = ["update"]
				for f in update:
					updates.append(f)
					tmp.append(f)
				result.append(tmp)
			elif el in self.data and el not in updates:
				result.append(["remove", el])
			elif el in other.data and el not in updates:
				result.append(["add", el])
		return result

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
