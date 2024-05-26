import pandas as pd
import os
#import webbrowser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup

def main():  
    read_links_from_excel()
    df_main = scrape_links()
    df_to_excel(df_main)

def read_links_from_excel():
    global urls
    #Read urls file in /xlsx directory and add urls to list
    path = os.getcwd() + "/xlsx"
    exceldata = pd.read_excel(path + "/urls.xlsx",sheet_name = "Sheet1")
    urls = exceldata['links'].tolist()
    #print(urls)

def scrape_links():
    driver = webdriver.Chrome()
    df = pd.DataFrame(columns=['App Name', 'App URL', 'Developer Name', 'Developer URL'])

    for url in urls:
        driver.get(url)
        time.sleep(5)

        app_current_url = driver.current_url
        app_name = driver.find_element(By.XPATH, "//h1[@itemprop='name']").text
        app_dev_url = driver.find_element(By.XPATH, "//div/a[contains(@href, '/store/apps/dev')]").get_attribute("href")
        app_dev_name = driver.find_element(By.XPATH, "//div/a[contains(@href, '/store/apps/dev')]/span").text

        #print(app_name)
        #print("Currect url:" + app_current_url)     
        #print(app_dev_url)
        #print(app_dev_name)
        data = {
            'App Name': [app_name],
            'App URL': [app_current_url],
            'Developer Name': [app_dev_name],
            'Developer URL': [app_dev_url]
        }
        df1 = pd.DataFrame(data)

        df = pd.concat([df, df1])
    return df

def df_to_excel(df_main):
    df_main.to_excel(os.getcwd() + "/xlsx/output.xlsx")

main()