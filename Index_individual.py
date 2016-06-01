__author__ = 'Shikhar'
import os
import MySQLdb
import re
import math
import warnings
import porter2
from collections import defaultdict

#stemmer = PorterStemmer()
warnings.filterwarnings('ignore', 'Unknown table')


class Indexing:
    '''
    Indexes docs
    '''
    def __init__(self, stpwrdfile, usID='shikhar', pswd='password', dbase='indexing_project', hst='localhost'):
        '''
        :param stpwrdfile: File path containing stopwords to be filtered
        :param usID: User ID for database connection
        :param pswd: password for database connection
        :param dbase: Name of the datbase
        :param hst: database hosted at @host
        '''
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
        '''
        :return: Creates a database schema on disk to store File info, namely id, path, length
        '''
        cursor = self.db.cursor()
        cursor.execute('DROP TABLE IF EXISTS FILES')
        cursor.execute('CREATE TABLE FILES(FILE_ID INT NOT NULL,LINK VARCHAR(150),LENGTH INT)')
        try:
            self.db.commit()
        except Exception, e:
            self.db.rollback()
            print e

    def setUpIDF(self):
        '''
        :return: Creates IDF table on disk to store word and IDF_VALUE
        '''
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
        '''
        :param doc_num: doc for which TF table has to be made.
        :return: Creates TF table on disk for given doc to store word and TFF_VALUE. Mame of table is DOCi for i=doc_num
        '''
        maxlenWord = 20 #maximum possible length of word
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
        '''
        :return:generates a Set of stopwords from the given stopword file
        '''
        with open(self.stopWordFile) as F_Stop:
            self.stopWordSet = set(F_Stop.read().split(' '))

    def IDF_insert(self):
        '''
        :return: finds IDF value for all words and insert them
        '''
        for i in xrange(1, self.N + 1):
            print 'Indexing IDF value for file %d' % i
            insertion_cursor = self.db.cursor()
            traversal_cursor = self.db.cursor()
            temp_cursor=self.db.cursor()
            traversal_cursor.execute("SELECT WORD FROM DOC%d" % i)

            for current_word in traversal_cursor:
                c = 0
                temp_cursor.execute(("SELECT * FROM IDF WHERE WORD='%s'" % current_word))
                if temp_cursor.rowcount==0:
                    for j in xrange(1, self.N + 1):
                        inner_query = "SELECT * FROM DOC%d WHERE WORD='%s'" % (j, current_word[0])
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
        '''
        :param fid: doc id for which TF value have to be caluclated
        :param word: word whose TF value is calc
        :param count_total: total number of words in given doc
        :param word_freq: freq of word in given doc
        :return: calculates and stores TF value in DOCi table
        '''
        cursor = self.db.cursor()
        value = float(word_freq) / (count_total)
        try:
            cursor.execute(("SELECT * FROM DOC%d WHERE WORD='%s'" % (fid, word)))
            present = cursor.rowcount > 0
            if not present:
                cursor.execute(("INSERT INTO DOC%d(WORD,TF_VALUE) VALUES('%s', %f)" % (fid, word, value)))
            else:
                query_update = 'UPDATE TF SET DOC' + str(fid) + ('=%f ' % value) + ("WHERE WORD='%s'" % word)
                cursor.execute(query_update)
        except Exception, e:
            print e
            # print 'Error entering value to data base for %s' % word

    def addToDatabase(self, FilePath, listOfWords, fid):
        '''
        :param FilePath:path of file to be indexed
        :param listOfWords: all the words in given file
        :param fid: id of given doc/file
        :return: processes each word by calc its freq and calling TF_insert function
        '''
        print 'Indexing file %d' % fid
        with open(FilePath,'r') as F:
            hashtable_words = {}
            hashtable_words = defaultdict(lambda: 0, hashtable_words)
            for word in listOfWords:
                hashtable_words[word] = hashtable_words[word] + 1
            cnt = len(listOfWords)
            self.setUpTF(fid)
            for word in hashtable_words:
                self.TF_insert(fid, word, cnt, hashtable_words[word])

    def removeStopWords(self, wordlist):
        '''
        :param wordlist: list of words in doc
        :return: filters stopwords
        '''
        return [x for x in wordlist if x not in self.stopWordSet]

    def fetchStemmedWords(self, path):
        '''
        :param path:path of doc
        :return: lowers and generates a filtered stemmed word list
        '''
        with open(path, 'r') as F:
            text = F.read().lower()
            text = re.sub(r'[^a-z0-9 ]', ' ', text)
            listOfWords = text.split(' ')
            listOfWords = self.removeStopWords(listOfWords)
            #listOfWords = [stemmer.stem(word, 0, len(word) - 1) for word in listOfWords]
            listOfWords=[porter2.stem(word) for word in listOfWords]
        return listOfWords

    def parseFile(self, path_to_file, fid):
        '''
        :param path_to_file:path of file to be indexed
        :param fid: id of file
        :return: processes the file by calling addToDatabase and insertFile functions
        '''
        listOfWords = self.fetchStemmedWords(path_to_file)
        self.insertFile(fid,path_to_file,len(listOfWords))
        self.addToDatabase(path_to_file, listOfWords, fid)

    def insertFile(self, id, f,count):
        '''
        :param id: id of doc
        :param f: path of doc
        :param count: number of words in doc
        :return: inserts these values to FILES table
        '''
        cur = self.db.cursor()
        cur.execute(("INSERT INTO FILES(FILE_ID,LINK,LENGTH) VALUES(%d,'%s',%d)" % (id, f, count)))


    def createIndex(self, pathtofolder):
        '''
        :param pathtofolder:Folder containing all files to be indexed
        :return: indexes all docs in given folder
        '''
        filesinside = []
        self.setUpFileInfo()
        ID = 0
        for f in os.listdir(pathtofolder):
            if os.path.isfile(os.path.join(pathtofolder, f)):
                f = os.path.join(pathtofolder, f)
                filesinside.append(f)
                ID += 1


        self.N = ID
        self.setUpIDF()
        self.getStopwords()
        for i in xrange(1, self.N + 1):
            self.parseFile(filesinside[i - 1], i)
        try:
            self.db.commit()
        except Exception, e:
            self.db.rollback()
            print e
        self.IDF_insert()

#######################################
