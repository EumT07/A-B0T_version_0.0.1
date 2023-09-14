# from tkinter import *
# from tkinter import ttk
# import os
# import time


# def counter():
#     hour = 7
#     minute = 59
#     second = 40

#     while(True):
#         os.system("cls")
#         print(f"Hour - {hour}:{minute}:{second} -")
#         time.sleep(1)
#         second += 1
#         if (second == 59):
#             minute += 1
#             second = 0
#             if (minute > 59):
#                 hour += 1
#                 minute = 0
#                 if (hour == 8):
#                     print("Bro your times has gone")
#                     break
#             continue
#         continue

running = False
hour = 0
minute = 0
second = 0

def digital_counter(self):
        #Add 1
        second += 1
        
        if(running):
            if(second == 60):
                minute += 1
                second = 0
                if(minute >= 59):
                    hour += 1
                    minute = 0
                    
        
    
def start_digital_counter(self):
    self.running = True
    self.digital_counter()


def stop_digital_counter(self):
    self.running = False
    self.digital_counter()

    

            
        


# counter()