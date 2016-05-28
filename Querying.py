__author__ = 'Shikhar'
import MySQLdb
import math
class Querying:
    def __init__(self,usID='shikhar', pswd='password', dbase='indexing_project', hst='localhost'):
        self.query=''
        self.userID = usID
        self.password = pswd
        self.database = dbase
        self.host = hst
        try:
            self.db = MySQLdb.connect(self.host, self.userID, self.password, self.database)
        except:
            print 'error initialising database'

    def __del__(self):
        self.db.close()

    def getQuery(self):
        self.query=raw_input('Enter Query')

    def getScore(self):

