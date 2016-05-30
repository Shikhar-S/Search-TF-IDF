from Index_individual import Indexing
path=raw_input('Enter file path:\n')
stop=raw_input('Enter stopword file path:\n')
indexer=Indexing(stop)
indexer.createIndex(path)
