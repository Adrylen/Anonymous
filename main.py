from ftplib import FTP
from time import sleep

import begin
import sys

from utils.Snapshot import Snapshot


@begin.start
def main(dirname, path, host, account, passwd, folder, frequency=15, depth=6, debug=False, maxsize="10000000"):
	print(sys.version)
	snapshot = Snapshot(dirname)
	snapshot.scan(int(depth))

	while True:
		s2 = Snapshot(dirname)
		s2.scan(int(depth))

		# print(len(snapshot.diff(s2)))
		for diff in snapshot.diff(s2):
			print(str(diff))

		snapshot = s2
		sleep(int(frequency))
