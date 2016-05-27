import os
import MySQLdb
import re
import math
from porterStemmer import PorterStemmer
from collections import defaultdict

stemmer = PorterStemmer()


class Indexing:
    def __init__(self, stpwrdfile, usID='shikhar', pswd='password', dbase='indexing_project', hst='localhost'):
        self.userID = usID
        self.password = pswd
        self.database = dbase
        self.host = hst
        self.cwd = os.getcwd()
        self.stopWordFile = stpwrdfile
        try:
            self.db = MySQLdb.connect(self.host, self.userID, self.password, self.database)
        except:
            print 'entering initialising database'
        self.N = 0

    def __del__(self):
        self.db.close()

    def setUpDatabase(self):
        # n is the number of files to be indexed
        # set up TF and IDF databases
        maxlenWord = 20
        try:
            cursor = self.db.cursor()
            cursor.execute("DROP TABLE IF EXISTS TF")
            tf = 'CREATE TABLE TF(WORD CHAR(%d) NOT NULL,' % maxlenWord

            for i in xrange(1, self.N):
                tf  += 'DOC' + str(i) + ' FLOAT,'
            tf = tf + 'DOC' + str(self.N) + ' FLOAT)'
            cursor.execute(tf)
            cursor.execute("DROP TABLE IF EXISTS IDF")
            idf = 'CREATE TABLE IDF(WORD CHAR(%d) NOT NULL,' % maxlenWord
            idf += 'IDF_VALUE FLOAT)'
            cursor.execute(idf)
        except Exception,e:
            print e
            print 'Error creating database'

    def removeStopWords(self, wordlist):
        with open(self.stopWordFile) as F_Stop:
             stopWordList = F_Stop.read().split(' ')
        wordlist = [x for x in wordlist if x not in stopWordList]
        return wordlist

    def TF_insert(self, fid, word, count_total, word_freq):
        # calculates TF and inserts into table TF
        cursor = self.db.cursor()
        value = word_freq/float(count_total)
        try:
            cursor.execute("SELECT * FROM TF WHERE WORD='%s'" % word)
            present = cursor.rowcount > 0
            if not present:
                query_insert = 'INSERT INTO TF(WORD,'
                for i in xrange(1, self.N):
                    query_insert = query_insert + 'DOC' + str(i) + ','
                query_insert = query_insert + 'DOC' + str(self.N)
                query_insert = query_insert + ") VALUES('" +word+"',"
                for i in xrange(1, fid):
                    query_insert = query_insert + '0,'
                query_insert = query_insert + ('%f' % value)
                for i in xrange(fid + 1, self.N + 1):
                    query_insert = query_insert + ',0'
                query_insert = query_insert + ')'

                cursor.execute(query_insert)
            else:
                # learn to use update command
                query_update = 'UPDATE TF SET DOC' + fid + ('=%f ' % value) + ("WHERE WORD='%s'" % word)

                cursor.execute(query_update)
            self.db.commit()
        except Exception, e:
            print e
            self.db.rollback()
            #print 'Error entering value to data base for %s' % word

    def IDF_insert(self):
        cursor = self.db.cursor()
        insertion_cursor = db.cursor()
        cursor.execute('SELECT * FROM TF')
        for row in cursor:
            c = self.N
            for ele in row:
                if ele == 0:
                    c -= 1
            insert_q = "INSERT INTO IDF VALUES('%s'," % row[0]
            value = math.log(self.N / c)
            insert_q += ('%f )' % value)
            insertion_cursor.execute(insert_q)

    def addToDatabase(self, F, listOfWords, fid):
        hashtable_words = {}
        hashtable_words = defaultdict(lambda: 0, hashtable_words)
        for word in listOfWords:
            hashtable_words[word] = hashtable_words[word] + 1
        cnt = len(listOfWords)
        for word in hashtable_words:
            self.TF_insert(fid, word, cnt, hashtable_words[word])

    def fetchStemmedWords(self, path):
        with open(path, 'r') as F:
            text = F.read()
            text = text.lower()
            text = re.sub(r'[^a-z0-9 ]', ' ', text)
            listOfWords = text.split(' ')
            listOfWords = self.removeStopWords(listOfWords)
            listOfWords = [stemmer.stem(word, 0, len(word) - 1) for word in listOfWords]
        return listOfWords

    def parseFile(self, path_to_file, fid):
        listOfWords = self.fetchStemmedWords(path_to_file)
        with open(path_to_file, 'r') as F:
            self.addToDatabase(F, listOfWords, fid)

    def createIndex(self, pathtofolder):
        filesinside = []
        for f in os.listdir(pathtofolder):
            if os.path.isfile(os.path.join(pathtofolder, f)):
                f=os.path.join(pathtofolder,f)
                #print f
                filesinside.append(f)
        self.N = len(filesinside)
        self.setUpDatabase()
        for i in xrange(1, self.N + 1):
            self.parseFile(filesinside[i - 1], i)
        self.IDF_insert()

#######################################
