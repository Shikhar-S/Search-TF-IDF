from timeit import default_timer as timer
from Tkinter import *
from ttk import *
import re
from Querying import Querying
class Searcher:
    def __init__(self,parent,path,width="576",height="475"):
        self.path=path
        self.parent = parent
        self.window = Toplevel(parent)
        self.window.geometry(width + 'x' + height)
        self.window.title("File Searcher")
        self.srch_label=Label(self.window,text='Enter Search Query:')
        self.srch_box=Text(self.window,height=1,width=50)
        self.search_button=Button(self.window,command=self.start_search,text='Search')
        self.label_frame=LabelFrame(self.window,text='Search Results')
        self.pack()
        self.window.mainloop()

    def pack(self):
        self.srch_label.pack(side="top",padx=5,pady=5)
        self.srch_box.pack(padx=5,pady=5)
        self.search_button.pack(padx=5,pady=5)
        self.label_frame.pack(padx=5,pady=5,fill='both',expand='yes')

    def start_search(self):
        search_query = self.srch_box.get("1.0", END)
        queryProcessor = Querying(path_to_folder=self.path,query=search_query)
        start = timer()
        result=queryProcessor.processQuery()
        end = timer()
        print 'Time taken to search %f' % (end - start)
        self.display(result)

    def display(self,result):
        labels=[]
        for i in xrange(0,len(result)):
            labels.append(Label(self.label_frame,textvariable=result[i]))
        for t in labels:
            t.pack()

