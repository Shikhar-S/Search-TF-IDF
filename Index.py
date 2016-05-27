import os
import MySQLdb
import re
from porterStemmer import PorterStemmer
from collections import defaultdict
stemmer=PorterStemmer()
class Indexing:
    def __init__(self, usID, pswd, dbase, hst,stpwrdfile):
        self.userID = usID
        self.password = pswd
        self.database = dbase
        self.host = hst
        self.cwd = os.getcwd()
        self.stopWordFile = stpwrdfile


    def setUpDatabase(self,n):
        #n is the number of files to be indexed
        #set up TF and IDF databases
        maxlenWord=20
        try:
            db = MySQLdb.connect(self.host, self.userID, self.password, self.database)
            cursor = db.cursor()
            tf = 'CREATE TABLE TF(WORD CHAR(%d),' % maxlenWord
            for i in xrange(1, n + 1):
                tf = tf + 'DOC' + i + ' FLOAT,'
            tf = tf + ')'
            cursor.execute(tf)
            idf='CREATE TABLE IDF(WORD CHAR(%d),' % maxlenWord
            for i in xrange(1, n + 1):
                tf = tf + 'DOC' + i + ' FLOAT,'
            idf = idf + ')'
            cursor.execute(idf)
            db.close()
        except:
            print 'Error creating database'


    def removeStopWords(self,wordlist):
        stopWordList=self.stopWordFile.read().split(' ')
        wordlist=[x for x in wordlist if x not in stopWordList]
        return wordlist


    def TF_insert(self,word,count):
        #calculates TF and inserts into table TF
        db = MySQLdb.connect(self.host, self.userID, self.password, self.database)
        cursor=db.cursor()




    def IDF(self,word):
        pass
        #returns IDF after TF has been calculated

    def addToDatabase(self,F,listOfWords,fid):
        #To-Do
        #set up connection to database

        #for each word call tf fn and insert into database
        hashtable_words = {}
        hashtable_words = defaultdict(lambda: 0, hashtable_words)
        for word in listOfWords:
            hashtable_words[word]=hashtable_words[word]+1
        cnt=len(listOfWords)
        for word in hashtable_words:
            self.TF_insert(word, cnt)


        #if not already present create a new row

    def parseFile(self,dataset_file,fid):
        path_tofile=self.cwd+dataset_file
        with open(path_tofile,'r') as F:
            text = F.read()
            text = text.lower()
            text = re.sub(r'[^a-z0-9 ]',' ',text)
            listOfWords = text.split(' ')
            listOfWords=self.removeStopWords(listOfWords)
            listOfWords = [stemmer.stem(word,0,len(word)-1) for word in listOfWords]
            self.addToDatabase(F,listOfWords,fid)

    def createIndex(self):pass






#######################################





