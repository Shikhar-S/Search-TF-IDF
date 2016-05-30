__author__ = 'Shikhar'
import os
import MySQLdb
import re
import math
import warnings
from porterStemmer import PorterStemmer
from collections import defaultdict

stemmer = PorterStemmer()
warnings.filterwarnings('ignore', 'Unknown table')


class Indexing:
    def __init__(self, stpwrdfile, usID='shikhar', pswd='password', dbase='indexing_project', hst='localhost'):
        self.userID = usID
        self.password = pswd
        self.database = dbase
        self.host = hst
        self.stopWordFile = stpwrdfile
        self.N = 0
        self.stopWordSet = set()
        self.query_insert = ''
        try:
            self.db = MySQLdb.connect(self.host, self.userID, self.password, self.database)
        except:
            print 'error initialising database'

    def __del__(self):
        self.db.close()

    def setUpFileInfo(self):
        cursor = self.db.cursor()
        cursor.execute('DROP TABLE IF EXISTS FILES')
        cursor.execute('CREATE TABLE FILES(FILE_ID INT NOT NULL,LINK VARCHAR(150))')
        try:
            self.db.commit()
        except Exception, e:
            self.db.rollback()
            print e

    def setUpIDF(self):
        maxlenWord = 20
        try:
            cursor = self.db.cursor()
            cursor.execute("DROP TABLE IF EXISTS IDF")
            idf = 'CREATE TABLE IDF(WORD CHAR(%d) NOT NULL,' % maxlenWord
            idf += 'IDF_VALUE FLOAT)'
            cursor.execute(idf)
            self.db.commit()
        except Exception, e:
            self.db.rollback()
            print e
            print 'Error creating idf database'

    def setUpTF(self, doc_num):
        # n is the number of files to be indexed
        # set up TF and IDF databases
        maxlenWord = 20
        try:
            cursor = self.db.cursor()
            cursor.execute('DROP TABLE IF EXISTS DOC' + str(doc_num))
            tf = 'CREATE TABLE DOC%d(WORD CHAR(%d) NOT NULL,' % (doc_num, maxlenWord)
            tf += 'TF_VALUE FLOAT)'
            cursor.execute(tf)
            self.db.commit()
        except Exception, e:
            self.db.rollback()
            print e
            print 'Error creating tf database ', doc_num

    def getStopwords(self):
        with open(self.stopWordFile) as F_Stop:
            self.stopWordSet = set(F_Stop.read().split(' '))

    def IDF_insert(self):
        cursor = self.db.cursor()
        # for every word get freq of no of tables it is part of store it in idf table then
        for i in xrange(1, self.N + 1):
            insertion_cursor = self.db.cursor()
            traversal_cursor = self.db.cursor()
            traversal_cursor.execute("SELECT WORD FROM DOC%d" % i)
            for current_word in traversal_cursor:
                c = 0
                for j in xrange(1, self.N + 1):
                    inner_query = "SELECT * FROM DOC%d WHERE WORD='%s'" % (j, current_word[0])
                    temp_cursor = self.db.cursor()
                    temp_cursor.execute(inner_query)
                    if temp_cursor.rowcount > 0:
                        c += 1
                c = math.log(self.N / float(c))
                if c != 0:
                    insertion_cursor.execute("INSERT INTO IDF(WORD,IDF_VALUE) VALUES('%s',%f)" % (current_word[0], c))
        try:
            self.db.commit()
        except Exception, e:
            self.db.rollback()
            print e


    def TF_insert(self, fid, word, count_total, word_freq):
        # calculates TF and inserts into table TF
        cursor = self.db.cursor()
        value = float(word_freq) / (count_total)
        try:
            cursor.execute(("SELECT * FROM DOC%d WHERE WORD='%s'" % (fid, word)))
            present = cursor.rowcount > 0
            if not present:
                cursor.execute(("INSERT INTO DOC%d(WORD,TF_VALUE) VALUES('%s',%f)" % (fid, word, value)))
            else:
                query_update = 'UPDATE TF SET DOC' + str(fid) + ('=%f ' % value) + ("WHERE WORD='%s'" % word)
                cursor.execute(query_update)
        except Exception, e:
            print e
            # print 'Error entering value to data base for %s' % word

    def addToDatabase(self, F, listOfWords, fid):
        print 'Indexing file %d' % fid
        hashtable_words = {}
        hashtable_words = defaultdict(lambda: 0, hashtable_words)
        for word in listOfWords:
            hashtable_words[word] = hashtable_words[word] + 1
        cnt = len(listOfWords)
        self.setUpTF(fid)
        for word in hashtable_words:
            self.TF_insert(fid, word, cnt, hashtable_words[word])
        try:
            self.db.commit()
        except Exception, e:
            self.db.rollback()
            print e

    def removeStopWords(self, wordlist):
        return [x for x in wordlist if x not in self.stopWordSet]

    def fetchStemmedWords(self, path):
        with open(path, 'r') as F:
            text = F.read().lower()
            text = re.sub(r'[^a-z0-9 ]', ' ', text)
            listOfWords = text.split(' ')
            listOfWords = self.removeStopWords(listOfWords)
            #listOfWords = [stemmer.stem(word, 0, len(word) - 1) for word in listOfWords]
        return listOfWords

    def parseFile(self, path_to_file, fid):
        listOfWords = self.fetchStemmedWords(path_to_file)
        with open(path_to_file, 'r') as F:
            self.addToDatabase(F, listOfWords, fid)

    def insertFile(self, id, f):
        cur = self.db.cursor()
        cur.execute(("INSERT INTO FILES(FILE_ID,LINK) VALUES(%d,'%s')" % (id, f)))


    def createIndex(self, pathtofolder):
        filesinside = []
        self.setUpFileInfo()
        ID = 0
        for f in os.listdir(pathtofolder):
            if os.path.isfile(os.path.join(pathtofolder, f)):
                f = os.path.join(pathtofolder, f)
                filesinside.append(f)
                ID += 1
                self.insertFile(ID, f)
        try:
            self.db.commit()
        except Exception, e:
            self.db.rollback()
            print e

        self.N = ID
        self.setUpIDF()
        self.getStopwords()
        for i in xrange(1, self.N + 1):
            self.parseFile(filesinside[i - 1], i)
        self.IDF_insert()
#######################################
