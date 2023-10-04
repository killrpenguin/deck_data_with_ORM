from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium_driver import Driver_Obj
from selenium.webdriver.support import expected_conditions as ec
from selenium.common import NoSuchElementException, ElementNotInteractableException


testing = Driver_Obj()
"""
with open("mxlinks", "r") as links:
    links_list = links.read().strip().split("\n")
    for link in links_list:
        testing.scrape(link)
        break
"""
xpath = "/html/body/div[2]/div/main/h1"
testing.scrape("https://nowsecure.nl")
wait = WebDriverWait(testing.driver, 30)
wait.until(ec.text_to_be_present_in_element_value((By.XPATH, xpath), text_="OH YEAH"))
testing.driver.save_screenshot("test.png")