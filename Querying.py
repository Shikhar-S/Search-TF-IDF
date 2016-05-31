__author__ = 'Shikhar'
import MySQLdb
from collections import defaultdict
import math
import porter2
import os
class Querying:
    def __init__(self, path_to_folder=os.getcwd(), n=0, usID='shikhar', pswd='password', dbase='indexing_project', hst='localhost'):
        self.path=path_to_folder
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
        self.query = raw_input('Enter Query\n')

    def getWeight(self, word, doc_num):
        cursor = self.db.cursor()
        cursor.execute("SELECT IDF_VALUE FROM IDF WHERE WORD='%s'" % word)
        temp=cursor.fetchone()
       # print temp
        if cursor.rowcount>0:
            idf = temp[0]
        else:
            idf=0
        tf_retrieval = "SELECT TF_VALUE FROM DOC%d WHERE WORD='%s'" % (doc_num, word)
        cursor.execute(tf_retrieval)
        if cursor.rowcount>0:
            temp=cursor.fetchone()
            return temp[0] * idf
        else:
            return 0
    def getN(self):
        self.N=len([name for name in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, name))])

    def processQuery(self):
        self.getN()
        query=(self.query).lower().split(' ')
        cur=self.db.cursor()
        score={}
        score=defaultdict(lambda: 0, score)
        for word in query:
            word=porter2.stem(word)
            for i in xrange(1,self.N+1):
                w=self.getWeight(word,i)
                if w>0:
                    score[i]=score[i]+(w*(query.count(word)/float(len(query))))
        for doc in score:
            cur.execute(("SELECT TF_VALUE FROM DOC%d" % doc))
            length=0
            for item in cur:
                length += (item[0]*item[0])
            length=math.sqrt(length)
            score[doc]=score[doc]/length
        result=[]
        for doc,value in sorted(score.iteritems(),key= lambda (k,v): (v,k)):
            result.append((doc,value))
        for i in xrange(len(result)-1,-1,-1):
            print result[i]
