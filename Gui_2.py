from timeit import default_timer as timer
from Tkinter import *
from ttk import *
import tkFileDialog
from Querying import Querying
class Searcher:
    def __init__(self,parent,width="576",height="475"):
        self.parent = parent
        self.window = Toplevel(parent)
        self.window.geometry(width + 'x' + height)
        self.window.title("File Searcher")
        self.srch_label=Label(self.window,text='Enter Search Query:')
        self.srch_box=Text(self.window,height=1,width=50)
        self.search_button=Button(self.window,command=self.start_search,text='Search')
        self.pack()
        self.window.mainloop()
    def pack(self):
        pass
    def start_search(self):
        pass