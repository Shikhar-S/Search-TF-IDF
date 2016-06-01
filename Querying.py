__author__ = 'Shikhar'
import MySQLdb
from collections import defaultdict
import math
import porter2
import os
class Querying:
    '''
    to Query based on Cosine Similarity statistic
    '''
    def __init__(self, path_to_folder=os.getcwd(), n=0, usID='shikhar', pswd='password', dbase='indexing_project', hst='localhost'):
        '''
        :param path_to_folder: folder containing indexed docs
        :param n: number of indexed docs
        :param usID: User ID for database connection
        :param pswd: password for database connection
        :param dbase: Name of the datbase
        :param hst: database hosted at @host
        '''
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
        '''
        :return: inputs the query from user
        '''
        self.query = raw_input('Enter Query\n')

    def getWeight(self, word, doc_num):
        '''
        :param word:query word for which weight is to be calculatd
        :param doc_num: doc in which weight is to be calculated
        :return: returns the weight of given word in doc
        '''
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
        '''
        :return: to initialise N-> number of documents in folder
        '''
        self.N=len([name for name in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, name))])

    def processQuery(self):
        '''
        :return: inputs the query and then processes each word to determine similarity coefficient for each doc using getWeight then displays the final result
        '''
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