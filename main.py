from tkinter import *
from tkinter import ttk
from datetime import datetime
import pickle
import time
import os
from tld import *
from dotenv import load_dotenv

load_dotenv()


class TLDClock():
    #Timer
    hour = 0
    minute = 0
    second = 0
    running = False

    def __init__(self,window):
        #window App
        self.window = window
        self.window.title("Bamboo Bot Clock")
        self.window.iconbitmap("./img/Bamboohr.ico")
        self.window.eval("tk::PlaceWindow . center")
        self.window.resizable(0,0)
        self.window.geometry("440x400")

        #Frames
        self.frame1 = Frame(self.window,bg="#2c2c2c",width=440,height=400)
        self.frame2 = Frame(self.window,bg="#2c2c2c",width=440,height=400)
        self.frameUser = Frame(self.window,bg="#2c2c2c",width=440,height=400)
        self.frameTime = Frame(self.window,bg="#2c2c2c",width=440,height=400)

        #Img
        self.logo = PhotoImage(file="./img/logo.PNG")
        #Container Time inside frame2
        self.container = LabelFrame(self.frame2, text="Time",padx=5,pady=5)

        #current_hour
        current_hour = Label(self.container,text="Current Hour :")
        current_hour.config(bg="#2c2c2c",fg="#fff")
        current_hour.grid(row=2,column=0,padx=5,pady=2,sticky=W)
        self.showHour = Label(self.container)

        #Counter Time
        self.counter = Label(self.frame2,font="12",padx=18,pady=10)
        current_time = f"{self.hour} : {self.minute} : {self.second}"
        self.counter.config(text=current_time,fg="#000")
        
        self.frame_Principal()
        
        #Getting Selenium-Scripts
        self.user = self.load_user_info()

        if(not(self.user == None)):
            self.email = self.user["email"]
            self.password = self.user["password"]
            #Clock - Bamboohr
            self.tld_clockIn = Clock_In(self.email,self.password)
            self.tld_clockOut = Clock_Out(self.email,self.password)
            self.tld_breakIn = Break_In(self.email,self.password)
            self.tld_breakOut = Break_Out(self.email,self.password)
        
    #Delete frame 1: principal
    def clear_widgets(self,frame):
        #destroy first frame
        frame.destroy()

    def hide_menu_frames(self):
        self.frame2.pack_forget()
        self.frameUser.pack_forget()
        self.frameTime.pack_forget()

    def menu(self):
        menuBar = Menu(self.window)
        self.window.config(menu=menuBar)

        #Menu options
        menuBar.add_command(label="Clock",command=self.frame_Sencond)

        settings = Menu(menuBar,tearoff=0)
        #Settings - options
        menuBar.add_cascade(label="Settings",menu=settings)
        #Optionces
        settings.add_command(label="User",command=self.frame_user)
        settings.add_command(label="Time",command=self.frame_time)
  
    def frame_Principal(self):
        #Principal Frame
        self.frame1.pack(fill="both",expand=1)
        
        #Image logo
        image = Label(self.frame1,image=self.logo)
        image.config(bg="#2c2c2c")
        image.pack(side="top",pady=30)

        #Label
        text_Content = "Welcome to Automatic BambooHr Bot\n it helps you to control your clock in and clock out\nMy the Force Be with You"
        welcome = Label(self.frame1, text=text_Content)
        welcome.config(bg="#2c2c2c",fg="#fff")
        welcome.pack(pady=5)
        
        #Button
        lets_go_button = Button(self.frame1,text="Let's go",command=self.frame_Sencond,width=10,height=20)
        lets_go_button.config(bg="#83c333",fg="#fff")
        lets_go_button.pack(side="bottom",pady=60)
 
    def frame_Sencond(self):
        self.clear_widgets(self.frame1)
        self.hide_menu_frames()
        self.menu()
        
        #Getting user
        user = self.load_user_info()

        if(not(user == None)):
            self.digitalClock()
        
        #Date

        #Second frame
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

        #Counter
        self.counter.grid(row=1,column=0,columnspan=4,padx=100,pady=40)

        self.digital_counter()
    #Settings : user
    def frame_user(self):
        self.hide_menu_frames()
        self.frameUser.pack(fill="both",expand=1)

        #Getting user
        user = self.load_user_info()

        #Framer user
        userInfo = LabelFrame(self.frameUser,text="User Info",padx=5,pady=5)
        userInfo.config(bg="#2c2c2c",fg="#fff")
        userInfo.grid(row=0,column=0,columnspan=4,padx=100,pady=100,sticky=N)
        
        # Lables
        #Email
        email_Label= Label(userInfo,text="Email :",padx=5,pady=10)
        email_Label.config(bg="#2c2c2c",fg="#fff")
        email_Label.grid(row=0,column=0,sticky=W)
        #Password
        password_Label = Label(userInfo,text="Password :",padx=5,pady=10)
        password_Label.config(bg="#2c2c2c",fg="#fff")
        password_Label.grid(row=1,column=0,sticky=W)

        # Entries
        if(user):
            #Email Entry
            email = Entry(userInfo,width=25,textvariable=StringVar(userInfo,user["email"]),state="disable")
            email.grid(row=0,column=1)
            #Password Entry
            password = Entry(userInfo,width=25,textvariable=StringVar(userInfo,user["password"]),state="disable")
            password.config(justify="left",show="*")
            password.grid(row=1,column=1)
        else:
            #Email Entry
            email = Entry(userInfo,width=25)
            email.grid(row=0,column=1)
            #Password Entry
            password = Entry(userInfo,width=25)
            password.config(justify="left",show="*")
            password.grid(row=1,column=1)

        #Frame buttons
        frameBtn = Frame(self.frameUser,width=280,height=50)
        frameBtn.config(bg="#2c2c2c")
        frameBtn.grid(row=2,column=0,columnspan=4)

        #Buttons
        # #Save Button
        save_btn = Button(frameBtn,text="Save",command=lambda:self.save_user(email.get(),password.get()))
        save_btn.config(bg="#83c333",fg="#fff",padx=20,pady=10)
        save_btn.grid(row=0,column=0,columnspan=2,padx=8) 

        #Edit Button
        edit_btn = Button(frameBtn,text="Clean",command=self.clean_user_info)
        edit_btn.config(bg="#ffff00",fg="#000",padx=20,pady=10)
        edit_btn.grid(row=0,column=2,columnspan=2,padx=8)

    def save_user(self,email,password):
        user = {"email":email,"password":password,"active": True}
        if(user["email"] and user["password"]):
            #Save data
            self.active = True
            #Creat Pickle Documet
            userData = open("./db/userinfo.pckl","wb")
            pickle.dump(user,userData)
        else:
            print("Fields are empties")
            pass
 
    def load_user_info(self):
        try:
            userdata = open("./db/userinfo.pckl","rb")
            user = pickle.load(userdata)
            return user
        except:
            pass

    def clean_user_info(self):
        #Delete file
        try:
            os.remove("./db/userinfo.pckl")
            self.frame_user()
        except:
            pass
    #Settings : time  
    def frame_time(self):
        self.hide_menu_frames()
        self.frameTime.pack(fill="both",expand=1)

        #Info Label
        info_text =Label(self.frameTime,text="Set your time, example: 14:00:00 (2pm) \n < hour:minute:second >\n in Military time format")
        info_text.config(bg="#2c2c2c",fg="#ff0000")
        info_text.grid(row=0,column=0,columnspan=4,pady=20)

        #Framer Time
        timer_settings = LabelFrame(self.frameTime,text="Timer",padx=5,pady=5)
        timer_settings.config(bg="#2c2c2c",fg="#fff")
        timer_settings.grid(row=1,column=0,columnspan=4,padx=150,pady=10,sticky=N)

        #Clock in
        clock_in = Label(timer_settings,text="Clock In :",padx=5,pady=10)
        clock_in.config(bg="#2c2c2c",fg="#fff")
        clock_in.grid(row=0,column=0,sticky=W)

        #Clock_in Entry
        clock_in_Entry = Entry(timer_settings,width=8)
        clock_in_Entry.grid(row=0,column=1)

        #Clock Out
        clock_out = Label(timer_settings,text="Clock Out :",padx=5,pady=10)
        clock_out.config(bg="#2c2c2c",fg="#fff")
        clock_out.grid(row=3,column=0,sticky=W)

        #Clock_in Entry
        clock_out_Entry = Entry(timer_settings,width=8)
        clock_out_Entry.grid(row=3,column=1)

        #Break In
        break_in = Label(timer_settings,text="Break In :",padx=5,pady=10)
        break_in.config(bg="#2c2c2c",fg="#fff")
        break_in.grid(row=1,column=0,sticky=W)

        #Break in Entry
        Break_in_Entry = Entry(timer_settings,width=8)
        Break_in_Entry.grid(row=1,column=1)

        #Break Out
        break_out = Label(timer_settings,text="Break Out :",padx=5,pady=10)
        break_out.config(bg="#2c2c2c",fg="#fff")
        break_out.grid(row=2,column=0,sticky=W)

        #break out entry
        break_out_entry = Entry(timer_settings,width=8)
        break_out_entry.grid(row=2,column=1,sticky=W)

        #Frame buttons
        frameBtn = Frame(self.frameTime,width=280,height=50)
        frameBtn.config(bg="#2c2c2c")
        frameBtn.grid(row=2,column=0,columnspan=4,pady=10)

        #Buttons
        #Edit Button
        edit_btn = Button(frameBtn,text="Edit",padx=20,pady=10)
        edit_btn.config(bg="#ffff00",fg="#000")
        edit_btn.grid(row=0,column=0,columnspan=2,padx=8)

        # #Save Button
        save_btn = Button(frameBtn,text="Save",padx=20,pady=10)
        save_btn.config(bg="#83c333",fg="#fff")
        save_btn.grid(row=0,column=2,columnspan=2,padx=8)
    
    def save_data_time(self):
        pass
    #Time-Clock-Counter
    def digitalClock(self):
        today_text = time.strftime("%H:%M:%S")
        today_hour = int(time.strftime("%H"))
        today_minute = int(time.strftime("%M"))
        today_second = int(time.strftime("%S"))

        if(today_hour == 14 and today_minute == 0 and today_second == 0):
            self.tld_clockIn.startConnection()
            self.start_digital_counter()
        if(today_hour == 19 and today_minute == 30 and today_second == 0):
            self.tld_breakIn.startConnection()
            self.stop_digital_counter()
        if(today_hour == 20 and today_minute == 00 and today_second == 0):
            self.tld_breakOut.startConnection()
            self.start_digital_counter()
        if(today_hour == 22 and today_minute == 30 and today_second == 0):
            self.tld_clockOut.startConnection()
            self.stop_digital_counter()
   
        #Labels
        self.showHour.config(text=today_text,bg="#2c2c2c",fg="#fff")
        self.showHour.grid(row=2,column=1,padx=2,pady=4,sticky=W)
        self.showHour.after(1000, self.digitalClock)    

    def digital_counter(self):
        #Add 1
        if(self.running):
            self.second += 1
            if(self.second == 60):
                self.minute += 1
                self.second = 0
                if(self.minute >= 59):
                    self.hour += 1
                    self.minute = 0
                    if(self.hour >= 8):
                        current_time = f"{self.hour} : {self.minute} : {self.second}"
                        self.counter.config(text=current_time,bg="#83c333",fg="#ff0000")
        
        current_time = f"{self.hour} : {self.minute} : {self.second}"
        self.counter.config(text=current_time,bg="#83c333",fg="#fff")     
        
        self.counter.after(1000,self.digital_counter)
    
    def start_digital_counter(self):
        self.running = True
        return

    def stop_digital_counter(self):
        self.running = False
        return

    def hello(self):
        print(self.running)

if __name__ == "__main__":
    window = Tk()
    app = TLDClock(window)
    window.mainloop()