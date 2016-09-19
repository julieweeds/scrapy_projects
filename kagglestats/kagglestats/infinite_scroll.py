import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Chrome()

browser.get("https://www.kaggle.com/datasets?sortBy=hottest&group=all")
time.sleep(1)

elem = browser.find_element_by_tag_name("body")

no_of_pagedowns = 60

while no_of_pagedowns:
    print(elem.text)
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.2)
    no_of_pagedowns-=1
