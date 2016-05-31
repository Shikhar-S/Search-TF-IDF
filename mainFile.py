import Index_individual
from Querying import Querying
from timeit import default_timer as timer
import os
path=raw_input('Enter folder name:\n')
path=os.path.join(os.getcwd(),path)
stop=raw_input('Enter stopword file name:\n')
stop=os.path.join(os.getcwd(),stop)
flag=raw_input("Do indexing?? Y: Yes N:NO\n")
if flag=='Y':
    start=timer()
    indexer=Index_individual.Indexing(stop)
    indexer.createIndex(path)
    end=timer()
    print 'Time taken to index %d files = %f' % (indexer.N,end-start)

queryProcessor=Querying(path)
queryProcessor.getQuery()
start=timer()
queryProcessor.processQuery()
end=timer()
print 'Time taken to search %f' % (end-start)
