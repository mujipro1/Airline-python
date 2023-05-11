from tkinter import *
from mysql.connector import connect, Error

class Login:
    userID = ''
    def __init__(self, parent):
        self.parent = parent
        parent = parent.Frames[0]
        parent.tkraise()

        self.userLabel = Label(parent ,font="Arial 13 bold" ,text="Customer ID")
        self.userLabel.config(fg='white', bg=self.parent.primary[self.parent.mode] )
        self.userLabel.place(x=520,y=280,anchor="nw")

        self.userEntry = self.makeEntry(parent,[640, 280])

        self.submitBtn = Button(parent, text = "Submit", font = "Arial 12 bold",
                             bg=self.parent.buttons[self.parent.mode], fg="white", width=30,
                             command = lambda:self.submit(parent))
        self.submitBtn.place(x=500,y=350,anchor="nw")

        self.submitBtn.bind("<Enter>", self.parent.enterEvent)
        self.submitBtn.bind("<Leave>", self.parent.leaveEvent)

        pass

    def makeEntry(self, parent, coord):
        tmp = Label(parent, width=20, bg='white')
        tmp.place(x=coord[0],y=coord[1], anchor='nw')       
    
        entry = Entry(parent, bd=0, font = 'Arial 12', bg=self.parent.primary[self.parent.mode])
        entry.config(fg='white', insertbackground="white")
        entry.place(x=coord[0],y=coord[1],anchor="nw", width=150)
        return entry

    def submit(self, parent):
        username = self.userEntry.get()

        self.userEntry.delete(0, 'end')

        auth = self.mySql(username)
        
        if(auth == True):
            self.parent.firstScreen()            
        else:
            warning = Label(parent, text = "Invalid Credentials ! Try Again", font="Arial 10 bold")
            warning.config(bg=self.parent.primary[self.parent.mode], fg="white")
            warning.place(x=570, y=400, anchor='nw')
            parent.after(1500, warning.destroy)

    def mySql(self, username):        
        query = "Select * from customer"
        result = self.parent.sqlConnection(query)
        for id in result:
            if (id[0] == username):
                    self.userName = id[1] + " " + id[2]
                    self.userID = id[0]
                    return True                
        return False        