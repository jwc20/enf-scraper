import requests
from bs4 import BeautifulSoup as bs4
import csv
import sys

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from time import sleep

url = "https://www.catchtable.net/shop/eggandflour/review?type=DINING_GLOBAL"
driver = webdriver.Chrome()
running = True

while running:
    driver.get(url)

    scroll_down_inf(2)
    running = False


def scrape():
    response = requests.get(url)
    if response.status_code == 200:
        soup = bs4(response.content, "html.parser")
        print(soup)


def scroll_down_inf(scroll_delay):
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        new_height = driver.execute_script("return document.body.scrollHeight")
        sleep(scroll_delay)

        if new_height == last_height:
            break
        last_height = new_height

    for remaining in range(scroll_delay, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write("{:2d} seconds remaining.".format(remaining))
        sys.stdout.flush()
        sleep(1)
    sys.stdout.write("\rComplete!                       \n")


if __name__ == "__main__":
    scrape()
