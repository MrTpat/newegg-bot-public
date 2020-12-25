from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
from chromedriver_py import binary_path
import os

def saveCookies(sel, file_name: str):
    if not os.path.exists('./cookies'):
        os.makedirs('./cookies')
    d = {}
    for c in sel.get_cookies():
        d[c['name']] = c['value']
    j = json.dumps(d)
    f = open(f'cookies/{file_name}','w')
    f.write(j)
    f.close()
    print('saved cookies!')

def initBrowser(url):
    chrome_options = Options()
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    chrome_options.add_argument('disable-gpu')
    chrome_options.add_argument('--log-level=OFF')
    browser = webdriver.Chrome(executable_path=binary_path, options=chrome_options)
    browser.get(url)
    return browser

browser = initBrowser('https://www.newegg.com')
file_name = input('Enter cookie file name to save to cookies folder: ')
input('Press key when page is done loading after you logged in: ')
saveCookies(browser, file_name)
browser.close()
