# import urllib.request
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from selenium import webdriver
import time
# from selenium.webdriver.common.keys import Keys

class scrapShopee():
    
    def scrap(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized") 
        phones = []
        for j in range(0,11):
            url = f'https://shopee.co.id/search?facet=1211&keyword=iphone%20x&noCorrection=true&page={j}'
            
            driver = webdriver.Chrome(chrome_options=options)
            driver.get(url)
            time.sleep(3)
            for i in range(1,7):
                driver.execute_script(f"window.scrollTo(0, window.scrollY + {i*160})")
                time.sleep(3)
            res = driver.execute_script("return document.documentElement.outerHTML")                        
            soup    = bs(res, 'html.parser')            
            
            datas = soup.find_all('div',class_='col-xs-2-4 shopee-search-item-result__item')              
            for data in datas :  
                try :      
                    phone_img = data.find('img').attrs['src']
                except : phone_img =''             
                try : phone_title = data.find('div',class_='_1NoI8_ _16BAGk').get_text()
                except : phone_title =''
                try : phone_sales = data.find('div',class_='_18SLBt').get_text()
                except : phone_sales = ''
                try : store_loc = data.find('div',class_='_3amru2').get_text()
                except : store_loc = ''
                try : phone_price = data.find('span',class_='_341bF0').get_text()
                except : phone_price =''
                phone_detail = {
                    'image' : phone_img,
                    'title' : phone_title,
                    'price' : phone_price,
                    'sales' : phone_sales
                    }                
                phones.append(phone_detail)
            driver.quit()
        df = pd.DataFrame(phones)
        df.to_csv('shopee_iphone_selenium.csv',sep=',')
if __name__ == '__main__':
    shopee = scrapShopee()
    shopee.scrap()