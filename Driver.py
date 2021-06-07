from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class Driver:

    def __init__(self):
        PATH = "C:\Program Files (x86)\chromedriver.exe"
        self.d = webdriver.Chrome(PATH)

    def acceptcookies(self):
        try:
            ac = WebDriverWait(self.d, 4).until(EC.presence_of_element_located(
                (By.LINK_TEXT, "AUSWAHL BESTÄTIGEN")))
            ac.click()
        except:
            return None

    def opentabs(self):
        # find selections for Bundeslaender and vacc centers
        selections = WebDriverWait(self.d, 10).until(EC.presence_of_element_located(
            (By.CLASS_NAME, "selection")))

        # holds the right indexes for the wanted vacc centers
        vacccentersindexlist = [12, 36, 37, 38, 39, 40]

        # index for list of vacc centers
        centerindex = 0

        for i in range(6):
            self.d.execute_script("window.open('');")
            self.d.switch_to.window(self.d.window_handles[i + 1])
            self.d.get("https://www.impfterminservice.de/impftermine")

            selections = WebDriverWait(self.d, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "selection")))

            # choose BW as Bundesland
            selections[0].click()
            blnder = WebDriverWait(self.d, 10).until((EC.presence_of_all_elements_located(
                (By.TAG_NAME, "li"))))
            blnder[1].click()

            # choose Impfzentren
            selections[1].click()
            vacccenters = WebDriverWait(self.d, 10).until(EC.presence_of_all_elements_located(
                (By.TAG_NAME, "li")))
            vacccenters[vacccentersindexlist[centerindex]].click()
            centerindex = centerindex + 1

            # click submitbtn
            buttons = WebDriverWait(self.d, 10).until(EC.presence_of_all_elements_located(
                (By.TAG_NAME, "button")))
            submitbtn = buttons[1]
            submitbtn.click()

            # accept cookies
            self.acceptcookies()

        # close first tab
        self.d.switch_to.window(self.d.window_handles[0])
        self.d.close()

    def loopthroughtaps(self):
        tapindex = 0
        h1ofwaitingroom = "Virtueller Warteraum des Impfterminservice"
        h1ofcoderoom = "Wurde Ihr Anspruch auf eine Corona-Schutzimpfung bereits geprüft?"
        while True:
            self.acceptcookies()
            tapindex = self.controltapindex(tapindex)
            self.d.switch_to.window(self.d.window_handles[tapindex])
            h1 = WebDriverWait(self.d, 10).until(EC.presence_of_element_located(
                (By.TAG_NAME, "h1")))
            if h1.text == h1ofwaitingroom:
                print("waiting room in tap " + str(tapindex + 1))
                tapindex = tapindex + 1
                continue
            elif h1.text == h1ofcoderoom:
                btns = WebDriverWait(self.d, 10).until(EC.presence_of_all_elements_located(
                    (By.CLASS_NAME, "ets-radio-control")))
                nobtn = btns[1]
                nobtn.click()
                print("coderoom in tap " + str(tapindex + 1))
                tapindex = tapindex + 1
                continue
            else:
                print("-----------------------------")
                print("next room reached in tap " + str(tapindex + 1))
                print("-----------------------------")
                break

    def controltapindex(self, tapindex):
        if tapindex == 6:
            tapindex = 0
            return tapindex
        else:
            return tapindex




