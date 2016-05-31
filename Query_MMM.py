__author__='Shikhar'
from Querying import Querying
import porter2
from collections import defaultdict
class Query_MMM(Querying):
    def __init__(self,pathtofolder,cor1=0.25,cand1=0.6):
        Querying.__init__(self, pathtofolder)
        self.C_or1=cor1
        self.C_or2=1-self.C_or1
        self.C_and1=cand1
        self.C_and2=1-self.C_and1
        self.maxIDF=0;

    def getMaxIDF(self):
        cursor=self.db.cursor()
        cursor.execute("SELECT MAX(IDF_VALUE) FROM IDF")
        temp_row=cursor.fetchone()
        self.maxIDF=temp_row[0]

    def getSimilarityAND(self, query, doc_num):
        cursor=self.db.cursor()
        min_w = 1
        max_w = 0
        for word in query:
            cursor.execute(("SELECT TF_VALUE FROM DOC%d WHERE WORD='%s'" %(doc_num, word)))
            for row in cursor:
                min_w=min(min_w,row[0])
                max_w=max(max_w,row[0])
        if min_w==1 and max_w==0:
            return  0
        cursor.execute(("SELECT IDF_VALUE FROM IDF WHERE WORD='%s'" % word))
        temp_row = cursor.fetchone()
        idf_value = temp_row[0]
        min_w = idf_value * min_w / self.maxIDF
        max_w = max_w * idf_value / self.maxIDF
        return self.C_and1*min_w+self.C_and2*max_w

    def getSimilarityOR(self, query, doc_num):
        cursor = self.db.cursor()
        min_w = 1
        max_w = 0
        for word in query:
            cursor.execute(("SELECT TF_VALUE FROM DOC%d WHERE WORD='%s'" % (doc_num, word)))
            for row in cursor:
                min_w = min(min_w, row[0])
                max_w = max(max_w, row[0])
        if min_w == 1 and max_w == 0:
            return 0
        cursor.execute(("SELECT IDF_VALUE FROM IDF WHERE WORD='%s'" % word))
        temp_row=cursor.fetchone()
        idf_value=temp_row[0]
        min_w=idf_value*min_w/self.maxIDF
        max_w=max_w*idf_value/self.maxIDF
        return self.C_or1 * max_w + self.C_or2 * min_w


    def processQuery(self):
        self.getN()
        self.getMaxIDF()
        query=[porter2.stem(word) for word in self.query.lower().split(' ')]
        score = {}
        score = defaultdict(lambda: 0, score)
        for i in xrange(1,self.N+1):
            t = self.getSimilarityOR(query, i)
            if t != 0:
                score[i] = t
        print "\n OR SEARCH \n"
        self.display(score)
        print "\n AND SEARCH\n"
        for i in xrange(1, self.N + 1):
            t = self.getSimilarityAND(query, i)
            if t != 0:
                score[i] = t
        self.display(score)

    def display(self,score):
        result = []
        for doc, value in sorted(score.iteritems(), key=lambda (k, v): (v, k)):
            result.append((doc, value))
        for i in xrange(len(result) - 1, -1, -1):
            print result[i]

