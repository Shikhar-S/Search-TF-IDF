__author__ = 'Shikhar'
import MySQLdb



class Querying:
    def __init__(self, usID='shikhar', pswd='password', dbase='indexing_project', hst='localhost', n=0):
        self.query = ''
        self.userID = usID
        self.password = pswd
        self.database = dbase
        self.host = hst
        self.N = n
        try:
            self.db = MySQLdb.connect(self.host, self.userID, self.password, self.database)
        except:
            print 'error initialising database'

    def __del__(self):
        self.db.close()

    def getQuery(self):
        self.query = raw_input('Enter Query')

    def getWeight(self, word, doc_num):
        cursor = self.db.cursor()
        cursor.execute("SELECT IDF_VALUE FROM IDF WHERE WORD='%s'" % word)
        idf = cursor[0][0]
        tf_retrieval = "SELECT TF_VALUE FROM DOC%d WHERE WORD='%s'" % (doc_num, word)
        cursor.execute(tf_retrieval)
        return cursor[0][0] * idf
