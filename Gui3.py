__author__='shikhar'
from Tkinter import *
from ttk import *
import MySQLdb
class Viewer:
    def __init__(self,parent,width="576", height="475", usID='shikhar', pswd='password', dbase='indexing_project', hst='localhost'):
        self.userID = usID
        self.password = pswd
        self.database = dbase
        self.host = hst
        try:
            self.db = MySQLdb.connect(self.host, self.userID, self.password, self.database)
        except:
            print 'error initialising database'

        self.parent=parent
        self.window=Toplevel(self.parent)
        self.window.geometry(width + 'x' + height)
        self.window.title("VIEWER")
        self.doc_id_text = Text(self.window,height=1,width=5)
        self.view_button=Button(self.window,command=self.show,text='View')
        self.doc_id_label=Label(self.window,text='Enter Doc Number to view its database:')
        self.view_frame=Frame(self.window)
        self.view_screen = Text(self.view_frame, height=20, width=70)
        self.scrollbar = Scrollbar(self.view_frame,command=self.view_screen.yview)
        self.back_button = Button(self.window, text='Back', command=self.exit)
        self.paint()

    def paint(self):
        self.doc_id_label.pack(side="top",padx=5,pady=5)
        self.doc_id_text.pack(padx=5,pady=5)
        self.view_button.pack(padx=5,pady=5)
        self.scrollbar.pack(fill=Y,side='right')
        self.view_screen.config(yscrollcommand=self.scrollbar.set)
        self.view_screen.pack(padx=5,pady=5)

        self.back_button.pack(padx=5,pady=5)
        self.view_frame.pack(padx=5, pady=5, fill='both', expand='yes')

    def getData(self,doc_id):
        cursor=self.db.cursor()
        try:
            cursor.execute(('SELECT * FROM DOC%s' % doc_id))
            result=[]
            for row in cursor:
                result.append(row)
            return  result
        except Exception,e:
            print e
            print 'error getting data'

    def show(self):
        doc_id=self.doc_id_text.get('1.0',END)
        try:
            self.view_screen.config(state='normal')
            self.view_screen.delete(1.0,END)
            result=self.getData(doc_id)
            view='WORD \t TF_VALUE\n'
            for row in result:
                view=view+str(row[0])+'\t'+str(row[1])+'\n'
            self.view_screen.insert(INSERT,view)
            self.view_screen.config(state=DISABLED)
        except Exception,e:
            print e
            print doc_id


    def exit(self):
        self.window.quit()
        self.window.destroy()