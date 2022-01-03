""" A script aimed to send and retreive messages via messenger """
# this script is resistant to selenium depreciated error


from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains as A
from selenium.webdriver.common.keys import Keys as K
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
import os
import time
import config

# suppression des affichages de webdriver-manager
os.environ["WDM_LOG_LEVEL"] = "0"
os.environ["WDM_PRINT_FIRST_LINE"] = "False"


def connect():
    r"""
    Set up of the bot

    This function launch a selenium driver and connect to messenger
    """

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("headless")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    browser = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )  # maybe shoud i've call it driver
    browser.get("https://www.messenger.com/t/100010820648031")
    accept = browser.find_elements(By.CLASS_NAME, "_42ft")
    accept[3].click()

    inputs = browser.find_elements(By.CLASS_NAME, "inputtext")
    inputs[0].send_keys(config.USR)
    inputs[1].send_keys(config.PWD)
    inputs[1].send_keys(K.ENTER)

    time.sleep(2)
    return browser


def send_message(browser, message):
    r"""Send the message in "message" string"""
    action = A(browser)
    action.send_keys(message + "\n").perform()


def retreive_messages(browser):
    """Retreive the last message send by user"""
    elems = browser.find_elements(By.CSS_SELECTOR, "div")  # yes it's violent
    text = elems[0].text.split("\n")
    message = _extract_messages(text)
    return message


def _extract_messages(text):
    """extract the message from raw text"""

    begin, start = None, None
    for index in range(len(text) - 1, 0, -1):
        if text[index] == "Entrer":
            end = index
        if text[index] == "Hadrien":
            begin = index
        if begin != None and end != None:
            return text[begin + 1 : end]

    return []


if __name__ == "__main__":
    browser = connect()
    time.sleep(1)
    # send_message(browser, "Hello world")
    print(retreive_messages(browser))
    browser.close()
