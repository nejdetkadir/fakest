import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from datetime import datetime
from Fakest import Fakest
import sched
import time


class UI(QtWidgets.QWidget):

    def __init__(self, fakest):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setFixedHeight(300)
        self.setFixedWidth(500)
        self.setWindowTitle("Fake student | FAKEST")

        self.studentNumberInput = QtWidgets.QLineEdit()
        self.studentPasswordInput = QtWidgets.QLineEdit()
        self.lessonUrlInput = QtWidgets.QLineEdit()
        self.datetimeInput = QtWidgets.QDateTimeEdit()

        vBoxLay = QtWidgets.QVBoxLayout()

        vBoxLay.addWidget(self.studentNumberInput)
        vBoxLay.addWidget(self.studentPasswordInput)
        vBoxLay.addWidget(self.lessonUrlInput)
        vBoxLay.addWidget(self.datetimeInput)

        hBoxLay = QtWidgets.QHBoxLayout()

        self.startButton = QtWidgets.QPushButton("START")
        self.quitButton = QtWidgets.QPushButton("QUIT")

        hBoxLay.addWidget(self.startButton)
        hBoxLay.addWidget(self.quitButton)

        vBoxLay.addLayout(hBoxLay)

        self.alertLabel = QtWidgets.QLabel()
        vBoxLay.addWidget(self.alertLabel)

        vBoxLay.addStretch()

        self.setLayout(vBoxLay)

        self.customizeWidgets()
        self.startButton.clicked.connect(self.checkValidation)
        self.quitButton.clicked.connect(self.quit)
        self.show()

    def customizeWidgets(self):
        self.studentNumberInput.setPlaceholderText("Student number")
        self.studentPasswordInput.setPlaceholderText("Password of your LMS account")
        self.lessonUrlInput.setPlaceholderText("URL of your lesson")
        self.datetimeInput.setDateTime(QtCore.QDateTime.currentDateTime())

        self.quitButton.setDisabled(True)

    def checkValidation(self):
        rightNow = datetime.now()
        datetimeArray = [rightNow, self.datetimeInput.dateTime().toPyDateTime()]
        datetimeArray.sort()

        if len(self.studentNumberInput.text()) != 9:
            self.alertLabel.setText("Please check your student number")
        elif 6 > len(self.studentPasswordInput.text()) or len(self.studentPasswordInput.text()) > 15:
            self.alertLabel.setText("Please check length of your password")
        elif len(self.lessonUrlInput.text()) != 75:
            self.alertLabel.setText("Please check your URL")
        elif datetimeArray[1] == rightNow and (datetimeArray[1] - datetimeArray[0]).seconds < 30:
            self.alertLabel.setText(
                "Can you check your datetime? You can replace with a future date.\nMaybe 2 minutes later ?")
        elif (datetimeArray[1] - datetimeArray[0]).seconds > 70000:
            self.alertLabel.setText("Can you replace with a older date? Maybe 1 or 2 hours ago?")
        else:
            self.alertLabel.setText(None)
            self.startButton.setDisabled(True)
            self.quitButton.setDisabled(False)
            self.waitForLogin()

    def login(self):
        self.fakest = Fakest(self.alertLabel)
        self.fakest.login(self.studentNumberInput.text(), self.studentPasswordInput.text())
        self.goToLesson()

    def goToLesson(self):
        self.fakest.whichLesson(self.lessonUrlInput.text())
        self.fakest.whichWeek()

    def waitForLogin(self):
        scheduler = sched.scheduler(time.time, time.sleep)
        scheduler.enter(((self.datetimeInput.dateTime().toPyDateTime() - datetime.now()).seconds - 60), 1, self.login)
        scheduler.run()

    def quit(self):
        self.fakest.quit()
        self.quit()