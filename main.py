import pandas as pd
import os
import webbrowser

def main():
    read_excel_links()
    open_urls()

def read_excel_links():
    global urls
    #Read urls file in /xlsx directory and add urls to list
    path = os.getcwd() + "/xlsx"
    exceldata = pd.read_excel(path + "/urls.xlsx",sheet_name = "Sheet1")
    urls = exceldata['links'].tolist()
    #print(urls)

def open_urls():
    browser = webbrowser.get('chrome')
    for url in urls:
        browser.open(url)

main()