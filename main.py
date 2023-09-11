from tkinter import *
from tkinter import ttk
from datetime import datetime
import time


class TLDClock():
    def __init__(self,window):
        #window App
        self.window = window
        self.window.title("Bamboo Clock")
        self.window.iconbitmap("./img/Bamboohr.ico")
        self.window.eval("tk::PlaceWindow . center")
        # self.window.resizable(0,0)
        self.window.geometry("440x400")

        #Frames
        self.frame1 = Frame(self.window,bg="#2c2c2c",width=440,height=400)
        self.frame2 = Frame(self.window,bg="#2c2c2c",width=440,height=400)
        self.container = LabelFrame(self.frame2, text="Time",padx=5,pady=5)

        #current_hour
        current_hour = Label(self.container,text="Current Hour :")
        current_hour.config(bg="#2c2c2c",fg="#fff")
        current_hour.grid(row=2,column=0,padx=5,pady=2,sticky=W)
        self.showHour = Label(self.container)

        self.frame_Principal()
        

    def clear_widgets(self,frame):
         # select all frame widgets and delete them
            frame.destroy() 
    
    def menu(self):
        pass

    def frame_Principal(self):
        #Principal Frame
        self.frame1.pack(fill="both",expand=1)
        
        #Image
        logo = PhotoImage(file="./img/bamboohr.png")
        image = Label(self.frame1,image=logo,width=150,height=150)
        image.pack(side="top",pady=40)

        #Label
        text_Content = "Welcome to Automatic BambooHr Bot\n it helps you to control your clock in and clock out"
        welcome = Label(self.frame1, text=text_Content)
        welcome.config(bg="#2c2c2c",fg="#fff")
        welcome.pack(pady=10)
        
        #Button
        Button(self.frame1,text="Let's go",command=self.frame_Sencond,width=10,height=20).pack(side="bottom",pady=40)

        
    
    def frame_Sencond(self):
        self.clear_widgets(self.frame1)
        self.digitalClock()
        # #Date

        # #Second frame
        self.frame2.pack(fill="both",expand=1)

        #Date Container
        self.container.config(bg="#2c2c2c",fg="#fff")
        self.container.grid(row=0,column=0,columnspan=4,padx=110,pady=20,sticky=N)
        
        #Date
        today = datetime.now()
        # todayNow = f"{today.day} / {today.month} / {today.year}"
        date_time = today.strftime("%d %B %Y")
        day_name = today.strftime("%A")

        #Date LAbel
        date = Label(self.container,text="Date : ")
        date.config(bg="#2c2c2c",fg="#fff")
        date.grid(row=0,column=0,padx=5,pady=2,sticky=W)

        date_text = Label(self.container,text=date_time)
        date_text.config(bg="#2c2c2c",fg="#fff")
        date_text.grid(row=0,column=1,padx=2,pady=2,sticky=W)

        #Day Label
        day = Label(self.container,text="Day : ",bg="#2c2c2c")
        day.config(bg="#2c2c2c",fg="#fff")
        day.grid(row=1,column=0,padx=5,pady=2,sticky=W)

        day_text = Label(self.container,text=day_name)
        day_text.config(bg="#2c2c2c",fg="#fff")
        day_text.grid(row=1,column=1,padx=2,pady=4,sticky=W)

        #New Frame

        
        
    def digitalClock(self):
        today_text = time.strftime("%H:%M:%S")
        #Labels
        self.showHour.config(text=today_text,bg="#2c2c2c",fg="#fff")
        self.showHour.grid(row=2,column=1,padx=2,pady=4,sticky=W)
        self.showHour.after(200, self.digitalClock)    
        


if __name__ == "__main__":
    window = Tk()
    app = TLDClock(window)
    window.mainloop()