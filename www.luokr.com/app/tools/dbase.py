#coding=utf-8

import sys
reload(sys)

import os, glob

sys.setdefaultencoding('utf-8')
sys.path[0] = os.path.dirname(os.path.dirname(sys.path[0]))

from app.etc import etc
import sqlite3

def main():
    for sql in glob.glob(os.path.join(etc['database_path'], '*.sql')):
        dat = sql[:-3] + 'dat'
        if os.path.exists(dat):
            print("Find dbase: %s" % dat)
        else:
            print("Make dbase: %s" % dat)

            con = sqlite3.connect(dat)
            con.executescript(open(sql).read())
            con.close()

if __name__ == "__main__":
    main()

