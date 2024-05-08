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
<<<<<<< Updated upstream
from fake_useragent import UserAgent
=======
import time
import os
>>>>>>> Stashed changes

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

        stock_codes = []
        for i in range(0, len(code_list), 2):
            stock_codes.append(code_list[i])
            
        self.logger.log(log_level="Event", log_msg=f"다음과 같은 종목 코드를 총 {len(stock_codes)}개 입력 받았습니다! \n{stock_codes}")
        self.logger.log(log_level="Event", log_msg=f"크롤링 예상 소요 시간은 총 {len(stock_codes)}분 입니다!")
        return stock_codes

    def data_init(self):
        self.data.clear()
        self.data["CODE"] = list()
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
        self.data["CODE"].append(stock_data.code)
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

    def get_stock_data(self, keyword, retry=5):
        url = "https://seekingalpha.com"
        
        #종목 검색
        #print(f"Keyword : {keyword}")
        
        # #무조건 대기시간 60초로 설정해야함
        self.driver_manager.get_page(f"{url}/symbol/{keyword}/earnings/estimates", 60)
        
        if not self.driver_manager.is_element_exist(By.XPATH, '//*[@id="content"]/div[2]/div[1]/div[1]/div/h1'):
            self.logger.log(log_level="Event", log_msg=f"종목 코드가 잘못되었습니다. {keyword}는 수동으로 엑셀에 입력해주세요.")
            dummy_data = StockData(code=keyword, day_price="", eps_period="", eps_estimate="", eps_growth="", eps_forward_pe="", eps_low="", eps_high="", eps_analysts="",
                            revenue_period="", revenue_estimate="", revenue_growth="", revenue_fwd="", revenue_low="", revenue_high="", revenue_analysts="")
            dummy_datas = [dummy_data, dummy_data]
            return dummy_datas, False
            
        max_retry = 5
        retry = 0
        
        while(not(retry == max_retry)):
            if self.driver_manager.is_element_exist(By.XPATH, '//*[@id="content"]/div[2]/div[2]/div/div/section[2]/div/div[2]/div[2]/div[2]/div/table/tbody') and self.driver_manager.is_element_exist(By.XPATH, '//*[@id="content"]/div[2]/div[2]/div/div/section[3]/div/div[2]/div[2]/div[2]/div/table/tbody'):
                break
            else:
                self.logger.log(log_level="Event", log_msg=f"페이지를 다시 로드합니다.")
                self.driver.find_element(By.XPATH, '//*[@id="Earnings Estimates"]/a').click()
                Util.wait_time(logger=self.logger, wait_time=60)
                retry += 1
        
        if not (self.driver_manager.is_element_exist(By.XPATH, '//*[@id="content"]/div[2]/div[2]/div/div/section[2]/div/div[2]/div[2]/div[2]/div/table/tbody') and self.driver_manager.is_element_exist(By.XPATH, '//*[@id="content"]/div[2]/div[2]/div/div/section[3]/div/div[2]/div[2]/div[2]/div/table/tbody')):
            self.logger.log(log_level="Event", log_msg=f"종목 정보 페이지 로드에 실패하여 {keyword} 종목을 건너 뜁니다. 이 종목은 나중에 다시 시도하거나 수동으로 엑셀에 입력해주세요.")
            dummy_data = StockData(code=keyword, day_price="", eps_period="", eps_estimate="", eps_growth="", eps_forward_pe="", eps_low="", eps_high="", eps_analysts="",
                            revenue_period="", revenue_estimate="", revenue_growth="", revenue_fwd="", revenue_low="", revenue_high="", revenue_analysts="")
            dummy_datas = [dummy_data, dummy_data]
            return dummy_datas, False
        
        if not self.driver_manager.is_element_exist(By.XPATH, '//*[@id="content"]/div[2]/div[1]/div[2]/span[1]'):
            self.logger.log(log_level="Event", log_msg=f"사용자가 차단 당했습니다. 브라우저를 열어 페이지의 파란 버튼을 꾹 눌러 차단을 해제해주세요.")
            self.logger.log(log_level="Event", log_msg=f"브라우저를 열어 페이지의 파란 버튼을 꾹 눌러도 차단이 해제되지않으면 몇 시간후 다시 시도 혹은 다른 컴퓨터로 시도해주세요.")
            enter = input("차단이 해제되었다면 엔터키를 누르시면 프로그램이 계속 실행됩니다.")
            enter = input("차단이 해제되었다면 1을 입력후 엔터, 차단이 해제되지 않았다면 2를 입력 후 엔터키를 눌러주세요!")
            if enter == 1:
                self.logger.log(log_level="Event", log_msg=f"프로그램을 계속 실행합니다.")
            elif enter == 2:
                raise Exception("사용자가 차단 당했습니다. 몇 시간후 다시 시도 혹은 다른 컴퓨터로 시도해주세요.")
            else:
                raise Exception("1 혹은 2가 아닌 다른 입력입니다. 프로그램을 종료합니다.")
        price = self.driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[1]/div[2]/span[1]').text[1:]
        
        #print(f"당일 주가 : {price}")
        
        dummy_data = StockData(code=keyword, day_price="", eps_period="", eps_estimate="", eps_growth="", eps_forward_pe="", eps_low="", eps_high="", eps_analysts="",
                            revenue_period="", revenue_estimate="", revenue_growth="", revenue_fwd="", revenue_low="", revenue_high="", revenue_analysts="")
                
        eps_table_elements = self.driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[2]/div/div/section[2]/div/div[2]/div[2]/div[2]/div/table/tbody').find_elements(By.TAG_NAME, "tr")
        eps_table_info = []
        
        if len(eps_table_elements) >= 2:
            eps_table_elements = eps_table_elements[:2]
        
        #print("Consensus EPS Estimates")
        for eps_table_element in eps_table_elements:
            eps_info = []
            eps_info.append(eps_table_element.find_element(By.TAG_NAME, "div").text)
            eps_info_elements = eps_table_element.find_elements(By.TAG_NAME, "td")
            for eps_info_element in eps_info_elements:
                eps_info.append(eps_info_element.text)
            eps_table_info.append(eps_info)
            #print(f"Fiscal Period Ending : {eps_info[0]} / EPS Estimate : {eps_info[1]} / YoY Growth : {eps_info[2]} / Forward PE : {eps_info[3]} / Low : {eps_info[4]} / High : {eps_info[5]} / # of Analysts : {eps_info[6]}")
        
        revenue_table_elements = self.driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[2]/div/div/section[3]/div/div[2]/div[2]/div[2]/div/table/tbody').find_elements(By.TAG_NAME, "tr")
        if len(revenue_table_elements) >= 2:
            revenue_table_elements = revenue_table_elements[:2]
        revenue_table_info = []
        
        #print("\nRevenue Estimate")
        for revenue_table_element in revenue_table_elements:
            revenue_info = []
            revenue_info.append(revenue_table_element.find_element(By.TAG_NAME, "div").text)
            revenue_info_elements = revenue_table_element.find_elements(By.TAG_NAME, "td")
            for revenue_info_element in revenue_info_elements:
                revenue_info.append(revenue_info_element.text)
            revenue_table_info.append(revenue_info)
            #print(f"Fiscal Period Ending : {revenue_info[0]} / Revenue Estimate : {revenue_info[1]} / YoY Growth : {revenue_info[2]} / Forward PE : {revenue_info[3]} / Low : {revenue_info[4]} / High : {revenue_info[5]} / # of Analysts : {revenue_info[6]}")
        
        stock_datas = []
        stock_data = StockData(code=keyword, day_price=price, eps_period=eps_table_info[0][0], eps_estimate=eps_table_info[0][1], eps_growth=eps_table_info[0][2], eps_forward_pe=eps_table_info[0][3], eps_low=eps_table_info[0][4], eps_high=eps_table_info[0][5], eps_analysts=eps_table_info[0][6],
                                revenue_period=revenue_table_info[0][0], revenue_estimate=revenue_table_info[0][1], revenue_growth=revenue_table_info[0][2], revenue_fwd=revenue_table_info[0][3], revenue_low=revenue_table_info[0][4], revenue_high=revenue_table_info[0][5], revenue_analysts=revenue_table_info[0][6])
        stock_datas.append(stock_data)
        
        if len(eps_table_elements) >= 2:
            stock_data = StockData(code=keyword, day_price=price, eps_period=eps_table_info[1][0], eps_estimate=eps_table_info[1][1], eps_growth=eps_table_info[1][2], eps_forward_pe=eps_table_info[1][3], eps_low=eps_table_info[1][4], eps_high=eps_table_info[1][5], eps_analysts=eps_table_info[1][6],
                                    revenue_period=revenue_table_info[1][0], revenue_estimate=revenue_table_info[1][1], revenue_growth=revenue_table_info[1][2], revenue_fwd=revenue_table_info[1][3], revenue_low=revenue_table_info[1][4], revenue_high=revenue_table_info[1][5], revenue_analysts=revenue_table_info[1][6])
            stock_datas.append(stock_data)
        else:
            stock_datas.append(dummy_data)
        return stock_datas, True
    
    def start_crawling(self):
        now = datetime.datetime.now()
        year = f"{now.year}"
        month = "%02d" % now.month
        day = "%02d" % now.day
        output_name = f"{year+month+day}_SeekingAlpha"
        
        self.file_manager.creat_dir(f"./output/{output_name}")
        
        stock_codes = self.get_init_settings_from_file()
<<<<<<< Updated upstream
=======
        stock_codes = stock_codes * 16
>>>>>>> Stashed changes
        
        cnt = 1
        stock_total = len(stock_codes)
        incomplete_stock = []
        for stock_code in stock_codes:
            self.logger.log(log_level="Event", log_msg=f"진행 상황 : {cnt}/{stock_total}")
            self.logger.log(log_level="Event", log_msg=f"현재 크롤링 중인 종목 코드 : {stock_code}")
            stock_datas, is_found= self.get_stock_data(stock_code)
            self.add_product_to_data(stock_datas[0])
            self.add_product_to_data(stock_datas[1])
            self.save_csv_datas(output_name)
            if is_found:
                cnt += 1
            else:
                incomplete_stock.append(stock_code)
        cnt -= 1
        self.logger.log(log_level="Event", log_msg=f"총 {cnt}개의 종목 정보 크롤링을 완료했습니다!")
        if cnt != stock_total:
            self.logger.log(log_level="Event", log_msg=f"{incomplete_stock} 종목 정보 크롤링을 실패하였습니다. 이 종목 정보는 수동으로 엑셀에 입력해주세요.")