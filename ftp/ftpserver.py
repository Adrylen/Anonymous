from ftplib import FTP
import ftplib
import traceback


def getPath(path):
	return "/".join(path.split("/")[:-1])

def cdTree(ftp, currentDir):
	if currentDir != "":
		try:
			ftp.cwd(currentDir)
		except ftplib.error_perm as e:
			#print("Probleme: " + str(e))
			cdTree(ftp, "/".join(currentDir.split("/")[:-1]))
			ftp.mkd(currentDir)
			ftp.cwd(currentDir)

def removeDirectory(ftp,path):
	try:
		dirs=[]
		files=[]
		ftp.retrlines("NLST",files.append)
		ftp.dir(dirs.append)
		for file in files:
			ftp.delete(file)
		for dir in dirs:
			removeDirectory(ftp, path+"/"+dir)
		ftp.rmd(path)
	except ftplib.error_perm as e:
		print(str(traceback.format_exc()))

def test():
	ftp = FTP('localhost')
	ftp.login('bob', '1234')
	#print(ftp.cwd('Bonjour'))
	print(ftp.dir())
	#print(ftp.retrbinary('RETR test/Bonjour.txt', open('Bonjour.txt', 'wb').write))
	file = open('Bonjour.txt','rb')
	cdTree(ftp, "/test/test1/test2")
	ftp.storbinary('STOR /test/test1/test2/Bonjour.txt', file)     # send the file
	ftp.quit()


if __name__ == "__main__":
	test()