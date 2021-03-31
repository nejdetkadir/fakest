from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By


class Fakest:

    def __init__(self):
        self.baseUrl = "https://lms.bandirma.edu.tr"
        self.driver = webdriver.Chrome()
        WebDriverWait(self.driver, 2)
        self.driver.get(self.baseUrl)

    def login(self, studentNum, studentPass):
        self.driver.find_element_by_xpath('//*[@id="UserName"]').send_keys(studentNum)
        self.driver.find_element_by_xpath('//*[@id="btnLoginName"]').click()

        self.driver.find_element_by_xpath('//*[@id="Password"]').send_keys(studentPass)
        self.driver.find_element_by_xpath('//*[@id="btnLoginPass"]').click()

        # check login operation
        self.checkUrl("https://lms.bandirma.edu.tr/Home/Index", "An error occurred while logging in")

    def quit(self):
        self.driver.quit()

    def checkUrl(self, url, message):
        if self.driver.current_url == url:
            print(message)
            self.quit()
