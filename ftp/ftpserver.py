from ftplib import FTP


def test():
	ftp = FTP('localhost')
	ftp.login('bob', '1234')
	print(ftp.cwd('Bonjour'))
	print(ftp.dir())
	print(ftp.retrbinary('RETR Bonjour.txt', open('Bonjour.txt', 'wb').write))
	ftp.quit()


if __name__ == "__main__":
	test()