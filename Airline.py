from tkinter import *
from login import Login
from mysql.connector import connect, Error
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime

class Application():
    root = Tk()
    mode = 1                                                #Default mode: 0-light, 1-dark                             
    topBarColor = ['#78aaad','#0f343b']
    primary = ['#d6dbce','#40676e']
    primaryfg = ['#202d2e','#b0e1eb']
    secondary = ['#69878a','#113036']
    buttons = ['#88a6a8','#19464f']
    buttonsfg = ['black','white']
    Frames = [0,0,0,0,0,0]

    def __init__(self):
        self.HomeFn()

    # Event Bindings for entering leaving buttons
    #------------------------------------------------

    def enterEvent(self, e):
        e.widget.config(cursor='hand2', bg=self.secondary[self.mode])
        pass

    def leaveEvent(self, e):
        e.widget.config(cursor='arrow', bg=self.buttons[self.mode], fg=self.buttonsfg[self.mode])
        pass

    def changeMod(self):
            self.mode = 1-self.mode
            for i in self.root.winfo_children():
                i.destroy()
            self.HomeFn()
    
    def sqlConnection(self, query):
        try:
            with connect(
                host="localhost",
                user = 'root', 
                password = "mysqlserver78",
                database = "airline"
            ) as connection:
            
                with connection.cursor() as cursor: 
                    cursor.execute(query)
                    result = cursor.fetchall()
                    connection.commit()

                connection.close()
                return result

        except Error as error:
            print(error)
        pass

    def HomeFn(self):
        root = self.root
        self.width = root.winfo_screenwidth()
        self.height = root.winfo_screenheight()

        root.geometry('900x600+220+50')
        root.state('zoomed')
        root.title('Fly Anytime, Anywhere')

        topBar = Frame(root, width=self.width, height=50, bg=self.topBarColor[self.mode])
        topBar.pack()
        topBar.pack_propagate(False)

        label = Label(topBar, font="Arial 12 bold", text='Fly Anytime, Anywhere!')
        label.config(bg=self.topBarColor[self.mode], fg='white')
        label.place(x=(self.width/2), y=26, anchor='center')

        for i in range(0, 6):
            frame = Frame(root, height=self.height, width=self.width, bg=self.primary[self.mode])
            frame.place(x=0, y=50)
            self.Frames[i] = frame

        self.auth = Login(self)
        pass


    def LabelMaker(self, text, master, coord, width=20):
        label = Label(master, text=text, width=width, height=6,font='Arial 16 bold')
        label.config(bg=self.buttons[self.mode],fg=self.buttonsfg[self.mode] )
        label.place(x=coord[0], y=coord[1], anchor='nw')
        return label
    

    def firstScreen(self):

        for i in range(0, 6):
            label = Label(master=self.Frames[i], bg=self.primary[self.mode], fg='white')
            label.config(text=self.auth.userName, font='Arial 17 bold')
            label.place(x=self.width/2, y=40, anchor='center')

        self.Frames[1].tkraise()
        parent = self.Frames[1]

        def logoutFn():
            self.Frames[0].tkraise()

        logoutBtn = Button(parent, text='Log Out', font='Arial 12 bold', bg=self.buttons[self.mode], fg='white')
        logoutBtn.config(command=logoutFn, width=12, height=2)
        logoutBtn.place(x=20, y=20)
    
        logoutBtn.bind("<Enter>", self.enterEvent)
        logoutBtn.bind("<Leave>", self.leaveEvent)

        viewRLabel = self.LabelMaker("My Reservations", parent, [250, 200])
        newRLabel = self.LabelMaker("New Reservation", parent, [550, 200])
        flightDetailsLabel = self.LabelMaker("Flights Details", parent, [850, 200])
        
        labels = [viewRLabel, newRLabel, flightDetailsLabel]

        for i in labels:
            i.bind("<Enter>", self.enterEvent)
            i.bind("<Leave>", self.leaveEvent)
        
        viewRLabel.bind("<Button>",self.viewReservationScreen)
        newRLabel.bind("<Button>",self.NewReservationScreen)
        flightDetailsLabel.bind("<Button>",self.flightDetailsScreen)


    def viewReservationScreen(self, e):
        self.Frames[2].tkraise()
        parent = self.Frames[2]

        backBtn = Button(parent, text='Back', font='Arial 12 bold', bg=self.buttons[self.mode], fg='white')
        backBtn.config(command=self.firstScreen, width=12, height=2)
        backBtn.place(x=20, y=20)

        backBtn.bind("<Enter>", self.enterEvent)
        backBtn.bind("<Leave>", self.leaveEvent)

        query = "Select * from reservation where customer_id = \'" + self.auth.userID +"\'"
        result = self.sqlConnection(query)

        if(len(result) == 0):
            displayMsg = Label(text='You have no reservations right now!', font='Arial 18 bold')
            displayMsg.config(bg=self.primary[self.mode], fg='light grey')
            displayMsg.place(x=self.width/2, y=(self.height/2)-50, anchor='center')
        else:
            xframe = Frame(parent, height=370, bg='red', width=820)
            xframe.place(x=290, y=120)

            canvas = Canvas(xframe)
            canvas.place(x=0, y=0, relheight=1, relwidth=1)
            
            self.trv1 = ttk.Treeview(canvas,height=20, selectmode ='browse')
            self.trv1.pack(side=LEFT)

            treeScroll = ttk.Scrollbar(canvas)
            treeScroll.configure(command=self.trv1.yview)
            self.trv1.configure(yscrollcommand=treeScroll.set)
            treeScroll.pack(side=RIGHT,fill=BOTH)

            style = ttk.Style()
            style.configure("Treeview.Heading", font='Arial 12 bold')
            style.configure("Treeview",font='Arial 12 bold' )

            self.trv1["columns"] = ("1", "2", "3","4","5")
            self.trv1['show'] = 'headings'

            self.trv1.column("1", width = 130, anchor ='c')
            self.trv1.column("2", width = 180, anchor ='c')
            self.trv1.column("3", width = 180, anchor ='c')
            self.trv1.column("4", width = 180, anchor ='c')
            self.trv1.column("5", width = 130, anchor ='c')

            self.trv1.heading("1", text ="Reservation ID")
            self.trv1.heading("2", text ="Departure Date")
            self.trv1.heading("3", text ="Departure Area")
            self.trv1.heading("4", text ="Travel Class")  
            self.trv1.heading("5", text ="Flight ID")

            for dt in result: 
                self.trv1.insert("", 'end',iid=dt[0], text=dt[0],
                        values =(dt[0],dt[1],dt[2],dt[3],dt[5]))


    def flightDetailsScreen(self, e):
        self.Frames[4].tkraise()
        parent = self.Frames[4]

        backBtn = Button(parent, text='Back', font='Arial 12 bold', bg=self.buttons[self.mode], fg='white')
        backBtn.config(command=self.firstScreen, width=12, height=2)
        backBtn.place(x=20, y=20)

        backBtn.bind("<Enter>", self.enterEvent)
        backBtn.bind("<Leave>", self.leaveEvent)

        query = "Select * from flight where flight_id in (Select flight_id from reservation where customer_id = \'" + self.auth.userID +"\')"
        result = self.sqlConnection(query)

        if(len(result) == 0):
            displayMsg = Label(text='You have no flights right now!', font='Arial 18 bold')
            displayMsg.config(bg=self.primary[self.mode], fg='light grey')
            displayMsg.place(x=self.width/2, y=(self.height/2)-50, anchor='center')
        else:
            xframe = Frame(parent, height=370, bg='red', width=960)
            xframe.place(x=230, y=120)

            canvas = Canvas(xframe)
            canvas.place(x=0, y=0, relheight=1, relwidth=1)
            
            self.trv2 = ttk.Treeview(canvas,height=20, selectmode ='browse')
            self.trv2.pack(side=LEFT)

            treeScroll = ttk.Scrollbar(canvas)
            treeScroll.configure(command=self.trv2.yview)
            self.trv2.configure(yscrollcommand=treeScroll.set)
            treeScroll.pack(side=RIGHT,fill=BOTH)

            style = ttk.Style()
            style.configure("Treeview.Heading", font='Arial 12 bold')
            style.configure("Treeview",font='Arial 12 bold' )

            self.trv2["columns"] = ("1", "2", "3","4","5","6")
            self.trv2['show'] = 'headings'

            self.trv2.column("1", width = 150, anchor ='c')
            self.trv2.column("2", width = 180, anchor ='c')
            self.trv2.column("3", width = 180, anchor ='c')
            self.trv2.column("4", width = 150, anchor ='c')
            self.trv2.column("5", width = 130, anchor ='c')
            self.trv2.column("6", width = 150, anchor ='c')

            self.trv2.heading("1", text ="Flight ID")
            self.trv2.heading("2", text ="Pilot Name")
            self.trv2.heading("3", text ="Flight Model")
            self.trv2.heading("4", text ="Departure Date")
            self.trv2.heading("5", text ="Departure Time")  
            self.trv2.heading("6", text ="Seats Available")

            for dt in result: 
                self.trv2.insert("", 'end',iid=dt[0], text=dt[0],
                        values =(dt[0],dt[1],dt[2],dt[3],dt[4],dt[5]))


    def makeEntry(self, parent, coord):
        tmp = Label(parent, width=27, bg='white')
        tmp.place(x=coord[0],y=coord[1], anchor='nw')       
    
        entry = Entry(parent, bd=0, font = 'Arial 12', bg=self.primary[self.mode])
        entry.config(fg='white', insertbackground="white")
        entry.place(x=coord[0],y=coord[1],anchor="nw", width=200)
        return entry

    def makeLabel(self, parent, coord, text):
        label = Label(parent ,font="Arial 13 bold" ,text=text)
        label.config(fg='white', bg=self.primary[self.mode] )
        label.place(x=coord[0],y=coord[1] ,anchor="nw")
        return label

    def NewReservationScreen(self, e):
        parent = self.Frames[3]
        parent.tkraise()

        backBtn = Button(parent, text='Back', font='Arial 12 bold', bg=self.buttons[self.mode], fg='white')
        backBtn.config(command=self.firstScreen, width=12, height=2)
        backBtn.place(x=20, y=20)

        backBtn.bind("<Enter>", self.enterEvent)
        backBtn.bind("<Leave>", self.leaveEvent)

        self.cal = Calendar(parent, selectmode = 'day')
        self.selector = 0
        def viewCalendar():
            self.selector = 1
            self.cal.place(x=850, y=200)

        self.makeLabel(parent, [400, 200], "Departure Date")
        self.makeLabel(parent, [400, 240], "Departure Area")
        self.makeLabel(parent, [400, 280], "Travel Class")
        self.makeLabel(parent, [400, 320], "Flight ID")

        self.deptDate = Button(parent, text='Select Date', font='Arial 12 bold', bg=self.secondary[self.mode])
        self.deptDate.config(fg='white', width=19, command=viewCalendar)
        self.deptDate.place(x=600, y=195)

        self.deptArea = self.makeEntry(parent, [600, 240])
        self.travelClass = self.makeEntry(parent, [600, 280])
        self.flight = self.makeEntry(parent, [600, 320])

        self.submitBtn = Button(parent, text = "Submit", font = "Arial 12 bold",
                             bg=self.buttons[self.mode], fg="white", width=30,
                             command = self.makeReservation)
        self.submitBtn.place(x=500,y=380,anchor="nw")

        self.submitBtn.bind("<Enter>", self.enterEvent)
        self.submitBtn.bind("<Leave>", self.leaveEvent)
        pass

    def makeReservation(self):
        deptDate = self.cal.get_date()
        deptArea = self.deptArea.get()
        travelClass = self.travelClass.get()
        flightID = self.flight.get()

        if(deptArea == "" or travelClass =="" or flightID ==""):
            self.errorMsg("Please Enter Data", self.Frames[3])
        elif(self.selector == 0):
            self.errorMsg("Please Select Date", self.Frames[3])
        elif(deptArea.isnumeric()):
            self.errorMsg("Area cannot be a Number", self.Frames[3])
        elif(travelClass.isnumeric()):
            self.errorMsg("Travel Class cannot be a Number", self.Frames[3])
        else:
            result = self.sqlConnection("Select max(reservation_id) from reservation")
            res_id = str(int(result[0][0])+1)

            datetime_object = datetime.strptime(deptDate, '%m/%d/%y')
            deptDate = datetime_object.strftime('%Y-%m-%d')

            query = "Insert into reservation Values (\'"+res_id+"\',\'"+deptDate+"\',\'"+deptArea+"\',\'"+travelClass+"\',\'"+self.auth.userID+"\',\'"+flightID+"\')"
            self.sqlConnection(query)

            self.deptArea.delete(0,END)
            self.travelClass.delete(0,END)
            self.flight.delete(0,END)
            
            self.errorMsg("Reservation Successful!", self.Frames[3])
            
        pass
    
    def errorMsg(self, text, parent):
        warning = Label(parent, text=text, font="Arial 10 bold")
        warning.config(bg=self.primary[self.mode], fg="white")
        warning.place(x=570, y=450, anchor='nw')
        self.root.after(1500, warning.destroy)

app = Application()
app.root.mainloop()
