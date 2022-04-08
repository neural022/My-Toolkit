# basic
import re
import time
from datetime import datetime
import random as rand

# crawler
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

class PersonInfo():
    def __init__(self, name, email, cellphone):
        self.name = name
        self.email = email
        self.cellphone = cellphone

class CoolpcGPUCrawler():
    def __init__(self, url, pattern, order_num, person_info):
        self.url = url
        self.pattern = pattern
        self.order_num = order_num
        self.person_info = person_info
        # pattern
        self.patterns = ('.*').join(p for p in pattern.split())
        self.items = dict()
        # options
        self.options = ChromeOptions()
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.options.add_argument("--start-maximized")

    def get_gpu_item(self):
        pass

    def show_item(self):
        for item_key in self.items.keys():
            print(item_key)

    def check_gpu_item(self):
        response_html = requests.get(self.url)
        soup = BeautifulSoup(response_html.text, 'html.parser')
        soup_options = soup.select_one("select[name='n12'] option")
        gpu_items = { option.text:option['value'] for option in soup_options.find_all('option') if not option.has_attr('disabled') }
        
        has_item = False
        for item_key, value in gpu_items.items():
            if re.search(self.patterns, item_key):
                self.items[item_key] = value
                has_item = True
        return has_item

    def skip_ad(self):
        # move to pixels
        action = ActionChains(self.chrome)
        action.move_by_offset(150, 150)
        action.click()
        action.perform()
        
    def select_gpu_item(self):
        select = Select(self.chrome.find_element(By.NAME, "n12"))
        select.select_by_value(list(self.items.values())[0])
    
    def select_gpu_item_num(self):
        select = Select(self.chrome.find_element(By.NAME, "u12"))
        select.select_by_value(str(self.order_num))
    
    def select_mail(self):
        buy_element = self.chrome.find_element(By.XPATH, "//img[@title='將估價結果 Email 給原價屋']")
        action = ActionChains(self.chrome)
        action.click(buy_element)
        action.perform()

    def key_in_info(self):
        sender = "<%s>" % self.person_info.name +self.person_info.mail
        cellphone = ""

    def crawling(self):
        # Check gpu item exist
        if self.check_gpu_item():
            ''' Place and order '''
            print("%s is exist" % self.pattern)
            # web driver
            self.chrome = webdriver.Chrome(options=self.options)
            self.chrome.get(self.url)
            # skip advertisement
            self.skip_ad()
            self.select_gpu_item()
            self.select_gpu_item_num()
            self.select_mail()
            # iframe = self.chrome.find_element(By.XPATH, "//iframe[@id='mycookie']")
            # self.chrome.switch_to.frame(iframe)
            # self.chrome.quit()
        else:
            print("%s is not exist" % self.pattern)

if __name__ == '__main__':
    
    rand.seed(datetime.now())
    coolpc_url = "https://www.coolpc.com.tw/evaluate.php"

    gpu_pattern = "RTX2060 12G"
    order_num = 2
    myinfo = PersonInfo('username', 'user@gmail.com', 'cellphone number')
    coolpc_crawler = CoolpcGPUCrawler(coolpc_url, gpu_pattern, order_num, myinfo)
    coolpc_crawler.crawling()
    coolpc_crawler.show_item()