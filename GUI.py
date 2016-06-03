from timeit import default_timer as timer
from Tkinter import *
import tkFileDialog
from Index_individual import Indexing
class File_Loader:
    def __init__(self,parent,width="576",height="475"):
        self.parent=parent
        self.window=Toplevel(parent)
        self.window.geometry(width+'x'+height)
        self.window.title("FILE_LOADER")
        self.Label_dir=Label(self.window,text="Enter Directory path:")
        self.text_field_dir=Text(self.window,height=1,width=60)
        self.dir_button=Button(self.window,command=self.selectDirectory,text="Select Directory")
        self.Label_stpwrd=Label(self.window,text="Enter stopword file path")
        self.text_field_stpwrd=Text(self.window,height=1,width=60)
        self.stpwrd_button=Button(self.window,command=self.selectStopwordFile,text="Select file")
        self.Label_stemmers=Label(self.window,text="Select Stemming Algorithm")
        self.list_stemmers=Listbox(self.window,selectmode=SINGLE)
        self.list_stemmers.insert(1,"Porter Stemmer")
        self.list_stemmers.insert(2,"Lovins")
        self.list_stemmers.insert(3,"Paice-Husk")
        self.button_index=Button(self.window,text="Index",command=self.startIndexing)
        self.button_search=Button(self.window,text="Search",command=self.startSearching)
        self.message_label=Label(self.window,text="Select Directory to search,Stopwords file,Stemming algo")
        self.dir_path=''
        self.stopwords_path=''
        self.pack()
        self.window.mainloop()

    def pack(self):
        self.Label_dir.pack(side="top",padx=5,pady=5)
        self.text_field_dir.pack(padx=5,pady=5)
        self.dir_button.pack(padx=5,pady=5)
        self.Label_stpwrd.pack(padx=5,pady=5)
        self.text_field_stpwrd.pack(padx=5,pady=5)
        self.stpwrd_button.pack(padx=5,pady=5)
        self.Label_stemmers.pack(padx=10,pady=5,anchor=W)
        self.list_stemmers.pack(padx=25,pady=5,anchor=W)
        self.button_index.pack(padx=5,pady=5,side="right")
        self.button_search.pack(padx=5,pady=5,side="right")
        self.message_label.pack(anchor=S)

    def selectDirectory(self):
        text_dir_box=self.text_field_dir.get("1.0",END)
        if text_dir_box== "\n":
            self.dir_path=tkFileDialog.askdirectory(initialdir='C:\\',mustexist=False,parent=self.window,title='Select Direcotry')
        else:
            self.dir_path=text_dir_box[0:len(text_dir_box)-1]


    def selectStopwordFile(self):
        text_stpwrd_box = self.text_field_dir.get("1.0", END)
        if text_stpwrd_box == "\n":
            file_opt = options = {}
            options['defaultextension'] = '.txt'
            options['filetypes'] = [('text files', '.txt')]
            options['initialdir'] = 'C:\\'
            options['parent'] = self.window
            options['title'] = 'Select stopwords file'
            self.stopwords_path = tkFileDialog.askopenfilename(**file_opt)
        else:
            self.stopwords_path = text_stpwrd_box[0:len(text_stpwrd_box) - 1]

    def canProceedIndexing(self): #can provide checks in this method to avoid program from crashing
        return self.stopwords_path != '' and self.dir_path!=''

    def startIndexing(self):
        if self.canProceedIndexing():
            start=timer()
            indexer = Indexing(self.stopwords_path)
            indexer.createIndex(self.dir_path)
            end=timer()
            print end-start
        else:
            #change error text here
            self.message_label.config(text='Enter Directory and Stopword File Paths!!',fg="red")

    def startSearching(self):
        if self.canProceedIndexing():
            pass
        else:
            # change error text here
            self.message_label.config(text='Enter Directory and Stopword File Paths!!',fg='red')

root=Tk()
root.iconify()
FL=File_Loader(root)
'''
https://docs.python.org/2/library/tkinter.html
http://www.tutorialspoint.com/python/python_gui_programming.htm
http://tkinter.unpythonic.net/wiki/tkFileDialog
http://www.i-programmer.info/programming/python/5073-creating-the-python-ui-with-tkinter.html
http://effbot.org/zone/tkinter-geometry.htm
http://effbot.org/tkinterbook/label.htm
'''
