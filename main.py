import begin
import sys

from utils.Snapshot import Snapshot


@begin.start
def main(dirname, path, host, account, passwd, folder, frequency=15, depth="6", debug=False, maxsize="10000000"):
	print(sys.version)
	snapshot = Snapshot(dirname)
#	snapshot.scan(depth).print()
