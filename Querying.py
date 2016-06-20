__author__ = 'Shikhar'
import MySQLdb
from collections import defaultdict
import math
import porter2
import lovins
import paicehusk
import os
class Querying:
    '''
    to Query based on Cosine Similarity statistic
    '''
    def __init__(self, query='',path_to_folder=os.getcwd(),stemming_algo='porter', n=0, usID='shikhar', pswd='password', dbase='indexing_project', hst='localhost'):
        '''
        :param path_to_folder: folder containing indexed docs
        :param n: number of indexed docs
        :param usID: User ID for database connection
        :param pswd: password for database connection
        :param dbase: Name of the datbase
        :param hst: database hosted at @host
        '''
        self.stemming_algo=stemming_algo
        self.path=path_to_folder
        self.query = query
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
        cursor.execute(("SELECT IDF_VALUE FROM IDF WHERE WORD='%s'" % word))
        temp=cursor.fetchone()
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
        cursor=self.db.cursor()
        cursor.execute('SELECT MAX(FILE_ID) FROM FILES')
       # self.N=len([name for name in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, name))])
        self.N=cursor.fetchone()[0]

    def generate_result(self,ranks):
        result=[]
        cursor = self.db.cursor()
        for cur_rank in ranks:
            query='SELECT * FROM FILES WHERE FILE_ID=%d' % cur_rank[0]
            #print cur_rank
            cursor.execute(query)
            row=cursor.fetchone()
            result.append(row[1])
        return result

    def stem(self, word):
        try:
            if self.stemming_algo == 'porter':
                return porter2.stem(word)
            elif self.stemming_algo == 'lovins':
                return lovins.stem(word)
            else:
                return paicehusk.stem(word)
        except Exception, e:
            pass

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
            word=self.stem(word)
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
        result.reverse()
        return self.generate_result(result)
