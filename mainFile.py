'''
import Index_individual
from Querying import Querying
from Query_MMM import Query_MMM
from timeit import default_timer as timer
import os
path=raw_input('Enter folder name:\n')
path=os.path.join(os.getcwd(),path)
stop=raw_input('Enter stopword file name:\n')
stop=os.path.join(os.getcwd(),stop)
flag=raw_input("Do indexing?? Y: Yes N:NO\n")
indexer=Index_individual.Indexing(stop)
if flag=='Y':
    start=timer()
    indexer.createIndex(path)
    end=timer()
    print 'Time taken to index %d files = %f' % (indexer.N,end-start)
###################################
queryProcessor=Querying(path)
queryProcessor.getQuery()
start=timer()
result=queryProcessor.processQuery()
end=timer()
for i in result:
    print i
print 'Time taken to search %f' % (end-start)
####################################
queryProcessor_MMM=Query_MMM(path)
queryProcessor_MMM.getQuery()
start=timer()
result=queryProcessor_MMM.processQuery()
end=timer()
for i in result:
    print i
print 'Time taken by MMM algo %f' % (end-start)
'''

from GUI import File_Loader
from Gui_2 import Searcher
from Tkinter import *
root=Tk()
root.iconify()
FL=File_Loader(root)
QS=Searcher(root,FL.dir_path)
