from ftplib import FTP
from time import sleep

import begin
import sys
import os
from ftp.ftpserver import cdTree

from utils.Snapshot import Snapshot


@begin.start
def main(dirname, path, host, account, passwd, folder, frequency=15, depth=6, debug=False, maxsize="10000000"):
	print(sys.version)
	snapshot = Snapshot(dirname)
	snapshot.scan(int(depth))

	ftp = FTP(host)
	ftp.login(account,passwd)

	for file in snapshot.data:
		cdTree(ftp, folder + "/" + file.path)
		ftp_command = "STOR " + folder + "/" + file.path
		ftp.storbinary(ftp_command, open(file.path))

	while True:
		s2 = Snapshot(dirname)
		s2.scan(int(depth))

		# print(len(snapshot.diff(s2)))
		for diff in snapshot.diff(s2):
			cdTree(ftp, folder + "/" + diff.path)
			ftp_command = "STOR " + folder + "/" + diff.path
			ftp.storbinary(ftp_command, open(diff.path))
			print(str(diff))

		snapshot = s2
		sleep(int(frequency))
