import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time

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

def scrape_links():
    try:
        driver = webdriver.Chrome()
        df = pd.DataFrame(columns=['App Name', 'App URL', 'Developer Name', 'Developer URL'])

        for url in urls:
            try:
                driver.get(url)
                time.sleep(5)
                #TODO handling exceptions for every element
                app_current_url = driver.current_url
                app_name = driver.find_element(By.XPATH, "//*[@itemprop='name']").text
                app_dev_url = driver.find_element(By.XPATH, "//div/a[contains(@href, '/store/apps/dev')]").get_attribute("href")
                app_dev_name = driver.find_element(By.XPATH, "//div/a[contains(@href, '/store/apps/dev')]/span").text

                data = {
                    'App Name': [app_name],
                    'App URL': [app_current_url],
                    'Developer Name': [app_dev_name],
                    'Developer URL': [app_dev_url]
                }
                df1 = pd.DataFrame(data)

                df = pd.concat([df, df1])
            except NoSuchElementException as e:
                print("Element not found:", e)
                #fill in empty values so that output row count would stay the same as initial xlsx.
                app_name = "EMPTY"
                app_dev_url = "EMPTY"
                app_dev_name = "EMPTY"

                data = {
                    'App Name': [app_name],
                    'App URL': [app_current_url],
                    'Developer Name': [app_dev_name],
                    'Developer URL': [app_dev_url]
                }
                df1 = pd.DataFrame(data)

                df = pd.concat([df, df1])
    finally:
        driver.quit()
    return df

def df_to_excel(df_main):
    df_main.to_excel(os.getcwd() + "/xlsx/output.xlsx")

main()