from Utility import Util
from Manager import DriverManager
from Utility import LoginModule
from Manager import FileManager

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from dataclasses import dataclass
import pandas as pd
import datetime

def sample_crawler(logger):
    driver_manager = DriverManager.WebDriverManager(logger, False, True)
    driver = driver_manager.get_driver()

    url = "https://seekingalpha.com/"

    driver_manager.get_page(url)

    #종목 검색
    keyword = "AFL"
    input_element = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div/header/div[1]/div[1]/div/div/div/input')
    input_element.send_keys(keyword)
    input_element.send_keys("\n")
    Util.wait_time(logger, 60)

logger = Util.Logger("Dev")
sample_crawler(logger)