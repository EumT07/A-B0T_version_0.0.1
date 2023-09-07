#imports
import os
from tld import *
from datetime import datetime
import time
from dotenv import load_dotenv

load_dotenv()
#and today.minute == 0 and today.second == 0
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
            if (today.hour == 11 and today.minute == 37 and today.second == 0):
                self.tld_clockIn.startConnection()
                continue
            elif(today.hour == 11 and today.minute == 38 and today.second == 0):
                self.tld_breakIn.startConnection()
                continue
            elif(today.hour == 11 and today.minute == 40 and today.second == 0):
                self.tld_breakOut.startConnection()
                continue
            elif(today.hour == 11 and today.minute == 42 and today.second == 0):
                self.tld_clockOut.startConnection()
                break
            
            

#Start
if __name__ == "__main__":
    email = os.getenv("email")
    password = os.getenv("password")
    start = Clock(email,password)
    start.getTime()


