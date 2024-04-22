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

    logger.log("Event", "Start time")

    #종목 검색
    keyword = "AFL"
    print(f"Keyword : {keyword}")
    driver_manager.get_page(f"{url}/symbol/{keyword}")
    
    #당일 주가
    price = driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[1]/div[2]/span[1]').text
    print(f"당일 주가 : {price}")
    
    #Consensus EPS Estimates
    driver_manager.get_page(f"{url}/symbol/{keyword}/earnings/estimates")
    eps_table_elements = driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[2]/div/div/section[2]/div/div[2]/div[2]/div[2]/div/table/tbody').find_elements(By.TAG_NAME, "tr")[:2]
    eps_table_info = []
    
    print("Consensus EPS Estimates")
    for eps_table_element in eps_table_elements:
        eps_info = []
        eps_info.append(eps_table_element.find_element(By.TAG_NAME, "div").text)
        eps_info_elements = eps_table_element.find_elements(By.TAG_NAME, "td")
        for eps_info_element in eps_info_elements:
            eps_info.append(eps_info_element.text)
        eps_table_info.append(eps_info)
        print(f"Fiscal Period Ending : {eps_info[0]} / EPS Estimate : {eps_info[1]} / YoY Growth : {eps_info[2]} / Forward PE : {eps_info[3]} / Low : {eps_info[4]} / High : {eps_info[5]} / # of Analysts : {eps_info[6]}")
    
    revenue_table_elements = driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[2]/div/div/section[3]/div/div[2]/div[2]/div[2]/div/table/tbody').find_elements(By.TAG_NAME, "tr")[:2]
    revenue_table_info = []
    
    print("\nRevenue Estimate")
    for revenue_table_element in revenue_table_elements:
        revenue_info = []
        revenue_info.append(revenue_table_element.find_element(By.TAG_NAME, "div").text)
        revenue_info_elements = revenue_table_element.find_elements(By.TAG_NAME, "td")
        for revenue_info_element in revenue_info_elements:
            revenue_info.append(revenue_info_element.text)
        revenue_table_info.append(revenue_info)
        print(f"Fiscal Period Ending : {revenue_info[0]} / Revenue Estimate : {revenue_info[1]} / YoY Growth : {revenue_info[2]} / Forward PE : {revenue_info[3]} / Low : {revenue_info[4]} / High : {revenue_info[5]} / # of Analysts : {revenue_info[6]}")
    
    logger.log("Event", "End time")

logger = Util.Logger("Dev")
sample_crawler(logger)

def test(logger):
    driver_manager = DriverManager.WebDriverManager(logger, False, True)
    driver = driver_manager.get_driver()

    url = "https://www.barchart.com/"

    driver_manager.get_page(url)
    Util.wait_time(logger, 60)

#test(logger)