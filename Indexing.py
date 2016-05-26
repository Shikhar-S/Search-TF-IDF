__author__ = 'Shikhar'
import MySQLdb
class Indexing:
    def __init__(self,usID,pswd,dbase,hst):
        self.userID=usID
        self.password=pswd
        self.database=dbase
        self.host=hst

    def setUpDatabase(self,N):
        db=MySQLdb.connect(self.host,self.userID,self.password,self.database)
        cursor=db.cursor()
        tf='CREATE TABLE TF(WORD CHAR(20) NOT NULL,'
        for i in xrange(1,N):
            tf=tf+'DOC'+i+' FLOAT,'
        tf=tf+'DOC'+N+' FLOAT)'
        cursor.execute(tf)
        idf='CREATE TABLE IDF(WORD CHAR(20) NOT NULL,'
        for i in xrange(1,N):
            idf=idf+'DOC'+i+' FLOAT,'
        idf=idf+'DOC'+N+' FLOAT)'
        cursor.execute(idf)
        db.close()

    