#imports
import os
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from dotenv import load_dotenv
from datetime import date, datetime, time as timeToday
import time


load_dotenv()

class Start():
    def __init__(self,email,password):
        self.email = email
        self.password = password


    def getTime(self):
        while(True):
            #Clean terminal
            os.system("cls")
            ##Gettin Time
            today = datetime.now()
            print(f"it's {today.hour}:{today.minute}:{today.second}")
            time.sleep(1)
            if (today.hour == 14 and today.minute == 5 and today.second == 0):
                self.startConnection()
                continue
            elif(today.hour == 14 and today.minute == 9 and today.second == 0):
                print("Break")
                continue
            else:
                os.system("cls")
                print("wait")
                time.sleep(1)
                

    def startConnection(self):
        driver = webdriver.Chrome()
        url = os.getenv("url")
        driver.implicitly_wait(5)
        driver.get(url)
        self.login(driver)
        time.sleep(1000)


    def login(self,driver):
        driver.implicitly_wait(5)
        #Email
        setEmail = driver.find_element(By.ID, "lemail")
        setEmail.send_keys(self.email)
        #password
        setPassword = driver.find_element(By.ID, 'password')
        setPassword.send_keys(self.password)
        #Button
        loginButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        loginButton.click()

        #Get info
        ads_info = driver.find_element(By.CLASS_NAME, "MuiBox-root")

        if(ads_info):
            confirm_ads = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "css-fngne8")))
            confirm_ads.click()
        
        self.clockIn(driver)

    def clockIn(self,driver):
        driver.implicitly_wait(5)
        clock_In = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "css-fngne8")))
        clock_In.click()
        self.quit(driver)
        print("Clock in: start")
        

    def clockOut(self):
        print("Clock out: close")

    def quit(self,driver):
        driver.implicitly_wait(5)
        time.sleep(2)
        driver.close()
        self.getTime()
        

    

#Start
if __name__ == "__main__":
    email = os.getenv("email")
    password = os.getenv("password")
    start = Start(email,password)
    start.getTime()

