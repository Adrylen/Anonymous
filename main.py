from ftplib import FTP
from time import sleep
import logging
import logging.config

import begin
import sys
import os

from utils.Snapshot import Snapshot


@begin.start
def main(dirname, path, host, account, passwd, folder, frequency=15, depth=6, debug=False, maxsize="10000000"):
	print(sys.version)
	logging.config.fileConfig(os.path.join(os.getcwd(), "log.conf"))
	main_logger = logging.getLogger("root")

	snapshot = Snapshot(dirname)
	snapshot.scan(int(depth))

	while True:
		s2 = Snapshot(dirname)
		s2.scan(int(depth))

		# print(len(snapshot.diff(s2))
		for diff in snapshot.diff(s2):
			main_logger.info(str(diff))

		snapshot = s2
		sleep(int(frequency))
