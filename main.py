from ftplib import FTP
from time import sleep
import logging
import logging.config

import begin
import sys
import os

from ftp.ftpserver import cdTree, getPath
from utils.Snapshot import Snapshot


@begin.start
def main(dirname, path, host, account, passwd, folder, frequency=15, depth=6, debug=False, maxsize="10000000"):
	print(sys.version)
	logging.config.fileConfig(os.path.join(os.getcwd(), "log.conf"))
	main_logger = logging.getLogger("root")

	snapshot = Snapshot(dirname)
	snapshot.scan(int(depth))

	ftp = FTP(host)
	ftp.login(account, passwd)

	for file in snapshot.data:
		if not file.isDir:
			cdTree(ftp, "/" + folder + "/" + getPath(file.path))
			ftp_command = "STOR " + "/" + folder + "/" + file.path
			ftp.storbinary(ftp_command, open(file.path, "rb"))

	while True:
		s2 = Snapshot(dirname)
		s2.scan(int(depth))

		for diff in snapshot.diff(s2):
			if not diff[1].isDir:
				if diff[0] == "update" or diff[0] == "add":
					cdTree(ftp, "/" + folder + "/" + getPath(diff[1].path))
					ftp_command = "STOR " + "/" + folder + "/" + diff[1].path
					ftp.storbinary(ftp_command, open(diff[1].path, "rb"))
				else:
					# TODO REMOVE
					pass
			if debug:
				main_logger.info(str(diff))

			journal = open(path, "a")
			journal.write(str(diff))
			journal.close()

		snapshot = s2
		sleep(int(frequency))
