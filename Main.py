from Driver import *


# setup driver
driver = Driver()

# accept cookies
driver.d.get("https://www.impfterminservice.de/impftermine")
driver.acceptcookies()

# open one tab for each vacc center
driver.opentabs()

# loop through tabs
driver.loopthroughtaps()

# make appointment?
