from tkinter import *
from tkinter import ttk, messagebox as errorMessage
from datetime import datetime
import sqlite3
import time
import os, sys
import requests
from modules.tld import *
from modules.test import *
import webbrowser
from win10toast import ToastNotifier
from dotenv import load_dotenv
#Load .env data
load_dotenv()

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")
   
    return os.path.join(base_path, relative_path)

class TLDClock():
    """SQL Propierties"""
    db_user = resource_path("db\\user.db")
    query_user = """
    CREATE TABLE user(
        email VARCHAR(100) NOT NULL,
        password VARCHAR(100) NOT NULL,
        shift VARCHAR(100) NOT NULL)"""
    db_records = resource_path("db\\records.db")
    query_records ="""
    CREATE TABLE records(
        record_name VARCHAR(100),
        records_value VARCHAR(100))"""
    db_clockTime = resource_path("db\\time.db")
    query_clockTime ="""
    CREATE TABLE timeClock(
        time_clockIn VARCHAR(100) NOT NULL,
        time_breakIn VARCHAR(100) NOT NULL,
        time_breakOut VARCHAR(100) NOT NULL,
        time_clockOut VARCHAR(100) NOT NULL)"""
    #Import Classes
    tld_clockIn = None
    tld_clockOut = None
    tld_breakIn = None
    tld_breakOut = None
    tld_test = None
    #Records Messages
    clockIn_message = None
    breakIn_message = None
    breakOut_message = None
    clockOut_message = None
    data_records = []
    #Active message
    active_clockIn_message = False
    active_breakIn_message = False
    active_breakOut_message = False
    active_clockOut_message = False
    #Frames
    frameUser = None
    frameTime = None
    frame2 = None
    showHour = None
    

    def __init__(self,window):
        """Starting the app"""
        #window App settings
        self.window = window
        self.window.title("A-B0T")
        self.window.iconbitmap(resource_path("img\\icon.ico"))
        self.window.eval("tk::PlaceWindow . center")
        self.window.resizable(0,0)
        self.window.geometry("440x400")

        #Frames
        self.frame1 = Frame(self.window,bg="#2c2c2c",width=440,height=400)
        self.frame2 = Frame(self.window,bg="#2c2c2c",width=440,height=400)
        self.frameabout = Frame(self.window,bg="#2c2c2c",width=440,height=400)
        
        
        #Img
        self.logo = PhotoImage(file=resource_path("img\\logo.PNG"))
        #User Icon
        self.user_icon = PhotoImage(file=resource_path("img\\userIcon.PNG"))

        #Show first intro
        self.loading_app()
        #Creating Data Base Tables
        self.create_DataBase(self.db_user,self.query_user)
        self.create_DataBase(self.db_records,self.query_records)
        self.create_DataBase(self.db_clockTime,self.query_clockTime)

    #Internet
    def check_internet_connection(self):
        """Check Internet connection"""
        try:
            requests.get("https://www.google.com", timeout=3)
            return True
        except Exception as e:
            return False
        
    #Data Base sqlite3
    def create_DataBase(self,dbName,query):
        """Create Tables"""
        with sqlite3.connect(dbName) as connection:
            cursor = connection.cursor()
            try:
                cursor.execute(query)
            except sqlite3.OperationalError:
                print(F"DB ok")
                pass
    #Runs commds Data base
    def run_dataBase(self,dbName,query,parameters = ()):
        """Run all querys sqlite3"""
        with sqlite3.connect(dbName) as connection:
            cursor = connection.cursor()
            result = cursor.execute(query,parameters)
            connection.commit()
        return result
    # Frames
    #Delete frame 1: principal
    def clear_widgets(self,frame):
        try:
            #destroy first frame
            frame.destroy()
        except Exception as e:
            print(f"Error: {type(e).__name__} -> clear_widgets ")
            pass

    def hide_frames(self):
        try:
            self.frame2.pack_forget()
            self.frameabout.pack_forget()
            if(not(self.frameUser == None)):
                self.frameUser.pack_forget()
            if(not(self.frameTime == None)):
                self.frameTime.pack_forget()
        except AttributeError:
            print("Error hide_frames atributos")
            pass
        except Exception as e:
            print(f"Error: {type(e).__name__} -> hide_menu_frames ")
            pass
    
    #Menu
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
            #3 Languages
            # settings.add_command(label="Language",state="disabled")
            lang = Menu(settings, tearoff=0)
            settings.add_cascade(label="Languages", menu=lang)
            lang.add_cascade(label="Spanish",state="disabled")
            lang.add_cascade(label="English",state="disabled")
            lang.add_cascade(label="Portuguese",state="disabled")
            lang.add_cascade(label="French",state="disabled")
            lang.add_cascade(label="Italian",state="disabled")
            #4 Help - Options
            help = Menu(menuBar,tearoff=0)
            menuBar.add_cascade(label="Help",menu=help)
            #help: 1 manual
            help.add_command(label="More info",state="disabled")
            #help: 2 contact
            help.add_command(label="Send feedback",state="disabled")
            #help: 3 Notificacions
            notifications = Menu(help,tearoff=0)
            help.add_cascade(label="Notifications",menu=notifications)
            notifications.add_cascade(label="On",state="disabled")
            notifications.add_cascade(label="Off",state="disabled")
            #help: 4 System
            system = Menu(help,tearoff=0)
            help.add_cascade(label="System",menu=system)
            system.add_cascade(label="Reboot",command=self.reboot)
            system.add_cascade(label="Factory Restore",command=self.factory_restore)
            #Separator
            help.add_separator()
            #help: 5 About -> A-B0T
            help.add_command(label="About..",command=self.about_bot)
            
        except Exception as e:
            print(f"Error: {type(e).__name__} -> menu")
            pass
    
    #Frame 1
    def frame_Principal(self):
        try:
            #Principal Frame
            self.frame1.pack(fill="both",expand=1)
            #Image logo
            image = Label(self.frame1,image=self.logo)
            image.config(bg="#2c2c2c")
            image.pack(side="top",pady=20)
   
            #Label
            text_Content = "A-B0T\n\nWelcome to A-B0T (Automatic Bot)\n it helps you to control your clock in and clock out\n< May the Force Be with You >"
            welcome = Label(
                self.frame1,
                text=text_Content,
                font=("Adobe Garamond Pro",10,"bold"))
            welcome.config(bg="#2c2c2c",fg="#fff")
            welcome.pack(pady=10)
        
            internet_Connection = self.check_internet_connection()
            
            if(internet_Connection):
                #Button
                lets_go_button = Button(
                    self.frame1,text="Let's go",
                    command=self.frame_Sencond,
                    width=10,
                    height=20)
                lets_go_button.config(
                    bg="#83c333",
                    fg="#fff",font=("Adobe Garamond Pro",8,"bold"))
                lets_go_button.pack(side="bottom",pady=40)
            else:
                errorMessage.showinfo("Internet Connection","Check your internet Connection and try again")
            
            self.check_records()

        except Exception as e:
            print(f"Error: {type(e).__name__} -> frame_Principal")
            pass
    
    #Frame 2
    def frame_Sencond(self):
        try:
            self.clear_widgets(self.frame1)
            self.hide_frames()
            self.menu()
            self.show_records()
            
            #Getting user info
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
                text_bot_message = "Bot is running"
            else:
                text_bot_message = "¡¡¡ Bot off !!!"
                pass
            
            #Date

            #Second frame
            self.frame2.pack(fill="both",expand=1)

            #Date Container
            #Container Time inside frame2
            container = LabelFrame(self.frame2, text="Time",padx=5,pady=5)
            container.config(bg="#2c2c2c",fg="#fff")
            container.grid(
                row=0,
                column=1,
                columnspan=1,
                padx=25,
                pady=10,
                sticky=N+S)
            
            #current_hour
            current_hour = Label(container,text="Current Hour :")
            current_hour.config(bg="#2c2c2c",fg="#fff")
            current_hour.grid(row=2,column=0,padx=5,pady=2,sticky=W)
            self.showHour = Label(container)
        
            #Date
            today = datetime.now()
            date_time = today.strftime("%d %B %Y")
            day_name = today.strftime("%A")

            #Date LAbel
            date = Label(container,text="Date : ")
            date.config(bg="#2c2c2c",fg="#fff")
            date.grid(row=0,column=0,padx=5,pady=2,sticky=W)

            date_text = Label(container,text=date_time)
            date_text.config(bg="#2c2c2c",fg="#fff")
            date_text.grid(row=0,column=1,padx=2,pady=2,sticky=W)

            #Day Label
            day = Label(container,text="Day : ",bg="#2c2c2c")
            day.config(bg="#2c2c2c",fg="#fff")
            day.grid(row=1,column=0,padx=5,pady=2,sticky=W)

            day_text = Label(container,text=day_name)
            day_text.config(bg="#2c2c2c",fg="#fff")
            day_text.grid(row=1,column=1,padx=2,pady=4,sticky=W)

            #Records
            record = Label(self.frame2, text="Records",padx=5,pady=10)
            record.config(
                bg="#2c2c2c",
                fg="#fff",
                font=("Adobe Garamond Pro",10,"bold"))
            record.grid(
                row=1,
                column=1,
                columnspan=1,
                padx=40,
                pady=8,
                sticky=N+S)
    

            #Clock in 
            record_clockIn = Label(self.frame2, text="Clock In :")
            record_clockIn.config(
                bg="#2c2c2c",
                fg="#fff",
                font=("Adobe Garamond Pro",10,"bold"))
            record_clockIn.grid(row=2,column=0,padx=8,pady=8,sticky=W)
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
            record_breakIn.config(
                bg="#2c2c2c",
                fg="#fff",
                font=("Adobe Garamond Pro",10,"bold"))
            record_breakIn.grid(row=3,column=0,padx=8,pady=8,sticky=W)
            #text
            record_text_breakIn = Label(self.frame2,text=self.breakIn_message)

            if(self.active_breakIn_message):
                record_text_breakIn.config(bg="#2c2c2c",fg="#ffff00",padx=30)
            else:
                record_text_breakIn.config(bg="#2c2c2c",fg="#ff0000",padx=30)
            record_text_breakIn.grid(row=3,column=1)

            #Break out 
            record_breakOut = Label(self.frame2, text="Break Out :")
            record_breakOut.config(
                bg="#2c2c2c",
                fg="#fff",
                font=("Adobe Garamond Pro",10,"bold"))
            record_breakOut.grid(row=4,column=0,padx=8,pady=8,sticky=W)
            #text
            record_text_breakOut = Label(self.frame2,text=self.breakOut_message)
            if(self.active_breakOut_message):
                record_text_breakOut.config(bg="#2c2c2c",fg="#ffff00",padx=30)
            else:
                record_text_breakOut.config(bg="#2c2c2c",fg="#ff0000",padx=30)
            record_text_breakOut.grid(row=4,column=1)

            #Clock Our 
            record_clockOut = Label(self.frame2, text="Clock Out :")
            record_clockOut.config(
                bg="#2c2c2c",
                fg="#fff",
                font=("Adobe Garamond Pro",10,"bold"))
            record_clockOut.grid(row=5,column=0,padx=8,pady=8,sticky=W)
            #text
            record_text_clockOut = Label(self.frame2,text=self.clockOut_message)
            if(self.active_clockOut_message):
                record_text_clockOut.config(bg="#2c2c2c",fg="#ffff00",padx=30)
            else: 
                record_text_clockOut.config(bg="#2c2c2c",fg="#ff0000",padx=30)
            record_text_clockOut.grid(row=5,column=1)

            #Bot message
            bot_message = Label(self.frame2, text=text_bot_message,padx=5,pady=10)
            bot_message.config(
                bg="#2c2c2c",
                fg="#ffff00",
                font=("Adobe Garamond Pro",10,"bold"))
            bot_message.grid(row=6,column=1,columnspan=1,padx=40,pady=10,sticky=N+S)

            self.digitalClock()
             
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Error: {type(e).__name__} -> frame_Second")
            pass
    
    #Settings : user
    def frame_user(self):
        try:
            self.hide_frames()
            self.frameUser = Frame(self.window,bg="#2c2c2c",width=440,height=400) 
            self.frameUser.pack(fill="both",expand=1)

            #Getting user info
            user = self.load_user_info()

            #Image logo
            image = Label(self.frameUser,image=self.user_icon)
            image.config(bg="#2c2c2c")
            image.grid(row=0,column=0,columnspan=4,padx=100,pady=15,sticky=N+S)

            #Framer user
            userInfo = LabelFrame(self.frameUser,text="User Info",padx=5,pady=5)
            userInfo.config(bg="#2c2c2c",fg="#fff",font=("Adobe Garamond Pro",10,"bold"))
            userInfo.grid(row=1,column=0,columnspan=4,padx=100,pady=10,sticky=N)
        
            # Lables
            #Email
            email_Label= Label(userInfo,text="Email :",padx=5,pady=8)
            email_Label.config(
                bg="#2c2c2c",
                fg="#fff",
                font=("Adobe Garamond Pro",10,"bold"))
            email_Label.grid(row=0,column=0,sticky=W)
            #Password
            password_Label = Label(userInfo,text="Password :",padx=5,pady=8)
            password_Label.config(
                bg="#2c2c2c",
                fg="#fff",
                font=("Adobe Garamond Pro",10,"bold"))
            password_Label.grid(row=1,column=0,sticky=W)
            #Shift
            shift_label = Label(userInfo,text="Shift :",padx=5,pady=8)
            shift_label.config(
                bg="#2c2c2c",
                fg="#fff",
                font=("Adobe Garamond Pro",10,"bold"))
            shift_label.grid(row=2,column=0,sticky=W)
            
        
            #Frame buttons
            frameBtn = Frame(self.frameUser, width=450, height=40)
            frameBtn.config(bg="#2c2c2c")
            frameBtn.grid(row=2,column=0,columnspan=8,pady=20)

            #Buttons
            #Save Button
            save_btn = Button(frameBtn,text="Save")
            save_btn.config(bg="#83c333",fg="#fff",padx=10,pady=10)
            save_btn.grid(row=0,column=0,columnspan=2,padx=4)

            #Update Button
            update_btn = Button(frameBtn,text="Edit",command=lambda:self.update_user_info(userInfo,save_btn,update_btn,clean_btn,test_btn))
            update_btn.config(bg="#7f7f7f",fg="#fff",padx=10,pady=10,state="disabled")
            update_btn.grid(row=0,column=2,columnspan=2,padx=4)

            #Clean Button
            clean_btn = Button(frameBtn,text="Clean",command=self.clean_user_info)
            clean_btn.config(bg="#7f7f7f",fg="#fff",padx=10,pady=10,state="disabled")
            clean_btn.grid(row=0,column=4,columnspan=2,padx=4)

            #Test Button
            test_btn = Button(frameBtn,text="Test",command=lambda:self.test_user(email.get(),password.get()))
            test_btn.config(bg="#7f7f7f",fg="#fff",padx=10,pady=10,state="disabled")
            test_btn.grid(row=0,column=8,columnspan=2,padx=4)

            #Entries
            if(user):
                #Email Entry
                email = Entry(
                    userInfo,
                    width=25,
                    textvariable=StringVar(userInfo,user["email"]),state="disable")
                email.grid(row=0,column=1)
                #Password Entry
                password = Entry(
                    userInfo,
                    width=25,
                    textvariable=StringVar(userInfo,user["password"]),state="disable")
                password.config(justify="left",show="*")
                password.grid(row=1,column=1)
                #DropMenu
                shift_text = Label(userInfo,text=user["shift"])
                shift_text.config(
                    bg="#2c2c2c",
                    fg="#fff",)
                shift_text.grid(row=2,column=1)
                #Button
                save_btn.config(bg="#7f7f7f",state="disabled")
                update_btn.config(bg="#83c333",fg="#fff",state="normal")
                test_btn.config(bg="#83c333",fg="#fff",state="normal")
                clean_btn.config(bg="#83c333",fg="#fff",state="normal")
            else:
                #Email Entry
                email = Entry(userInfo,width=25)
                email.grid(row=0,column=1)
                #Password Entry
                password = Entry(userInfo,width=25)
                password.config(justify="left",show="*")
                password.grid(row=1,column=1)
                #DropMenu
                shift_value = StringVar(value="Day")
                shift_list = ["Day","Night"]
                drop_menu = OptionMenu(userInfo,shift_value,*shift_list)
                drop_menu.config(
                    bg="#2c2c2c",
                    fg="#fff",
                    activebackground="#2c2c2c",
                    activeforeground="#fff")
                drop_menu.grid(row=2,column=1)
                save_btn.config(command=lambda:self.save_user(email.get(),password.get(),shift_value.get()))
        except Exception as e:
            print(f"Error: {type(e).__name__} -> frame_user ")
            pass    
                    
    def save_user(self,email,password,shift_value):
        try:
            user = {"email":email,"password":password,"Shift": shift_value}
            print(user)
            if(user["email"] and user["password"] and user["Shift"]):
                # Insert data into user table sql3
                query = "INSERT INTO user VALUES(?,?,?)"
                parameters = (email,password,shift_value)
                self.run_dataBase(self.db_user,query,parameters)
                self.frame2.destroy()
                time.sleep(1)
                self.frame_user()
                # self.restart()
            else:
                errorMessage.showerror("Error", "Fields are Empties")
        except Exception as e:
            print(f"Error: {type(e).__name__} -> save_user")
            pass        
 
    def load_user_info(self):
        try:
            user = None
            #Reading Data from user table
            query = "SELECT email, password, shift FROM user"
            userdata = self.run_dataBase(self.db_user,query).fetchone()
            if(userdata):
                user = {"email":userdata[0],"password":userdata[1],"shift":userdata[2]}
                return user
            else:
                return user
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Error: {type(e).__name__} -> load_user_info")
            pass

    def update_user_info(self,userInfo,save_btn,update_btn,clean_btn,test_btn):
        try:
            #Getting user
            user = self.load_user_info()

            #Updating new data
            #Email
            newEmail_entry = Entry(
                userInfo,
                width=25,
                textvariable=StringVar(userInfo,user["email"]),state="normal")
            newEmail_entry.grid(row=0,column=1)

            #Password
            newPassword_entry = Entry(
                userInfo,
                width=25,
                textvariable=StringVar(userInfo,user["password"]),state="normal")
            newPassword_entry.config(justify="left",show="*")
            newPassword_entry.grid(row=1,column=1)

            #DropMenu
            new_shift_value = StringVar(value=user["shift"])
            shift_list = ["Day","Night"]
            drop_menu = OptionMenu(userInfo,new_shift_value,*shift_list)
            drop_menu.config(
                bg="#2c2c2c",
                fg="#fff",
                activebackground="#2c2c2c",
                activeforeground="#fff")
            drop_menu.grid(row=2,column=1)

            #Button
            save_btn.config(
                bg="#83c333",
                state="normal",
                command=lambda:self.save_updated_user(
                    newEmail_entry.get(),
                    newPassword_entry.get(),
                    new_shift_value.get()))
            update_btn.config(bg="#7f7f7f",fg="#fff",state="disabled")
            test_btn.config(bg="#7f7f7f",fg="#fff",state="disabled")
            clean_btn.config(bg="#7f7f7f",fg="#fff",state="disabled")
        except Exception as e:
            print(f"Error: {type(e).__name__} -> update_user_info")
            pass

    def save_updated_user(self,new_email,new_password,new_shift_value):
        try:
            #Savind new info
            user = {"email":new_email,"password":new_password,"Shift": new_shift_value}
            if(not(user["email"] == "") and not(user["password"] == "") and not(user["Shift"] == "")):
                #Run Sqlite3
                query = "UPDATE user SET email = ?, password = ?, shift = ?"
                parameters = (new_email,new_password,new_shift_value)
                self.run_dataBase(self.db_user,query,parameters)
                time.sleep(1)
                self.frame_user()
            else:
                errorMessage.showerror("Error", "Fields are Empties")
        except Exception as e:
            print(f"Error: {type(e).__name__} -> save_updated_user")
            pass
        pass 
    
    def clean_user_info(self):
        #Cleaning fields
        try:
            result = errorMessage.askquestion("Clean","Do you want to clean all fields?")

            if(result):
                userdata = self.load_user_info()
                userEmail = userdata["email"]
                #Delete user data
                query = "DELETE FROM user WHERE email = ?"
                self.run_dataBase(self.db_user,query,(userEmail,))
                time.sleep(1)
                self.frame_user()
            else:
                time.sleep(1)
                self.frame_user()

        except Exception as e:
            print(f"Error: {type(e).__name__} -> clean_user_info ")
            pass

    def test_user(self,email,password):
        try:
            """Checking if user email and password is correct, testing the scrapping code"""
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
                else:
                    #success login message
                    errorMessage.showinfo("Success","Your email and password are correct")
                    time.sleep(2)
                    self.frame_user()
        except Exception as e:
            print(f"Error: {type(e).__name__} -> test_user ")
            pass
             
    #Settings : time  
    def frame_time(self):
        try:
            self.hide_frames()
            self.frameTime = Frame(self.window,bg="#2c2c2c",width=440,height=400)
            self.frameTime.pack(fill="both",expand=1)

            clock_Data = self.load_clock_data()

            #Info Label
            info_text =Label(self.frameTime,text="Set your time, example: 14:00:00 (2pm) \n < hour:minute:second >\n in Military time format")
            info_text.config(bg="#2c2c2c",fg="#ffff00")
            info_text.grid(row=0,column=0,columnspan=4,pady=20)

            #Framer Time
            timer_settings = LabelFrame(
                self.frameTime,
                text="Timer",
                padx=5,
                pady=5)
            timer_settings.config(bg="#2c2c2c",fg="#fff")
            timer_settings.grid(
                row=1,
                column=0,
                columnspan=4,
                padx=150,
                pady=10,
                sticky=N)

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
            frameBtn.grid(row=2,column=0,columnspan=6,pady=10)

            #Buttons
            #Save Button
            save_btn = Button(frameBtn,text="Save",padx=15,pady=10)
            save_btn.grid(row=0,column=0,columnspan=2,padx=6)

            #Update Button
            update_btn = Button(
                frameBtn,text="Edit",
                padx=15,
                pady=10,
                command=lambda:self.update_clock_data(
                    timer_settings,save_btn,
                    update_btn,clean_btn))
            update_btn.grid(row=0,column=2,columnspan=2,padx=6)

            # Clean Button
            clean_btn = Button(
                frameBtn,text="Clean",
                padx=15,
                pady=10,
                command=self.clean_clock_data)
            clean_btn.grid(row=0,column=4,columnspan=2,padx=6)

            if(clock_Data):
                #Clock_in Entry
                clockIn_time = f"{clock_Data[0]['hour']}:{clock_Data[0]['minutes']}:{clock_Data[0]['seconds']}"
                clock_in = Entry(
                    timer_settings,
                    width=8,
                    textvariable=StringVar(timer_settings,clockIn_time),state="disabled")
                clock_in.grid(row=0,column=1)

                #Break in Entry
                breakIn_time = f"{clock_Data[1]['hour']}:{clock_Data[1]['minutes']}:{clock_Data[1]['seconds']}"
            
                break_in = Entry(
                    timer_settings,
                    width=8,
                    textvariable=StringVar(timer_settings,breakIn_time),state="disabled")
                break_in.grid(row=1,column=1)

                #break out entry
                breakOut_time = f"{clock_Data[2]['hour']}:{clock_Data[2]['minutes']}:{clock_Data[2]['seconds']}"
                break_out = Entry(
                    timer_settings,
                    width=8,
                    textvariable=StringVar(timer_settings,breakOut_time),state="disabled")
                break_out.grid(row=2,column=1,sticky=W)

                #Clock_Out Entry
                clockOut_time = f"{clock_Data[3]['hour']}:{clock_Data[3]['minutes']}:{clock_Data[3]['seconds']}"
                clock_out = Entry(
                    timer_settings,
                    width=8,
                    textvariable=StringVar(timer_settings,clockOut_time),state="disabled")
                clock_out.grid(row=3,column=1)

                #Buttons
                save_btn.config(bg="#7f7f7f",fg="#fff",state="disabled")
                update_btn.config(bg="#83c333",fg="#fff")
                clean_btn.config(bg="#83c333",fg="#fff",state="normal")

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
                save_btn.config(
                    bg="#83c333",
                    fg="#fff",
                    command=lambda:self.save_clock_data(
                        clock_in.get(),
                        break_in.get(),
                        break_out.get(),
                        clock_out.get()))
                update_btn.config(bg="#7f7f7f",fg="#fff",state="disabled")
                clean_btn.config(bg="#7f7f7f",fg="#fff",state="disabled")
        except Exception as e:
            print(f"Error: {type(e).__name__} -> frame_time ")
            pass
        
    def save_clock_data(self,clock_in,break_in,break_out,clock_out):
        try:
            if(not(clock_in == "" or len(clock_in) < 8) and 
            not(break_in == "" or len(break_in) < 8) and 
            not(break_out == "" or len(break_out) < 8) and 
            not(clock_out == "" or len(clock_out) < 8)):
                #DAta
                clock_Data = [clock_in,break_in,break_out,clock_out]
                #Creat Pickle Documet
                query = "INSERT INTO timeClock VALUES (?,?,?,?)"
                parameters = tuple(clock_Data)
                self.run_dataBase(self.db_clockTime,query,parameters)
                self.frame2.destroy()
                time.sleep(1)
                self.frame_time()
                # self.restart()

            else:
                errorMessage.showerror("Error", "Fields are Empties or Wrong format")
                pass
        except Exception as e:
            print(f"Error: {type(e).__name__} -> save_clock_data ")
            pass
    
    def load_clock_data(self):
        try:
            clock_Data = None
            query = "SELECT * FROM timeClock"
            userdata = self.run_dataBase(self.db_clockTime,query).fetchone()
            if(userdata):
                """Getting info then aplly Split in order to get Hour minute second"""
                clock_in,break_in,break_out,clock_out = userdata

                #Clock_in
                clock_in_hour,clock_in_minute,clock_in_seconds = clock_in.split(":")
                #Break_in
                break_in_hour,break_in_minute,break_in_seconds = break_in.split(":")
                #Break_out
                break_out_hour,break_out_minute,break_out_seconds = break_out.split(":")
                #Clock_out
                clock_out_hour,clock_out_minute,clock_out_seconds = clock_out.split(":")
        
                """Creating Dictionaries in order to save info and be able to use them, getting by their properties"""
                #Clock_in
                clockIn = {"hour":int(clock_in_hour),"minutes":int(clock_in_minute),"seconds":int(clock_in_seconds)}
                #break_in
                breakIn = {"hour":int(break_in_hour),"minutes":int(break_in_minute),"seconds":int(break_in_seconds)}
                #break_out
                breakOut = {"hour":int(break_out_hour),"minutes":int(break_out_minute),"seconds":int(break_out_seconds)}
                #Clock_in
                clockOut = {"hour":int(clock_out_hour),"minutes":int(clock_out_minute),"seconds":int(clock_out_seconds)}


                """Creating a list with all dictionaries"""
                clock_Data = [clockIn,breakIn,breakOut,clockOut]
                return clock_Data
            else:
                return clock_Data
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Error: {type(e).__name__} -> load_clock_data ")
            pass

    def update_clock_data(self,timer_settings,save_btn,update_btn,clean_btn):
        try:
            #Getting data
            clock_Data = self.load_clock_data()

            #Clock_in Entry
            clockIn_time = f"{clock_Data[0]['hour']}:{clock_Data[0]['minutes']}:{clock_Data[0]['seconds']}"
            clock_in = Entry(
                timer_settings,
                width=8,
                textvariable=StringVar(timer_settings,clockIn_time),
                state="normal")
            clock_in.grid(row=0,column=1)

            #Break in Entry
            breakIn_time = f"{clock_Data[1]['hour']}:{clock_Data[1]['minutes']}:{clock_Data[1]['seconds']}"
            break_in = Entry(
                timer_settings,
                width=8,
                textvariable=StringVar(timer_settings,breakIn_time),
                state="normal")
            break_in.grid(row=1,column=1)

            #break out entry
            breakOut_time = f"{clock_Data[2]['hour']}:{clock_Data[2]['minutes']}:{clock_Data[2]['seconds']}"
            break_out = Entry(
                timer_settings,
                width=8,
                textvariable=StringVar(timer_settings,breakOut_time),
                state="normal")
            break_out.grid(row=2,column=1,sticky=W)

            #Clock_Out Entry
            clockOut_time = f"{clock_Data[3]['hour']}:{clock_Data[3]['minutes']}:{clock_Data[3]['seconds']}"
            clock_out = Entry(
                timer_settings,
                width=8,
                textvariable=StringVar(timer_settings,clockOut_time),
                state="normal")
            clock_out.grid(row=3,column=1)

            #Buttons
            #Buttons
            save_btn.config(
                bg="#83c333",
                fg="#fff",
                state="normal",
                command=lambda:self.save_newClock_data(
                    clock_in.get(),
                    break_in.get(),
                    break_out.get(),
                    clock_out.get()))
            update_btn.config(bg="#7f7f7f",fg="#fff",state="disabled")
            clean_btn.config(bg="#7f7f7f",fg="#fff",state="disabled")


        except Exception as e:
            print(f"Error: {type(e).__name__} -> update_clock_data")
            pass 
    
    def save_newClock_data(self,clock_in,break_in,break_out,clock_out):
        try:
            if(not(clock_in == "" or len(clock_in) < 8) and 
            not(break_in == "" or len(break_in) < 8) and 
            not(break_out == "" or len(break_out) < 8) and 
            not(clock_out == "" or len(clock_out) < 8)):
                #Time Data
                clock_Data = [clock_in,break_in,break_out,clock_out]
                #run data base
                query = "UPDATE timeClock SET time_clockIn = ?, time_breakIn = ?, time_breakOut = ?, time_clockOut = ?"
                parameters = tuple(clock_Data)
                self.run_dataBase(self.db_clockTime,query,parameters)
                time.sleep(1)
                self.frame_time()         
            else:
                errorMessage.showerror("Error", "Fields are Empties or Wrong format")
                pass
        except Exception as e:
            print(f"Error: {type(e).__name__} -> save_newClock_data ")
            pass
        
    def clean_clock_data(self):
        #Delete file
        try:
            result = errorMessage.askquestion("Clean","Do you want to clean all fields?")

            if(result):
                #Query
                query = "DELETE FROM timeClock"
                self.run_dataBase(self.db_clockTime,query)
                time.sleep(1)
                self.frame_time()
            else:
                time.sleep(1)
                self.frame_time()
        except Exception as e:
            print(f"Error: {type(e).__name__} -> clean_clock_data ")
            pass

    #shift Logic
    def shift(self):
        try:
            #Checking if there is weekend
            day_name = time.strftime("%A")
            #Days
            friday = day_name.lower() == "friday"
            saturday = day_name.lower() == "saturday"
            sunday = day_name.lower() == "sunday"
            #Weekend
            weekend = saturday or sunday
            #Get Hour Minute Seconds
            today_hour = int(time.strftime("%H"))
            today_minute = int(time.strftime("%M"))
            today_second = int(time.strftime("%S"))
            #variables to get shift value form user db
            shift = ""

            #Get shift
            user = self.load_user_info()
            if(user):
                shift = user["shift"]

            #Night shift Friday until 08 am
            friday_Hour = today_hour >= 5 and today_minute >= 0 and today_second >= 10
            #Night shift sunday from 20 pm
            sunday_Hour = today_hour < 20 and today_minute >= 0 and today_second >= 0

            if(shift.lower() == "day"):
                if(not(weekend)):
                    # self.check_time()
                    print("Turno diurno activado")
                else:
                    print("Day shift: day off")
              
            if(shift.lower() == "night"):
                if((friday and not(friday_Hour)) and not(saturday) and (sunday and not(sunday_Hour))):
                    print("Turno nocturno activado")
                    pass
                else:
                    print("Night shift: day off")

        except Exception as e:
            print(f"Error: {type(e).__name__} -> shift")
            pass

    #Time-Clock-Counter
    def digitalClock(self):
        """Show a clock in order to watch the current time at the moment, when we get the current time, this code tries to figure out if the app is running on weekdays or weekends, in order to work without any issue depending on the daily shift or night shift."""
        try:
            today_text = time.strftime("%H:%M:%S")
            
            #Get Hours data and user info
            clockData = self.load_clock_data()
            user = self.load_user_info()

            if(not(user == None) and not(clockData == None)):
                # self.shift()
                pass

            #Labels
            self.showHour.config(text=today_text,bg="#2c2c2c",fg="#fff")
            self.showHour.grid(row=2,column=1,padx=2,pady=4,sticky=W)
            self.showHour.pack_forget()
            self.showHour.after(1000, self.digitalClock)
        except TypeError:
            pass
        except Exception as e:
            print(f"Error: {type(e).__name__} -> digitalClock")
            pass  
    
    #Start Bot-App   
    def check_time(self):
        """This code just takes time and start evaluating different parameters, this code start web scrapping code allowing us to open a browser and take data user from dataBases, and start 'Clock in' and 'Clock out' inside the bamboo page """
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
                """Assigning all values to these variables"""
                clock_in = clockData[0]
                break_in = clockData[1]
                break_out = clockData[2]
                clock_out = clockData[3]
            #Clock In
            if(today_hour == clock_in["hour"] and 
            today_minute == clock_in["minutes"] and 
            today_second == clock_in["seconds"]):
                # self.tld_clockIn.startConnection()
                records_name = "Clock In"
                self.clockIn_message = self.tld_clockIn.clockTime()
                self.active_clockIn_message = True
                self.save_records(records_name,self.clockIn_message)
                time.sleep(1)
                self.frame_Sencond()     
            #Break In
            if(today_hour == break_in["hour"] and 
           today_minute == break_in["minutes"] and 
           today_second == break_in["seconds"]):
                # self.tld_breakIn.startConnection()
                records_name = "Break In"
                self.breakIn_message = self.tld_breakIn.clockTime()
                self.active_breakIn_message = True
                self.save_records(records_name,self.breakIn_message)
                time.sleep(1)
                self.frame_Sencond()
            #Break Out
            if(today_hour == break_out["hour"] and 
            today_minute == break_out["minutes"] and 
            today_second == break_out["seconds"]):
                # self.tld_breakOut.startConnection()
                records_name = "Break Out"
                self.breakOut_message = self.tld_breakOut.clockTime()
                self.active_breakOut_message = True
                self.save_records(records_name,self.breakOut_message)
                time.sleep(1)
                self.frame_Sencond()
            #Clock Out
            if(today_hour == clock_out["hour"] and 
           today_minute == clock_out["minutes"] and 
           today_second == clock_out["seconds"]):
                # self.tld_clockOut.startConnection()
                records_name = "Clock Out"
                self.clockOut_message = self.tld_clockOut.clockTime()
                self.active_clockOut_message = True
                self.save_records(records_name,self.clockOut_message)
                time.sleep(1)
                self.frame_Sencond()
                
        except Exception as e:
            print(f"Error CheckTime: {type(e).__name__}")
            pass

    #Records
    def save_records(self,records_name,record_value):
        try:
            #Data Base
            query = "INSERT into records VALUES (?,?)"
            parameters = (records_name,record_value)
            self.run_dataBase(self.db_records,query,parameters)
        except Exception as e:
            print(f"Error: {type(e).__name__} -> save_records")
            pass
    
    def load_records_one_by_one(self,parameter):
        try:
            #dataBase
            query = f"SELECT * FROM records WHERE record_name = '{parameter}'"
            records = self.run_dataBase(self.db_records,query).fetchone()
            return records
        except sqlite3.OperationalError:
            pass
        except Exception as e:
            print(f"Error Loading records: {type(e).__name__}")
            pass
    
    def len_records(self):
        try:
            #dataBase
            query = f"SELECT * FROM records"
            records = self.run_dataBase(self.db_records,query).fetchall()
            return records
        except sqlite3.OperationalError:
            pass
        except Exception as e:
            print(f"Error len(Loading records): {type(e).__name__}")

    def show_records(self):
        try:
            clockIn = self.load_records_one_by_one("Clock In")
            breakIn = self.load_records_one_by_one("Break In")
            breakOut = self.load_records_one_by_one("Break Out")
            clockOut = self.load_records_one_by_one("Clock Out")
  
            if(clockIn):
                self.clockIn_message = clockIn[1]
            else:
                self.clockIn_message = "No records Yet"

            if(breakIn):
                self.breakIn_message = breakIn[1]
            else:
                self.breakIn_message = "No records Yet"
                
            if(breakOut):
                self.breakOut_message = breakOut[1]
            else:
                self.breakOut_message = "No records Yet"
                
            if(clockOut):
                self.clockOut_message = clockOut[1]
            else:
                self.clockOut_message = "No records Yet"
            
        except Exception as e:
            print(f"Error: {type(e).__name__} -> show_records")
            pass
      
    #Help Frame
    def manual(self):
        pass
    
    def send_feedback(self):
        pass
       
    def about_bot(self):
        try:
            self.hide_frames()
            self.frameabout.pack(fill="both",expand=1)
        
            #Image logo
            image = Label(self.frameabout,image=self.logo)
            image.config(bg="#2c2c2c")
            image.pack(side="top",pady=30)

            #Label
            text_Content = "A-B0T\nVersion 0.0.1\n\nA-B0T is an automated bot helping us to control\nthe 'clock in' and 'clock out' within a time range\n set by the user with its Bammboo account data\nthe bot is built with python 3.11 and Selenium.5\n\n© A-B0T 2023. All rights reserved"
            welcome = Label(self.frameabout, text=text_Content)
            welcome.config(bg="#2c2c2c",fg="#fff",font=("@Yu Gothic UI Semilight",10))
            welcome.pack(pady=5)

            link = Label(self.frameabout,text="\nSource Code")
            link.config(bg="#2c2c2c", fg="#1e90ff", cursor="hand2")
            link.pack()
            link.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/EumT07/A-B0T_version_0.0.1"))
        except Exception as e:
            print(type(e).__name__)
            pass


    def reboot(self):
        try:
            value = errorMessage.askokcancel("Reboot","Reboot will Delete data records and Start the app again.\n\nAre you sure to want to reboot the app?")

            if(value):
                #Delete all records data
                query = "DELETE FROM records"
                self.run_dataBase(self.db_records,query)
                time.sleep(1)
                message = "Please wait until the app finishes, don't close the app"
                self.loading_progessBar(message)
            else:
                pass
               
        except Exception as e:
            print(type(e).__name__)
        
    def factory_restore(self):
        try:
            db_tables = ['user','records','timeClock']
            db_files = [self.db_user,self.db_records,self.db_clockTime]

            value = errorMessage.askokcancel("Factory Restore","Factory Restore will Delete all data (user info, time Clock info, records info) and Start the app again.\n\nAre you sure to want to reset Factory defaults?")

            if(value):
                for db in zip(db_files,db_tables):
                    query = f"DELETE FROM {db[1]}"
                    self.run_dataBase(db[0],query)
                message = f"Please wait until Factory Restory ends, don't close the app"
                self.loading_progessBar(message)  
            else:
                pass
        except Exception as e:
            print(type(e).__name__)
        pass

    #Records More than 4, trying to clear records and avoid any king of mistake
    def check_records(self):
        """Check if app got 4 records, and cleaning this data for the momemt, this helps to app works without any problems"""
        try:
            records = self.len_records()
            if(len(records) == 4):
                query = "DELETE FROM records"
                self.run_dataBase(self.db_records,query)
            else:
                pass
        except TypeError:
            print("Check string query")
            pass
        except Exception as e:
            print(f"Error Check_records : {type(e).__name__}")
            pass
    
    def loading_app(self):
        try:
            #Clean screen
            self.hide_frames()
            self.frameLoading = Frame(self.window,bg="#2c2c2c",width=440,height=400)
            self.frameLoading.pack(fill="both",expand=1)

            #Image logo
            image = Label(self.frameLoading,image=self.logo)
            image.config(bg="#2c2c2c")
            image.pack(side="top",pady=30)
            time.sleep(1)
            def step():
                for i in range(5):
                    self.frameLoading.update_idletasks()
                    progresBar['value'] += 20
                    time.sleep(1)
                    text_value = "Loading", round(progresBar['value']),"%"
                    text.config(text=text_value)
            
            #Widget messge
            message_text = "Please wait until the app load all the features"
            message = Label(
                self.frameLoading,
                text=message_text,
                bg="#2c2c2c",
                fg="#fff")
            message.pack(pady=5)
            #Widget
            progresBar = ttk.Progressbar(
                self.frameLoading,
                orient="horizontal",
                length=260,
                mode="determinate")
            progresBar.pack(side="top",pady=10)

            #Widget text
            text = Label(self.frameLoading,text="0%",bg="#2c2c2c",fg="#fff")
            text.pack(padx=20,pady=10)
            
            time.sleep(1)
            step()

            #This works -> but Not sure if it is necessary
            image.pack_forget()
            progresBar.pack_forget()
            message.pack_forget()
            text.pack_forget()
            self.frameLoading.pack_forget()
            self.frameLoading.destroy()
            time.sleep(1)
            self.frame_Principal()
            pass
        except Exception as e:
            print(f"Error Loading_progres bas : {type(e).__name__}")
            pass
    
    def loading_progessBar(self,message = None):
        try:
            #Clean screen
            self.hide_frames()
            self.frameLoading = Frame(self.window,bg="#2c2c2c",width=440,height=400)
            self.frameLoading.pack(fill="both",expand=1)

            #Image logo
            image = Label(self.frameLoading,image=self.logo)
            image.config(bg="#2c2c2c")
            image.pack(side="top",pady=30)
            time.sleep(1)
            def step():
                for i in range(5):
                    self.frameLoading.update_idletasks()
                    progresBar['value'] += 20
                    time.sleep(1)
                    text_value = "Loading", round(progresBar['value']),"%"
                    text.config(text=text_value)
                    

            message_label = Label(
                self.frameLoading,
                bg="#2c2c2c",
                fg="#fff",
                text=message)
            message_label.pack(pady=5)
            #Widget
            progresBar = ttk.Progressbar(
                self.frameLoading,
                orient="horizontal",
                length=260,
                mode="determinate")
            progresBar.pack(side="top",pady=10)

            #Widget text
            text = Label(self.frameLoading,text="0%",bg="#2c2c2c",fg="#fff")
            text.pack(padx=20,pady=10)
            
            time.sleep(1)
            step()

            #This works -> but Not sure if it is necessary
            image.pack_forget()
            progresBar.pack_forget()
            message_label.pack_forget()
            text.pack_forget()
            self.frameLoading.pack_forget()
            self.frameLoading.destroy()
            time.sleep(1)
            self.restart()
            pass
        except Exception as e:
            print(f"Error Loading_progres bas : {type(e).__name__}")
            pass
    #Restart APP          
    def restart(self):
        """There is an issue, I haven't figured out yet, but the problem is when you save data and start the app when the app is running, it starts writing text on top of the previous text, I think the problem is when we try to delete or destroy the frame. So next code just close the app and start again to avoid this issue."""
        try:
            self.window.destroy()
            #Path with python/tkinter app when is running with cmd
            os.startfile("main.py")
            #Path when this pass is a desktop app.
            # os.startfile(resource_path("A-B0T.exe"))
        except Exception as e:
            errorMessage.showwarning("Error",f"Path Erro: {type(e).__name__}")
            
        
if __name__ == "__main__":
    window = Tk()
    app = TLDClock(window)
    window.mainloop()