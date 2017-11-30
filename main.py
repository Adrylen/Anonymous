from ftplib import FTP
from time import sleep
import logging
import logging.config

import begin
import sys
import os

from ftp.ftpserver import cdTree, getPath,removeDirectory
from utils.Snapshot import Snapshot


@begin.start
def main(dirname, path, host, account, passwd, folder, frequency=5, depth=6, debug=False, maxsize="10000000"):
	print(sys.version)
	logging.config.fileConfig(os.path.join(os.getcwd(), "log.conf"))
	main_logger = logging.getLogger("root")

	snapshot = Snapshot(dirname)
	snapshot.scan(int(depth))

	ftp = FTP(host)
	ftp.login(account, passwd)

	for file in snapshot.data:
		if not file.isDir:
			pathforftp = file.path.replace(os.path.sep, '/')
			cdTree(ftp, "/" + folder + "/" + getPath(pathforftp))
			ftp_command = "STOR " + "/" + folder + "/" + pathforftp
			ftp.storbinary(ftp_command, open(file.path, "rb"))

	while True:
		s2 = Snapshot(dirname)
		s2.scan(int(depth))

		for diff in snapshot.diff(s2):
			pathforftp = diff[1].path.replace(os.path.sep, '/')
			if not diff[1].isDir:
				if diff[0] == "update" or diff[0] == "add":
					cdTree(ftp, "/" + folder + "/" + getPath(pathforftp))
					ftp_command = "STOR " + "/" + folder + "/" + pathforftp
					ftp.storbinary(ftp_command, open(diff[1].path, "rb"))
				else:
					ftp.delete("/" + folder + "/" + pathforftp)
			else:
				if diff[0] == "remove":
					print("/" + folder + "/" + pathforftp)
					removeDirectory(ftp,"/" + folder + "/" + pathforftp)
			if debug:
				main_logger.info(str(diff))

			journal = open(path, "a")
			journal.write(str(diff)+"\n")
			journal.close()

		snapshot = s2
		sleep(int(frequency))
