from timeit import default_timer as timer
from Tkinter import *
from ttk import *
import webbrowser
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
        self.label_frame=None
        self.pack()
        self.window.mainloop()

    def pack(self):
        self.srch_label.pack(side="top",padx=5,pady=5)
        self.srch_box.pack(padx=5,pady=5)
        self.search_button.pack(padx=5,pady=5)


    def refreshresults(self):
        if self.label_frame is not None:
            self.label_frame.destroy()
        self.label_frame=LabelFrame(self.window, text='Search Results')
        self.label_frame.pack(padx=5, pady=5, fill='both', expand='yes')

    def start_search(self):
        self.refreshresults()
        search_query = self.srch_box.get("1.0", END)
        queryProcessor = Querying(path_to_folder=self.path,query=search_query)
        start = timer()
        result=queryProcessor.processQuery()
        end = timer()
        print 'Time taken to search %f' % (end - start)
        self.display(result)

    def open_in_browser(self,event):
        add="file://"+event.widget['text']
        webbrowser.open_new(add)


    def display(self,result):
        labels=[]
        for i in xrange(0,len(result)):
            labels.append(Label(self.label_frame,text=result[i]))
            labels[i].config(foreground='blue')
        for t in labels:
            t.pack()
            t.bind("<Button-1>",self.open_in_browser)

