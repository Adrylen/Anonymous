from ftplib import FTP


ftp = FTP('localhost')
ftp.login('bob', '1234')
print(ftp.cwd('Bonjour'))
print(ftp.dir())
print(ftp.retrbinary('RETR Bonjour.txt', open('Bonjour.txt', 'wb').write))
ftp.quit()

