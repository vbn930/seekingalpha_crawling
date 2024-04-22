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
from bs4 import BeautifulSoup
import requests
import pyperclip
from fake_useragent import UserAgent
import random
import pyautogui as pg
from PIL import ImageGrab
from functools import partial
import cv2
import numpy as np
from io import BytesIO
from PIL import Image
import time
import os

@dataclass
class StockData:
    code: str
    day_price: str
    eps_period: str
    eps_estimate: str
    eps_growth: str
    eps_forward_pe: str
    eps_low: str
    eps_high: str
    eps_analysts: str
    revenue_period: str
    revenue_estimate: str
    revenue_growth: str
    revenue_fwd: str
    revenue_low: str
    revenue_high: str
    revenue_analysts: str

class SeekingAlpha_Crawler:
    def __init__(self, logger):
        self.file_manager = FileManager.FileManager()
        self.logger = logger
        self.driver_manager = DriverManager.WebDriverManager(self.logger, is_headless=False, is_use_udc=True)
        self.driver = self.driver_manager.driver
        self.file_manager.creat_dir("./output")
        self.data = dict()
        self.data_init()

    def get_init_settings_from_file(self):
        data = pd.read_csv("./setting.csv").fillna(0)
        
        code_list = data["CODE"].to_list()

        start_code = data["start_code"].to_list()
        start_code.append(0)
        start_code = start_code[0:start_code.index(0)]
        stock_codes = []
        for i in range(0, len(code_list), 2):
            stock_codes.append(code_list[i])
        
        if len(start_code) != 0:
            stock_codes = stock_codes[stock_codes.index(start_code[0]):]
        
        print(stock_codes)
        return stock_codes

    def data_init(self):
        self.data.clear()
        self.data["EPS Fiscal Period Ending"] = list()
        self.data["EPS Estimate"] = list()
        self.data["EPS YoY Growth"] = list()
        self.data["Forward PE"] = list()
        self.data["EPS Low"] = list()
        self.data["EPS High"] = list()
        self.data["EPS # of Analysts"] = list()
        self.data["Revenue Fiscal Period Ending"] = list()
        self.data["Revenue Estimate"] = list()
        self.data["Revenue YoY Growth"] = list()
        self.data["Revenue FWD Price/Sales"] = list()
        self.data["Revenue Low"] = list()
        self.data["Revenue High"] = list()
        self.data["Revenue # of Analysts"] = list()
        self.data["당일 주가"] = list()
    
    def add_product_to_data(self, stock_data: StockData):
        for i in range(2):
            self.data["EPS Fiscal Period Ending"].append(stock_data.eps_period)
            self.data["EPS Estimate"].append(stock_data.eps_estimate)
            self.data["EPS YoY Growth"].append(stock_data.eps_growth)
            self.data["Forward PE"].append(stock_data.eps_forward_pe)
            self.data["EPS Low"].append(stock_data.eps_low)
            self.data["EPS High"].append(stock_data.eps_high)
            self.data["EPS # of Analysts"].append(stock_data.eps_analysts)
            self.data["Revenue Fiscal Period Ending"].append(stock_data.revenue_period)
            self.data["Revenue Estimate"].append(stock_data.revenue_estimate)
            self.data["Revenue YoY Growth"].append(stock_data.revenue_growth)
            self.data["Revenue FWD Price/Sales"].append(stock_data.revenue_fwd)
            self.data["Revenue Low"].append(stock_data.revenue_low)
            self.data["Revenue High"].append(stock_data.revenue_high)
            self.data["Revenue # of Analysts"].append(stock_data.revenue_analysts)
            self.data["당일 주가"].append(stock_data.day_price)
        

    def save_csv_datas(self, output_name):
        data_frame = pd.DataFrame(self.data)
        data_frame.to_excel(f"./output/{output_name}/{output_name}.xlsx", index=False)
        return

    def get_stock_data(self, keyword):
        url = "https://seekingalpha.com"
        
        #종목 검색
        print(f"Keyword : {keyword}")
        
        # #무조건 대기시간 30초로 설정해야함
        self.driver_manager.get_page(f"{url}/symbol/{keyword}/earnings/estimates", 60)
        
        
        price = self.driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[1]/div[2]/span[1]').text
        
        print(f"당일 주가 : {price}")
        
        eps_table_elements = self.driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[2]/div/div/section[2]/div/div[2]/div[2]/div[2]/div/table/tbody').find_elements(By.TAG_NAME, "tr")[:2]
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
        
        revenue_table_elements = self.driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[2]/div/div/section[3]/div/div[2]/div[2]/div[2]/div/table/tbody').find_elements(By.TAG_NAME, "tr")[:2]
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
        
        stock_data = StockData(code=keyword, day_price=price, eps_period=eps_info[0], eps_estimate=eps_info[1], eps_growth=eps_info[2], eps_forward_pe=eps_info[3], eps_low=eps_info[4], eps_high=eps_info[5], eps_analysts=eps_info[6],
                                revenue_period=revenue_info[0], revenue_estimate=revenue_info[1], revenue_growth=revenue_info[2], revenue_fwd=revenue_info[3], revenue_low=revenue_info[4], revenue_high=revenue_info[5], revenue_analysts=revenue_info[6])
        return stock_data
    
    def start_crawling(self):
        now = datetime.datetime.now()
        year = f"{now.year}"
        month = "%02d" % now.month
        day = "%02d" % now.day
        output_name = f"{year+month+day}_SeekingAlpha"
        
        self.file_manager.creat_dir(f"./output/{output_name}")
        
        stock_codes = self.get_init_settings_from_file()
        # stock_codes = stock_codes * 16
        
        cnt = 1
        stock_total = len(stock_codes)
        for stock_code in stock_codes:
            self.logger.log(log_level="Event", log_msg=f"진행 상황 : {cnt}/{stock_total}")
            self.logger.log(log_level="Event", log_msg=f"현재 크롤링 중인 종목 코드 : {stock_code}")
            stock_data = self.get_stock_data(stock_code)
            self.add_product_to_data(stock_data)
            self.save_csv_datas(output_name)
            cnt += 1