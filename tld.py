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

class Tld():
    def __init__(self,email,password):
        self.email = email
        self.password = password

    def startConnection(self):
        driver = webdriver.Chrome()
        url = os.getenv("url")
        driver.implicitly_wait(10)
        driver.get(url)
        time.sleep(5)
        self.login(driver)
        return

    def login(self,driver):
        driver.implicitly_wait(10)
        #Email
        setEmail =  driver.find_element(By.ID, "lemail")
        setEmail.send_keys(self.email)
        #password
        setPassword =  driver.find_element(By.ID, 'password')
        setPassword.send_keys(self.password)
        #Login Button
        loginButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        
        # waiting
        time.sleep(4)
        loginButton.click()

        #Get info
        time.sleep(4)
        ads_info =  driver.find_element(By.CLASS_NAME, "MuiBox-root")

        if(ads_info):
            confirm_ads = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "css-fngne8")))
            time.sleep(4)
            confirm_ads.click()

        self.clock(driver)
        return
        
    def clock(self,driver):
        # driver.implicitly_wait(5)
        # clock_In = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "css-fngne8")))
        # # waiting
        # time.sleep(4)
        # clock_In.click()
        time.sleep(4)
        self.quit(driver)
        return
        
    def quit(self,driver):
        driver.close()
        return
    

class Clock_In(Tld):
    def __init__(self,email,password):
        super().__init__(email,password)
    

class Clock_Out(Tld):
    def __init__(self,email,password):
        super().__init__(email,password)


class Break_In(Tld):
    def __init__(self,email,password):
        super().__init__(email,password)


class Break_Out(Tld):
    def __init__(self,email,password):
        super().__init__(email,password)

    

