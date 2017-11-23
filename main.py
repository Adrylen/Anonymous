import begin
import sys


# dirname path host account passwd folder --frequency 15 --depth 6 --debug --maxsize 10000000
@begin.start
def main(dirname, path, host, account, passwd, folder, frequency=15, depth="6", debug=False, maxsize="10000000"):
	print(sys.version)
