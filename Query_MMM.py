__author__='Shikhar'
from Querying import Querying
import porter2
from collections import defaultdict
import math
from Index_individual import Indexing
class Query_MMM(Querying):
    '''
    Implements Maxed min and max formula for ranking documents based on search query
    '''
    def __init__(self,pathtofolder,query,stemming_algo='porter',cor1=0.6,cand1=0.6):
        '''
        :param pathtofolder:Folder containing Files to be indexed (to be passed to base class)
        :param cor1: OR coefficient for MMM formula
        :param cand1: AMD cefficient for MMM formula
        '''
        Querying.__init__(self, query,pathtofolder,stemming_algo)
        self.C_or1=cor1
        self.C_or2=1-self.C_or1
        self.C_and1=cand1
        self.C_and2=1-self.C_and1
        self.maxIDF=0

    def getMaxIDF(self):
        '''
        :return: gives maximum IDF value which is the denominator in MMM formula
        '''
        cursor=self.db.cursor()
        cursor.execute("SELECT MAX(IDF_VALUE) FROM IDF")
        temp_row=cursor.fetchone()
        self.maxIDF=temp_row[0]

    def get_min_max_values(self,query,doc_num):
        '''
        :param query: query given by user
        :param doc_num: doc id in which max and min value of weight has to be found
        :return: gives a tuple containing max and min weights out of all given query words in given doc
        '''
        cursor = self.db.cursor()
        cursor.execute("SELECT LENGTH FROM FILES WHERE FILE_ID=%d" % doc_num)
        row=cursor.fetchone()
        len_doc=row[0]
        min_w = math.log(self.N)*len_doc #largest value of weight=freq
        max_w = 0
        idf_value=1
        for word in query:
            cursor.execute(("SELECT TF_VALUE FROM DOC%d WHERE WORD='%s'" % (doc_num, word)))
            if cursor.rowcount>0:
                row=cursor.fetchone()
                t_freq =  row[0]*len_doc
                cursor.execute(("SELECT IDF_VALUE FROM IDF WHERE WORD='%s'" % word))
                temp_row = cursor.fetchone()
                idf_value = temp_row[0]
                min_w = min(idf_value * t_freq / self.maxIDF,min_w)
                max_w = max(t_freq * idf_value / self.maxIDF,max_w)
            else:
                min_w=0
        return (min_w,max_w)


    def getSimilarityAND(self, query, doc_num):
        '''
        :param query: query given by user
        :param doc_num: doc id for which MMM has to be calculated
        :return: calculates MMM value for AND type search
        '''
        ans=self.get_min_max_values(query,doc_num)
        min_w=ans[0]
        max_w=ans[1]
        return self.C_and1*min_w+self.C_and2*max_w

    def getSimilarityOR(self, query, doc_num):
        '''
        :param query: query given by user
        :param doc_num: doc id for which MMM has to be calculated
        :return: calculates MMM value for OR type search
        '''
        ans = self.get_min_max_values(query, doc_num)
        min_w = ans[0]
        max_w = ans[1]
        return self.C_or1 * max_w + self.C_or2 * min_w

    def processQuery_OR(self,query):
        '''
        :return: to process the input query based on MMM
        '''
        score = {}
        score = defaultdict(lambda: 0, score)
        for i in xrange(1,self.N+1):
            t = self.getSimilarityOR(query, i)
            if t != 0:
                score[i] = t
        result_OR=[]
        for doc, value in sorted(score.iteritems(), key=lambda (k, v): (-v, k)):
            result_OR.append((doc, value))
        return self.generate_result(result_OR)
        #print "\n OR SEARCH \n"
        #self.display(score)
        #print "\n AND SEARCH\n"

    def processQuery_AND(self,query):
        score = {}
        score = defaultdict(lambda: 0, score)
        for i in xrange(1, self.N + 1):
            t = self.getSimilarityAND(query, i)
            if t != 0:
                score[i] = t
        result_AND = []
        for doc, value in sorted(score.iteritems(), key=lambda (k, v): (-v, k)):
            result_AND.append((doc, value))
        return self.generate_result(result_AND)

    def processQuery(self,type='OR'):
        self.getN()
        self.getMaxIDF()
        query = [self.stem(word) for word in self.query.lower().split(' ')]
        if type=='OR':
            return self.processQuery_OR(query)
        else:
            return self.processQuery_AND(query)

    def display(self,score):
        '''
        :param score: array representing relevance of each doc to the query
        :return: displays final result by sorting score array
        '''
        result = []
        for doc, value in sorted(score.iteritems(), key=lambda (k, v): (v, k)):
            result.append((doc, value))
        for i in xrange(len(result) - 1, -1, -1):
            print result[i]
