#imports
import os
from tld import *
from datetime import datetime
import time
from dotenv import load_dotenv

load_dotenv()

class Clock():
    def __init__(self,email,password):
        self.email = email
        self.password = password
        self.tld_clockIn = Clock_In(self.email,self.password)
        self.tld_clockOut = Clock_Out(self.email,self.password)
        self.tld_breakIn = Break_In(self.email,self.password)
        self.tld_breakOut = Break_Out(self.email,self.password)

        pass

    def getTime(self):
        while(True):
            #Cleaning terminal
            os.system("cls")
            ##Getting Time
            today = datetime.now()
            print(f"it's {today.hour}:{today.minute}:{today.second}")
            time.sleep(1)
            if (today.hour == 14 and today.minute == 00 and today.second == 0):
                self.tld_clockIn.startConnection()
                continue
            elif(today.hour == 19 and today.minute == 00 and today.second == 0):
                self.tld_breakIn.startConnection()
                continue
            elif(today.hour == 19 and today.minute == 30 and today.second == 0):
                self.tld_breakOut.startConnection()
                continue
            elif(today.hour == 23 and today.minute == 30 and today.second == 0):
                self.tld_clockOut.startConnection()
                break

    # def getTime(self):
    #     c = 0
    #     while(c <= 20):
    #         c += 1
    #         #Cleaning terminal
    #         os.system("cls")
    #         print(c)
    #         time.sleep(1)
    #         if (c == 5):
    #             # self.tld_clockIn.startConnection()
    #             print(self.tld_clockIn)
    #             time.sleep(2)
    #             continue
    #         elif(c == 10):
    #             # self.tld_breakIn.startConnection()
    #             print(self.tld_breakIn)
    #             time.sleep(2)
    #             continue
    #         elif(c == 15):
    #             # self.tld_breakOut.startConnection()
    #             print(self.tld_breakOut)
    #             time.sleep(2)
    #             continue
    #         elif(c == 20):
    #             # self.tld_clockOut.startConnection()
    #             print(self.tld_clockOut)
    #             time.sleep(2)
    #             break

email = os.getenv("email")
password = os.getenv("password")
start = Clock(email,password)
start.getTime()

