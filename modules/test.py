#imports
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time

class Test():
    """Propierties"""
    url= "https://languagedoctors.bamboohr.com/login.php?r=%2Fhome"
    loginError = None
    def __init__(self,email,password):
        self.email = email
        self.password = password

    def startConnection(self):
        """This code run the scripts"""
        try:
            driver = webdriver.Chrome()
            driver.implicitly_wait(10)
            driver.get(self.url)
            time.sleep(5)
            self.login(driver)
            return
        except Exception as e:
            print(type(e).__name__)

    def login(self,driver):
        try:
            driver.implicitly_wait(10)
            #Email -> html id tag
            setEmail =  driver.find_element(By.ID, "lemail")
            setEmail.send_keys(self.email)
            #password -> html id tag
            setPassword =  driver.find_element(By.ID, 'password')
            setPassword.send_keys(self.password)
            #Login Button
            loginButton = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
        
            # waiting
            time.sleep(4)
            loginButton.click()

            #Error Login
            time.sleep(2)
            errorLogin = driver.find_element(By.CLASS_NAME,"fabric-1v6ecp0-text").text
            
            if(errorLogin == "The email or password you entered is invalid."):
                self.loginError = "Error: Wrong Email/password " 
                time.sleep(1)
                return

            #Get info
            time.sleep(4)
            ads_info =  driver.find_element(By.CLASS_NAME, "MuiBox-root")

            if(ads_info):
                confirm_ads = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "css-fngne8")))
                time.sleep(4)
                confirm_ads.click()

            time.sleep(4)
            self.quit(driver)
            return
        except Exception as e:
            print("Error login")
            print(type(e).__name__)
        
    def quit(self,driver):
        try:
            driver.close()
            return
        except Exception as e:
            print(type(e).__name__)

