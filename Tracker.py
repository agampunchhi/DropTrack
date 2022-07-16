from discord import channel, message, file
import discord
import time
import requests
from bs4 import BeautifulSoup
import classes
from selenium import webdriver
from selenium.webdriver.common.by import By
import platform
import os

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'

option = webdriver.ChromeOptions()
option.add_argument('--headless')
option.add_argument("--enable-javascript")
option.add_argument("--no-sandbox")
option.add_argument("--disable-gpu")
option.add_argument("--log-level-3")
option.add_argument("--disable-dev-shm-usage")
option.add_argument("--disable-notifications")
option.add_argument("--ignore-certificate-errors")
option.add_argument("--user-agent=" + user_agent)
option.add_argument("--disable-blink-features=AutomationControlled")

option.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chromedriver_path = os.environ.get("CHROMEDRIVER_PATH")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
}

async def createItem(userID , channelID, ProductLink, client):
    if (ProductLink.find('flipkart') != -1):
        response = requests.get(ProductLink, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        titleTag = titleTagArray[1]
        if soup.find("span", {"class": titleTag}):
            title = soup.find("span", {"class": titleTag}).get_text()
        else:
            title = "No Title Found"
        print(title.strip())
        for ptag in flipkartArray:
            if soup.find(id=ptag):
                price = soup.find(id=ptag).get_text()
                print(price)
                break
            elif soup.find("div", {"class": ptag}):
                price = soup.find("div", {"class": ptag}).get_text()
                break
            else:
                price = "0"
        print(price)
        imgTag = imgTagArray[1]
        if soup.find("img", {"class": imgTag}):
            img = soup.find("img", {"class": imgTag}).get('src')
        else:
            img = "https://i.imgur.com/vh2Cjlq.png"
        print(img)
    elif (ProductLink.find('amazon') != -1):
        browser = webdriver.Chrome(executable_path=chromedriver_path, options=option)
        browser.get(ProductLink)
        price = ""
        try:
            content = browser.page_source
            soup = BeautifulSoup(content, 'html.parser')
            price = soup.find("span", {"class": "a-offscreen"}).get_text()
        except:
            price = "0"
        if len(price) < 2:
                price = "0"
        print(price)
        title = browser.find_element_by_id("productTitle").text
        print(title)
        img = browser.find_element_by_id("landingImage").get_attribute("src")
        print(img)
        browser.quit()
    elif ProductLink.find('myntra') != -1:
        try:
            browser = webdriver.Chrome(executable_path=chromedriver_path, options=option)
            browser.get(ProductLink)
            if browser.find_element_by_class_name("pdp-price").text is not None:
                price = browser.find_element_by_class_name("pdp-price").text
            else:
                price = "0"
            if browser.find_element_by_class_name("pdp-title").text is not None or browser.find_element_by_class_name("pdp-name").text is not None:
                title = browser.find_element_by_class_name("pdp-title").text + " " + browser.find_element_by_class_name("pdp-name").text
            else:
                title = "No Title Found"
            if browser.find_element_by_class_name("image-grid-image").get_attribute("style").split('"')[1] is not None:
                img = browser.find_element_by_class_name("image-grid-image").get_attribute("style").split('"')[1]
            else:
                img = "https://i.imgur.com/vh2Cjlq.png"
            browser.quit()
        except Exception as e:
            browser.quit()
            print(e)
        browser.quit()
    elif ProductLink.find('tatacliq') != -1:
        try:
            browser = webdriver.Chrome(executable_path=chromedriver_path, options=option)
            browser.implicitly_wait(5)
            browser.get(ProductLink)
            if browser.find_element_by_class_name("ProductDetailsMainCard__productName").text is not None:
                title = browser.find_element_by_class_name("ProductDetailsMainCard__productName").text
            else:
                title = "No Title Found"
            if browser.find_element_by_class_name("ProductDetailsMainCard__price").text is not None:
                price = browser.find_element_by_class_name("ProductDetailsMainCard__price").text
            else:
                price = "0"
            if browser.find_element_by_class_name("Image__actual").get_attribute("src") is not None:
                img = browser.find_element_by_class_name("Image__actual").get_attribute("src")
            else:
                img = "https://i.imgur.com/vh2Cjlq.png"
            browser.quit()
        except Exception as e:
            browser.quit()
            print(e)
    elif ProductLink.find('hm') != -1:
        try:
            response = requests.get(ProductLink, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.find("h1", {"class": "primary product-item-headline"}).get_text()
            print(title.strip())
            price = soup.find("div", {"class": "primary-row product-item-price"}).get_text().strip()
            price = price.replace("\nPer U", "")
            img = soup.findAll("img")[1].get("src")
            img = 'https:' + img
            print(img)
        except Exception as e:
            print(e)
    return classes.Item(userID, channelID, title, price, ProductLink, img)

async def checkPrice(client, ProductLink):
    if(ProductLink.find('flipkart') != -1):
        response = requests.get(ProductLink, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        try:
            for ptag in flipkartArray:
                if soup.find("div", {"class": ptag}):
                    price = soup.find("div", {"class": ptag}).get_text()
                    break
                else:
                    price = "0"
                    continue
            return price
        except Exception as e:
            print(e)
            return "0"
    elif(ProductLink.find('amazon') != -1):
        if ProductLink.find('127.0.0.1') != -1:
            return "0"
        try:
           browser = webdriver.Chrome(executable_path=chromedriver_path, options=option)
           browser.get(ProductLink)
        except Exception as e:
           print(e)
           return "0"
        if browser.find_element_by_id('availability').text is not None:
            availability = browser.find_element_by_id('availability').get_attribute('innerHTML')
            if availability.find('Currently unavailable') != -1:
                print("Not Available")
                return "0"
        price = ""
        try:
            content = browser.page_source
            soup = BeautifulSoup(content, 'html.parser')
            price = soup.find("span", {"class": "a-offscreen"}).get_text()
        except Exception as e:
            print(e)
            price = "0"
        if len(price) < 2:
            price = "0"
        print(price)
        browser.quit()
        return price
    elif ProductLink.find('myntra') != -1:
        try:
            browser = webdriver.Chrome(executable_path=chromedriver_path, options=option)
            browser.implicitly_wait(2)
            browser.get(ProductLink)
            if browser.find_element_by_class_name("pdp-price").text is not None:
                price = browser.find_element_by_class_name("pdp-price").text
                browser.quit()
            else:
                price = "0"
            return price
        except Exception as e:
            print(e)
            browser.quit()
            return "0"
    elif ProductLink.find('tatacliq') != -1:
        if(ProductLink.find('127.0.0.1') != -1):
            return "0"
        try:
            browser = webdriver.Chrome(executable_path=chromedriver_path, options=option)
            browser.implicitly_wait(3)
            browser.get(ProductLink)
            browser.implicitly_wait(3)
            if browser.find_element_by_class_name("ProductDetailsMainCard__price").text is not None:
                price = browser.find_element_by_class_name("ProductDetailsMainCard__price").text
                browser.quit()
            else:
                price = "0"
            return price
        except Exception as e:
            browser.quit()
            print(e)
            return "0"
    elif ProductLink.find('hm') != -1:
        try:
            response = requests.get(ProductLink, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            price = soup.find("div", {"class": "primary-row product-item-price"}).get_text().strip()
            price = price.replace("\nPer U", "")
            return price
        except Exception as e:
            print(e)
            return "0"

async def sendMsg(channel, msg, file):
    await channel.send(msg, file=file)

priceTagArray = ['_30jeq3 _3yRFQ5','_30jeq3 _16Jk6d','priceblock_dealprice', 'priceblock_saleprice', 'priceblock_ourprice']
flipkartArray = ['_30jeq3 _3yRFQ5','_30jeq3 _16Jk6d']
amazonArray = ['//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[1]/span[1]', '//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]/span[2]/span[1]']
titleTagArray = ['productTitle', 'B_NuCI']
imgTagArray = ['landingImage','_396cs4 _2amPTt _3qGmMb _3exPp9']
