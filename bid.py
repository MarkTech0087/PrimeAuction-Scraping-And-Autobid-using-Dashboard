import pyautogui
from selenium import webdriver
from selenium.webdriver import ActionChains
# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import ui
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import *
# import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from time import sleep
import json
import random
import string
from datetime import datetime
import sys
import os
import time
import re
from constant import USERNAME, PASSWORD


if len(sys.argv) == 2:
    auction_url = sys.argv[1]
    print('account', auction_url)
        
else:
    print("Incorrect number of arguments provided.")


def pressTab(count : int):
    for i in range(count):
        pyautogui.hotkey('tab')
        sleep(0.1)                    

def pressShiftTab(count : int):
    for i in range(count):
        pyautogui.hotkey('shiftleft', 'tab')
        sleep(0.1)     

def pressSpace():
    pyautogui.press('space')
    sleep(0.1)

def pressEnter():
    pyautogui.press('enter')
    sleep(1)

def pressDown(count : int):
    for i in range(count):
        pyautogui.press('down')
        sleep(0.1)

def cut():
    pyautogui.hotkey('ctrl', 'x')
    sleep(0.1)

def copy():
    pyautogui.hotkey('ctrl', 'c')
    sleep(0.1)

def paste():
    pyautogui.hotkey('ctrl', 'v')
    sleep(0.1)

def selectAll():
    pyautogui.hotkey('ctrl', 'a')
    sleep(0.1)

def typing(value : str):
    pyautogui.typewrite(value)

def wait_url(driver : webdriver.Chrome, url : str):
    print(url)
    while True:
        cur_url = driver.current_url
        if cur_url == url:
            break
        sleep(0.1)  


def next(driver : webdriver.Chrome):
    find_element(driver, By.CLASS_NAME, 'air3-btn-primary').click()

def find_element(driver : webdriver.Chrome, whichBy, unique : str) -> WebElement:
    while True:
        try:
            element = driver.find_element(whichBy, unique)
            break
        except:
            pass
        sleep(1)
    return element

def find_elements(driver : webdriver.Chrome, whichBy, unique : str) -> list[WebElement]:
    while True:
        try:
            elements = driver.find_elements(whichBy, unique)
            break
        except:
            pass
        sleep(0.1)
    return elements


driver = webdriver.Chrome()
driver.maximize_window()

def login():
    driver.get("https://auction.primeauctions.com/Public/Account/Login")
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'Username'))).send_keys(USERNAME)
        print("Inputed username successfully")
    except:
        print("Not found the login form")
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'Password'))).send_keys(PASSWORD)
        print("Inputed password successfully")
    except:
        print("Not found login form")
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,'SubmitLogin'))).click()
        print("Clicked login submit button")
    except:
        print("Not found the login")
    try:
        sleep(3)
        driver.find_element(By.CLASS_NAME, 'showSweetAlert')
        print("Incorrect username and/or password")
    except:
        print("Valid username and password")
    
login()



def bid():
    driver.get(auction_url)
    sleep(5)
    try:
        auction_status = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'divAuctionItemDetail'))).find_element(By.TAG_NAME, 'label').text
        if auction_status == "Ended":
            print("")
        print("This auction is Ended")
        # driver.quit()
    except:
        print("This auction is available")

    try:
        next_min_bid = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'min-next-bid'))).text
        print("Got the minimum next bid")
    except:
        print("Can't get the minimum next bid")
        driver.quit()

    max_bid_input = find_element(driver, By.ID, 'Detail_MaxBidAmount')
    max_bid_input.clear()
    max_bid_input.send_keys(next_min_bid)

    bid_now = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[contains(@id, "btnSubmitBid")]')))
    bid_now.click()

    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'HighestBidderCheckBox'))).click()
        print("Clicked Highest Bidder CheckBox")
        sleep(2)
    except:
        pass
    sleep(5)

    place_agree = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'agreed')))
    place_agree.click()

    sleep(3)

    error_message = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'spnErrorMsg')))
    if error_message.text == "":
        print("Success: ", "Thank you for the bid, You are the highest bidder for this item")
    else:
        print("Failed: ", error_message.text)
    driver.quit()

bid()
