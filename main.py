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
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'Username'))).send_keys("Winnj1@me.com")
        print("Inputed username successfully")
    except:
        print("Not found the login form")
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'Password'))).send_keys("Upwork1!")
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


def auction_scrape():
    try:
        auction_lists = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'auction-item-cardcolor')))
        print(len(auction_lists))
        print(f"There are {len(auction_lists)} numbers of auction")
    except:
        print("there is no any auction or couldn't find any auctions")
        driver.quit()

    auction_data_list = [] 

    for auction in auction_lists:
        auction_dict = {}
        auction_name = auction.find_element(By.CLASS_NAME, 'auction-name-limit').text
        auction_category_info = auction.find_element(By.CLASS_NAME, 'category-info').text
        auction_product_info = auction.find_element(By.CLASS_NAME, 'product-dessc')
        auction_item_number = auction_product_info.find_element(By.CLASS_NAME, 'align-items-baseline').find_element(By.TAG_NAME, 'p').text
        auction_ends_date = auction_product_info.find_element(By.CLASS_NAME, 'local-date-time').get_attribute("data-auc-date")
        auction_view_items_attr = auction_product_info.find_element(By.TAG_NAME, 'a').get_attribute('onclick')
        view_items_url = "https://auction.primeauctions.com/" + re.findall(r'"([^"]*)"', auction_view_items_attr)[0]

        print(auction_name)
        print(auction_category_info)
        print(auction_item_number)
        print(auction_ends_date)

        # Add the data to the dictionary
        auction_dict['auction_name'] = auction_name
        auction_dict['auction_category_info'] = auction_category_info
        auction_dict['auction_item_number'] = auction_item_number
        auction_dict['auction_ends_date'] = auction_ends_date
        auction_dict['view_items_url'] = view_items_url
        
        # Append the dictionary to the list
        auction_data_list.append(auction_dict)

    # Convert the list of dictionaries to a JSON string
    json_data = json.dumps(auction_data_list, indent=4)
    
    # Print the JSON string
    print(json_data)

    with open('1.json', 'w') as json_file:
        json_file.write(json_data)

    sleep(2)

    with open('1.json', 'r') as json_file:
        auction_data_list = json.load(json_file)
    
    # Iterate over each auction
    for auction in auction_data_list:
        view_items_url = auction['view_items_url']
        
        # Visit the URL using Selenium's WebDriver
        driver.get(view_items_url)
        auction["product_items"] = []
        
        while True:
            auction_product_items = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'auction-item-cardcolor')))
            print(len(auction_product_items))

            for auction_product_item in auction_product_items:
                item_dict = {}
                try:
                    item_title = auction_product_item.find_element(By.CLASS_NAME, 'Itemlist-Lottitle')
                    print("There is product item")
                except:
                    print("This is not product item")
                    continue
                
                item_title_text = item_title.text
                item_url = item_title.find_element(By.TAG_NAME, 'a').get_attribute('href')
                product_detail = auction_product_item.find_element(By.CLASS_NAME , 'auction-Itemlist-Title').text
                current_bid_amount = auction_product_item.find_element(By.XPATH, '//*[contains(@id, "CurrentBidAmount")]/span[2]').text
                auction_status = auction_product_item.find_element(By.TAG_NAME, 'label').text

                product_images = auction_product_item.find_elements(By.TAG_NAME, 'img')
                product_image_urls = [image.get_attribute('src') for image in product_images]


                print(item_title_text)
                print(item_url)
                print(product_detail)
                print(current_bid_amount)
                print(auction_status)
                print(product_image_urls)

                item_dict['item_title'] = item_title_text
                item_dict['item_url'] = item_url
                item_dict['product_detail'] = product_detail
                item_dict['current_bid_amount'] = current_bid_amount
                item_dict['auction_status'] = auction_status
                item_dict['product_image_urls'] = product_image_urls
                # sleep(0.1)

                auction['product_items'].append(item_dict)

            pagination_next_button = driver.find_element(By.XPATH, '//*[@id="contentPager"]/nav/ul/li[13]')

            if "disabled" in pagination_next_button.get_attribute("class"):
                print("Reached a page where the next button is disabled")
                break
            else:
                pagination_next_button.click()

        sleep(5)
        # After processing all auctions and their product items, write data to JSON file
        with open('1.json', 'w') as json_file:
            json.dump(auction_data_list, json_file, indent=4)

    print("Auction data collection complete.")  


auction_scrape()
sleep(10000)






driver.quit()


        

