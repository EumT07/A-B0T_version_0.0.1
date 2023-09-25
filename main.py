from tkinter import *
from tkinter import ttk, messagebox as errorMessage
from datetime import datetime
import pickle
import time
import os
import requests
from modules.tld import *
from modules.test import *
import webbrowser
from dotenv import load_dotenv

load_dotenv()

class TLDClock():
    #Timer
    hour = 0
    minute = 0
    second = 0
    running = False
    tld_clockIn = None
    tld_clockOut = None
    tld_breakIn = None
    tld_breakOut = None
    tld_test = None
    #Records
    clockIn_message = "No records Yet"
    breakIn_message = "No records Yet"
    breakOut_message = "No records Yet"
    clockOut_message = "No records Yet"
    data_records = []
    #Active message
    active_clockIn_message = False
    active_breakIn_message = False
    active_breakOut_message = False
    active_clockOut_message = False


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
        self.frameabout = Frame(self.window,bg="#2c2c2c",width=440,height=400)

        #Img
        self.logo = PhotoImage(file="./img/logo.PNG")
        #Container Time inside frame2
        self.container = LabelFrame(self.frame2, text="Time",padx=5,pady=5)

        #User Icon
        self.user_icon = PhotoImage(file="./img/userIcon.PNG")

        #current_hour
        current_hour = Label(self.container,text="Current Hour :")
        current_hour.config(bg="#2c2c2c",fg="#fff")
        current_hour.grid(row=2,column=0,padx=5,pady=2,sticky=W)
        self.showHour = Label(self.container)

        #Counter Time
        # self.counter = Label(self.frame2,font="12",padx=18,pady=10)
        # current_time = f"{self.hour} : {self.minute} : {self.second}"
        # self.counter.config(text=current_time,fg="#000")
        
        self.frame_Principal()
        
    # Frames
    #Delete frame 1: principal
    def clear_widgets(self,frame):
        try:
            #destroy first frame
            frame.destroy()
        except Exception as e:
            print(type(e).__name__)

    def hide_menu_frames(self):
        try:
            self.frame2.pack_forget()
            self.frameUser.pack_forget()
            self.frameTime.pack_forget()
            self.frameabout.pack_forget()
        except Exception as e:
            print(type(e).__name__)

    def menu(self):
        try:
            menuBar = Menu(self.window)
            self.window.config(menu=menuBar)

            #Menu options
            menuBar.add_command(label="Clock",command=self.frame_Sencond)

            #Settings - options
            settings = Menu(menuBar,tearoff=0)
            menuBar.add_cascade(label="Settings",menu=settings)
            
            #1 User
            settings.add_command(label="User",command=self.frame_user)
            #2  Time
            settings.add_command(label="Time",command=self.frame_time)
            #Help - Options
            help = Menu(menuBar,tearoff=0)
            menuBar.add_cascade(label="Help",menu=help)
            #1 manual
            help.add_command(label="view",state="disabled")
            help.add_command(label="Send feedback",state="disabled")
            help.add_separator()
            help.add_command(label="About..",command=self.about_bot)

        except Exception as e:
            print(type(e).__name__)
    
    def check_internet_connection(self):
        try:
            requests.get("https://www.google.com", timeout=3)
            return True
        except Exception as e:
            return False
    #Frame 1
    def frame_Principal(self):
        try:
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
        
            internet_Connection = self.check_internet_connection()
            
            if(internet_Connection):
                #Button
                lets_go_button = Button(self.frame1,text="Let's go",command=self.frame_Sencond,width=10,height=20)
                lets_go_button.config(bg="#83c333",fg="#fff")
                lets_go_button.pack(side="bottom",pady=60)
            else:
                errorMessage.showinfo("Internet Connection","Check your internet Connection and try again")

        except Exception as e:
            print(type(e).__name__)
    #Frame 2
    def frame_Sencond(self):
        try:
            self.clear_widgets(self.frame1)
            self.hide_menu_frames()
            self.menu()
        
            #Getting user
            user = self.load_user_info()
            clockData = self.load_clock_data()
            text_bot_message = ""
        
        
            if(not(user == None) and not(clockData == None)):
                email = user["email"]
                password = user["password"]
                #Clock - Bamboohr
                self.tld_clockIn = Clock_In(email,password)
                self.tld_clockOut = Clock_Out(email,password)
                self.tld_breakIn = Break_In(email,password)
                self.tld_breakOut = Break_Out(email,password)
                self.digitalClock()
                # self.digital_counter()
                text_bot_message = "Bot is running"
            else:
                text_bot_message = "¡¡¡ Set your email/pass\nand time clock !!!"
                pass
            
  
            #Date

            #Second frame
            self.frame2.pack(fill="both",expand=1)

            #Date Container
            self.container.config(bg="#2c2c2c",fg="#fff")
            self.container.grid(row=0,column=1,columnspan=1,padx=30,pady=10,sticky=N+S)
        
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

            #Records
            record = Label(self.frame2, text="Records",padx=5,pady=10)
            record.config(bg="#2c2c2c",fg="#ffff00")
            record.grid(row=1,column=1,columnspan=1,padx=45,pady=10,sticky=N+S)
    

            #Clock in 
            record_clockIn = Label(self.frame2, text="Clock In :")
            record_clockIn.config(bg="#2c2c2c",fg="#83c333")
            record_clockIn.grid(row=2,column=0,padx=10,pady=8,sticky=W)
            #text
            # text=self.clockIn_message
            record_text_clockIn = Label(self.frame2,text=self.clockIn_message)

            if(self.active_clockIn_message):
                record_text_clockIn.config(bg="#2c2c2c",fg="#ffff00",padx=30)
            else:
                record_text_clockIn.config(bg="#2c2c2c",fg="#ff0000",padx=30)
            record_text_clockIn.grid(row=2,column=1)

            #Break in 
            record_breakIn = Label(self.frame2, text="Break In :")
            record_breakIn.config(bg="#2c2c2c",fg="#83c333")
            record_breakIn.grid(row=3,column=0,padx=10,pady=8,sticky=W)
            #text
            record_text_breakIn = Label(self.frame2,text=self.breakIn_message)

            if(self.active_breakIn_message):
                record_text_breakIn.config(bg="#2c2c2c",fg="#ffff00",padx=30)
            else:
                record_text_breakIn.config(bg="#2c2c2c",fg="#ff0000",padx=30)
            record_text_breakIn.grid(row=3,column=1)

            #Break out 
            record_breakOut = Label(self.frame2, text="Break Out :")
            record_breakOut.config(bg="#2c2c2c",fg="#83c333")
            record_breakOut.grid(row=4,column=0,padx=10,pady=8,sticky=W)
            #text
            record_text_breakOut = Label(self.frame2,text=self.breakOut_message)
            if(self.active_breakOut_message):
                record_text_breakOut.config(bg="#2c2c2c",fg="#ffff00",padx=30)
            else:
                record_text_breakOut.config(bg="#2c2c2c",fg="#ff0000",padx=30)
            record_text_breakOut.grid(row=4,column=1)

            #Clock Our 
            record_clockOut = Label(self.frame2, text="Clock Out :")
            record_clockOut.config(bg="#2c2c2c",fg="#83c333")
            record_clockOut.grid(row=5,column=0,padx=10,pady=8,sticky=W)
            #text
            record_text_clockOut = Label(self.frame2,text=self.clockOut_message)
            if(self.active_clockOut_message):
                record_text_clockOut.config(bg="#2c2c2c",fg="#ffff00",padx=30)
            else: 
                record_text_clockOut.config(bg="#2c2c2c",fg="#ff0000",padx=30)
            record_text_clockOut.grid(row=5,column=1)

            #Bot message
            bot_message = Label(self.frame2, text=text_bot_message,padx=5,pady=10)
            bot_message.config(bg="#2c2c2c",fg="#ffff00")
            bot_message.grid(row=6,column=1,columnspan=1,padx=45,pady=10,sticky=N+S)

        except Exception as e:
            print(type(e).__name__)
    
 
    #Settings : user
    def frame_user(self):
        try:
            self.hide_menu_frames()
            self.frameUser.pack(fill="both",expand=1)

            #Getting user
            user = self.load_user_info()

            #Image logo
            image = Label(self.frameUser,image=self.user_icon)
            image.config(bg="#2c2c2c")
            image.grid(row=0,column=0,columnspan=4,padx=100,pady=20,sticky=N+S)

            #Framer user
            userInfo = LabelFrame(self.frameUser,text="User Info",padx=5,pady=5)
            userInfo.config(bg="#2c2c2c",fg="#fff")
            userInfo.grid(row=1,column=0,columnspan=4,padx=100,pady=30,sticky=N)
        
            # Lables
            #Email
            email_Label= Label(userInfo,text="Email :",padx=5,pady=10)
            email_Label.config(bg="#2c2c2c",fg="#fff")
            email_Label.grid(row=0,column=0,sticky=W)
            #Password
            password_Label = Label(userInfo,text="Password :",padx=5,pady=10)
            password_Label.config(bg="#2c2c2c",fg="#fff")
            password_Label.grid(row=1,column=0,sticky=W)

            #Frame buttons
            frameBtn = Frame(self.frameUser, width=450, height=40)
            frameBtn.config(bg="#2c2c2c")
            frameBtn.grid(row=2,column=0,columnspan=6,pady=20)


            #Buttons
            #Save Button
            save_btn = Button(frameBtn,text="Save",command=lambda:self.save_user(email.get(),password.get()))
            save_btn.config(bg="#83c333",fg="#fff",padx=20,pady=10)
            save_btn.grid(row=0,column=0,columnspan=2,padx=8) 

            #Edit Button
            clean_btn = Button(frameBtn,text="Clean",command=self.clean_user_info)
            clean_btn.config(bg="#7f7f7f",fg="#fff",padx=20,pady=10,state="disabled")
            clean_btn.grid(row=0,column=2,columnspan=2,padx=8)

            #Test Button
            test_btn = Button(frameBtn,text="Test",command=lambda:self.test_user(email.get(),password.get()))
            test_btn.config(bg="#7f7f7f",fg="#fff",padx=20,pady=10,state="disabled")
            test_btn.grid(row=0,column=5,columnspan=2,padx=8)

            #Entries
            if(user):
                #Email Entry
                email = Entry(userInfo,width=25,textvariable=StringVar(userInfo,user["email"]),state="disable")
                email.grid(row=0,column=1)
                #Password Entry
                password = Entry(userInfo,width=25,textvariable=StringVar(userInfo,user["password"]),state="disable")
                password.config(justify="left",show="*")
                password.grid(row=1,column=1)
                #Button
                save_btn.config(bg="#7f7f7f",state="disabled")
                test_btn.config(bg="#0000ff",fg="#fff",state="normal")
                clean_btn.config(bg="#ffff00",fg="#000",state="normal")

            else:
                #Email Entry
                email = Entry(userInfo,width=25)
                email.grid(row=0,column=1)
                #Password Entry
                password = Entry(userInfo,width=25)
                password.config(justify="left",show="*")
                password.grid(row=1,column=1)
        except Exception as e:
            print(type(e).__name__)    
                    
    def save_user(self,email,password):
        try:
            user = {"email":email,"password":password,"active": True}
            if(user["email"] and user["password"]):
                #Save data
                self.active = True
                #Creat Pickle Documet
                userData = open("./db/userinfo.pckl","wb")
                pickle.dump(user,userData)
                self.frame2.pack_forget()
                time.sleep(1)
                self.restart()
            else:
                errorMessage.showerror("Error", "Fields are Empties")
        except Exception as e:
            print(type(e).__name__)        
 
    def load_user_info(self):
        try:
            user = None
            userdata = open("./db/userinfo.pckl","rb")
            if(userdata):
                user = pickle.load(userdata)
                return user
            else:
                return user
        except FileNotFoundError:
            pass
        except Exception as e:
            print(type(e).__name__)

    def clean_user_info(self):
        #Delete file
        try:
            result = errorMessage.askquestion("Clean","Do you want to clean all fields?")

            if(result):
                os.remove("./db/userinfo.pckl")
                time.sleep(1)
                self.frame_user()
            else:
                time.sleep(1)
                self.frame_user()
        except Exception as e:
            print(type(e).__name__)

    def test_user(self,email,password):
        try:
            user = self.load_user_info()

            if(not(user == None)):
                email = user["email"]
                password = user["password"]
                self.tld_test = Test(email,password)
                self.tld_test.startConnection()
                #Check if there is an error: Login 
                loginError = self.tld_test.loginError
                if(not(loginError == None)):
                    errorMessage.showerror("Account",loginError)
                #success login message
                errorMessage.showinfo("Success","Your email and password are correct")
                time.sleep(2)
                self.frame_user()
        except Exception as e:
            print(type(e).__name__)
        
        
    #Settings : time  
    def frame_time(self):
        try:
            self.hide_menu_frames()
            self.frameTime.pack(fill="both",expand=1)

            clock_Data = self.load_clock_data()

            #Info Label
            info_text =Label(self.frameTime,text="Set your time, example: 14:00:00 (2pm) \n < hour:minute:second >\n in Military time format")
            info_text.config(bg="#2c2c2c",fg="#ffff00")
            info_text.grid(row=0,column=0,columnspan=4,pady=20)

            #Framer Time
            timer_settings = LabelFrame(self.frameTime,text="Timer",padx=5,pady=5)
            timer_settings.config(bg="#2c2c2c",fg="#fff")
            timer_settings.grid(row=1,column=0,columnspan=4,padx=150,pady=10,sticky=N)

            #Clock in
            clock_in_Label = Label(timer_settings,text="Clock In :",padx=5,pady=10)
            clock_in_Label.config(bg="#2c2c2c",fg="#fff")
            clock_in_Label.grid(row=0,column=0,sticky=W)
            #Clock Out
            clock_out_Label = Label(timer_settings,text="Clock Out :",padx=5,pady=10)
            clock_out_Label.config(bg="#2c2c2c",fg="#fff")
            clock_out_Label.grid(row=3,column=0,sticky=W)
            #Break In
            break_in_Label = Label(timer_settings,text="Break In :",padx=5,pady=10)
            break_in_Label.config(bg="#2c2c2c",fg="#fff")
            break_in_Label.grid(row=1,column=0,sticky=W)
            #Break Out
            break_out_Label = Label(timer_settings,text="Break Out :",padx=5,pady=10)
            break_out_Label.config(bg="#2c2c2c",fg="#fff")
            break_out_Label.grid(row=2,column=0,sticky=W)

            #Frame buttons
            frameBtn = Frame(self.frameTime,width=280,height=50)
            frameBtn.config(bg="#2c2c2c")
            frameBtn.grid(row=2,column=0,columnspan=4,pady=10)

            #Buttons
            #Save Button
            save_btn = Button(frameBtn,text="Save",padx=20,pady=10)
            save_btn.grid(row=0,column=0,columnspan=2,padx=8)

            # Clean Button
            clean_btn = Button(frameBtn,text="Clean",padx=20,pady=10,command=self.clean_clock_data)
            clean_btn.grid(row=0,column=2,columnspan=2,padx=8)

            if(clock_Data):
                #Clock_in Entry
                clockIn_time = f"{clock_Data[0]['hour']}:{clock_Data[0]['minutes']}:{clock_Data[0]['seconds']}"
                clock_in = Entry(timer_settings,width=8,textvariable=StringVar(timer_settings,clockIn_time),state="disabled")
                clock_in.grid(row=0,column=1)

                #Break in Entry
                breakIn_time = f"{clock_Data[1]['hour']}:{clock_Data[1]['minutes']}:{clock_Data[1]['seconds']}"
            
                break_in = Entry(timer_settings,width=8,textvariable=StringVar(timer_settings,breakIn_time),state="disabled")
                break_in.grid(row=1,column=1)

                #break out entry
                breakOut_time = f"{clock_Data[2]['hour']}:{clock_Data[2]['minutes']}:{clock_Data[2]['seconds']}"
                break_out = Entry(timer_settings,width=8,textvariable=StringVar(timer_settings,breakOut_time),state="disabled")
                break_out.grid(row=2,column=1,sticky=W)

                #Clock_Out Entry
                clockOut_time = f"{clock_Data[3]['hour']}:{clock_Data[3]['minutes']}:{clock_Data[3]['seconds']}"
                clock_out = Entry(timer_settings,width=8,textvariable=StringVar(timer_settings,clockOut_time),state="disabled")
                clock_out.grid(row=3,column=1)

                #Buttons
                save_btn.config(bg="#7f7f7f",fg="#fff",state="disabled")
                clean_btn.config(bg="#ffff00",fg="#000",state="normal")

            else:
                #Clock_in Entry
                clock_in = Entry(timer_settings,width=8)
                clock_in.grid(row=0,column=1)

                #Clock_Out Entry
                clock_out = Entry(timer_settings,width=8)
                clock_out.grid(row=3,column=1)

                #Break in Entry
                break_in = Entry(timer_settings,width=8)
                break_in.grid(row=1,column=1)

                #break out entry
                break_out = Entry(timer_settings,width=8)
                break_out.grid(row=2,column=1,sticky=W)

                #Buttons
                save_btn.config(bg="#83c333",fg="#fff",command=lambda:self.save_clock_data(clock_in.get(),break_in.get(),break_out.get(),clock_out.get()))
                clean_btn.config(bg="#7f7f7f",fg="#fff",state="disabled")
        except Exception as e:
            print(type(e).__name__)
        
    def save_clock_data(self,clock_in,break_in,break_out,clock_out):
        try:

            if(not(clock_in == "" or len(clock_in) < 8) and 
            not(break_in == "" or len(clock_in) < 8) and 
            not(break_out == "" or len(clock_in) < 8) and 
            not(clock_out == "" or len(clock_in) < 8)):
                #Clock_in - Split get Hour minute second
                clock_in_hour,clock_in_minute,clock_in_seconds = clock_in.split(":")
                #Break_in - Split get Hour minute second
                break_in_hour,break_in_minute,break_in_seconds = break_in.split(":")
                #Break_out - Split get Hour minute second
                break_out_hour,break_out_minute,break_out_seconds = break_out.split(":")
                #Clock_out - Split get Hour minute second
                clock_out_hour,clock_out_minute,clock_out_seconds = clock_out.split(":")
        

                #Clock_in -> Dictionaries
                clockIn = {"hour":int(clock_in_hour),"minutes":int(clock_in_minute),"seconds":int(clock_in_seconds)}
                #break_in -> Dictionaries
                breakIn = {"hour":int(break_in_hour),"minutes":int(break_in_minute),"seconds":int(break_in_seconds)}
                #break_out -> Dictionaries
                breakOut = {"hour":int(break_out_hour),"minutes":int(break_out_minute),"seconds":int(break_out_seconds)}
                #Clock_in -> Dictionaries
                clockOut = {"hour":int(clock_out_hour),"minutes":int(clock_out_minute),"seconds":int(clock_out_seconds)}


                #Data Time
                clock_Data = [clockIn,breakIn,breakOut,clockOut]
            
                #Creat Pickle Documet
                userData = open("./db/clockinfo.pckl","wb")
                pickle.dump(clock_Data,userData)
                self.frame2.pack_forget()
                time.sleep(1)
                self.restart()

            else:
                errorMessage.showerror("Error", "Fields are Empties or Wrong format")
                pass
        except Exception as e:
            print(type(e).__name__)
    
    def load_clock_data(self):
        try:
            clock_Data = None
            userdata = open("./db/clockinfo.pckl","rb")
            if(userdata):
                clock_Data = pickle.load(userdata)
                return clock_Data
            else:
                return clock_Data
        except FileNotFoundError:
            pass
        except Exception as e:
            print(type(e).__name__)

    def clean_clock_data(self):
        #Delete file
        try:
            result = errorMessage.askquestion("Clean","Do you want to clean all fields?")

            if(result):
                os.remove("./db/clockinfo.pckl")
                time.sleep(1)
                self.frame_time()
            else:
                time.sleep(1)
                self.frame_time()
        except Exception as e:
            print(type(e).__name__)
    
    
    #Time-Clock-Counter
    def digitalClock(self):
        try:
            today_text = time.strftime("%H:%M:%S")
            
            #Get Hours data
            clockData = self.load_clock_data()

            if(not(clockData == None)):
                self.check_time()
            
            #Labels
            self.showHour.config(text=today_text,bg="#2c2c2c",fg="#fff")
            self.showHour.grid(row=2,column=1,padx=2,pady=4,sticky=W)
            self.showHour.after(1000, self.digitalClock)
        except:
            print("Hour Error")
            pass  
    
    """There is a little bit issue with the code, I'm getting an issue with the counter, when I save user or hours time data, and the bot starts to do its task the counter starts to add x2 the counter number, I don't know if there is a problem with the loops. I'll leave the code while I try to resolve it and be able to add a counter to the app."""
    
    def digital_counter(self):
        try:
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
                            #Counter
                            current_time = f"{self.hour} : {self.minute} : {self.second}"
                            self.counter.config(text=current_time,bg="#83c333",fg="#ff0000")
                            self.counter.grid(row=1,column=0,columnspan=4,padx=100,pady=40)
        
            current_time = f"{self.hour} : {self.minute} : {self.second}"
            self.counter.config(text=current_time,bg="#83c333",fg="#fff") 
            self.counter.grid(row=1,column=0,columnspan=4,padx=100,pady=40)    
        
            self.counter.after(1000,self.digital_counter)
        except Exception as e:
            print(type(e).__name__)

    def reset_counter(self):
        try:
            self.hour = 0
            self.minute = 0
            self.second = 0
            return
        except Exception as e:
            print(type(e).__name__)

    def start_digital_counter(self):
        try:
            # self.running = True
            today_text = time.strftime("%H:%M:%S")
            print(f"Bamboohr Bot start at: {today_text} ")
            return
        except Exception as e:
            print(type(e).__name__)

    def stop_digital_counter(self):
        try:
            # self.running = False
            today_text = time.strftime("%H:%M:%S")
            print(f"Bamboohr Bot Stop at: {today_text} ")
            return
        except Exception as e:
            print(type(e).__name__)
    """ - - - - """
    #Records
    def save_records(self,records):
        self.data_records.append(records)
        print(self.data_records)
        pass

    def check_time(self):
        try:
            today_hour = int(time.strftime("%H"))
            today_minute = int(time.strftime("%M"))
            today_second = int(time.strftime("%S"))
        
            clock_in = None
            break_in = None
            break_out = None
            clock_out = None

            #Get Hours data
            clockData = self.load_clock_data()

            if(clockData):
                clock_in = clockData[0]
                break_in = clockData[1]
                break_out = clockData[2]
                clock_out = clockData[3]
             
            if(today_hour == clock_in["hour"] and 
            today_minute == clock_in["minutes"] and 
            today_second == clock_in["seconds"]):
                # self.tld_clockIn.startConnection()
                self.clockIn_message = self.tld_clockIn.clockTime()
                self.active_clockIn_message = True
                self.save_records(self.clockIn_message)
                time.sleep(1)
                self.frame_Sencond()     
            
            if(today_hour == break_in["hour"] and 
           today_minute == break_in["minutes"] and 
           today_second == break_in["seconds"]):
                # self.tld_breakIn.startConnection()
                self.breakIn_message = self.tld_breakIn.clockTime()
                self.active_breakIn_message = True
                self.save_records(self.breakIn_message)
                time.sleep(1)
                self.frame_Sencond()

            if(today_hour == break_out["hour"] and 
            today_minute == break_out["minutes"] and 
            today_second == break_out["seconds"]):
                # self.tld_breakOut.startConnection()
                self.breakOut_message = self.tld_breakOut.clockTime()
                self.active_breakOut_message = True
                self.save_records(self.breakOut_message)
                time.sleep(1)
                self.frame_Sencond()
             
            if(today_hour == clock_out["hour"] and 
           today_minute == clock_out["minutes"] and 
           today_second == clock_out["seconds"]):
                # self.tld_clockOut.startConnection()
                self.clockOut_message = self.tld_clockOut.clockTime()
                self.active_clockOut_message = True
                self.save_records(self.clockOut_message)
                time.sleep(1)
                self.frame_Sencond()
        except Exception as e:
            print(type(e).__name__)

    #Help Frame
    def manual(self):
        pass
    def send_feedback(self):
        pass
       
    def about_bot(self):
        try:
            self.hide_menu_frames()
            #Principal Frame
            self.frameabout.pack(fill="both",expand=1)
        
            #Image logo
            image = Label(self.frameabout,image=self.logo)
            image.config(bg="#2c2c2c")
            image.pack(side="top",pady=30)

            #Label
            text_Content = "Bamboo bot Clock\nVersion 0.0.1\n\nBambooHr Bot is an automated bot helping us\nto control the 'clock in' and 'clock out'\nwithin a time range set by the user\nthe bot is built with python 3.11.5\n\n© bamboohr bot clock 2023. All rights reserved"
            welcome = Label(self.frameabout, text=text_Content)
            welcome.config(bg="#2c2c2c",fg="#fff")
            welcome.pack(pady=5)

            link = Label(self.frameabout,text="\nGithub code")
            link.config(bg="#2c2c2c", fg="#1e90ff", cursor="hand2")
            link.pack()
            link.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/EumT07"))
        except:
            pass
        
    #Restart APP          
    def restart(self):
        try:
            self.window.destroy()
            os.startfile("main.py")
        except Exception as e:
            print(type(e).__name__)
        

if __name__ == "__main__":
    window = Tk()
    app = TLDClock(window)
    window.mainloop()