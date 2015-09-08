#coding=utf-8

import os.path, sys
reload(sys)
sys.setdefaultencoding('utf-8')

sys.path[0] = os.path.dirname(os.path.dirname(sys.path[0]))

from app.etc import etc
import sqlite3

def main():
    for name, path in etc['sqlite_dbases'].items():
        if not os.path.exists(path):
            print("Make dbase: %s => %s" % (name, path))

            dbn = sqlite3.connect(path)
            dbn.executescript(open(os.path.join(os.path.dirname(path), name + '.sql')).read())
            dbn.close()
        else:
            print("Find dbase: %s => %s" % (name, path))

if __name__ == "__main__":
    main()

