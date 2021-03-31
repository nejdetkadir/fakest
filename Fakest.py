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
        self.lessons = []
        self.weeks = []

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
        if self.driver.current_url != url:
            print(message)
            self.quit()

    def parseHTML(self):
        return BeautifulSoup(self.driver.page_source, 'html.parser')

    def parseLessons(self):
        WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="courses"]/table')))
        lessons = self.parseHTML().find_all("a", {"class": "coursename"})
        for lesson in lessons:
            self.lessons.append([self.baseUrl + lesson['href'], lesson.text])

    def parseWeeks(self):
        weeks = self.parseHTML().find_all("div", {"class": "cardItem"})
        for week in weeks:
            card = week.find("div", {"class": "cardviewtitle"})
            if card is not None:
                if card.find("span", {"class": "badge label-activity-virtualclass"}) is not None:
                    name = card.find("span", {"class": "cardViewActivityName"}).text
                    a = card.find("a", {"class": "view"})
                    self.weeks.append([self.baseUrl + a['href'], name])

    def whichLesson(self, selectedUrl=None):
        if selectedUrl is None:
            self.parseLessons()
            print("###################################")
            # print name of lessons
            order = 0
            for l in self.lessons:
                print("{} <-> {}".format(order, l[1]))
                order += 1
            print("###################################")
            while True:
                try:
                    val = int(input('Which is your lesson? : '))
                    if val < 0 or val >= len(self.lessons):
                        raise Exception("!")
                    else:
                        self.driver.get(self.lessons[val][0])
                        # go to details page of selected lesson
                    break
                except:
                    print("That's not a valid option!")
        else:
            self.driver.get(selectedUrl)

    def whichWeek(self):
        self.parseWeeks()
        # default last week
        print("###################################")
        for w in self.weeks:
            print(w[1])
        print("Selected week => {}".format(self.weeks[len(self.weeks) - 1][1]))
        self.driver.get(self.weeks[len(self.weeks) - 1][0])
        WebDriverWait(self.driver, 60).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, '.btn.btn-primary.pointer')))
        self.confirmLesson()

    def confirmLesson(self):
        time.sleep(1)
        self.driver.find_element_by_css_selector('.btn.btn-primary.pointer').click()
