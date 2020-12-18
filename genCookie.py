from selenium import webdriver
import pickle
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import json
import time
import requests
from urllib.parse import urlparse, parse_qs
import colors
from chromedriver_py import binary_path

def saveCookies(sel):
    d = {}
    for c in sel.get_cookies():
        d[c['name']] = c['value']
    j = json.dumps(d)
    f = open("cookies.json","w")
    f.write(j)
    f.close()
    colors.printSuccess('saved cookies!')

def initBrowser(url):
    chrome_options = Options()
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    chrome_options.use_chromium = True  
    chrome_options.add_argument('disable-gpu')
    chrome_options.add_argument('--log-level=OFF')
    browser = webdriver.Chrome(executable_path=binary_path, options=chrome_options)
    browser.get(url)
    return browser

TEST = "https://www.newegg.com/microsoft-flight-simulator-premium-deluxe-edition-windows-10/p/N82E16832350816"
browser = initBrowser(TEST)
while True:
    input('Press key when done: ')
    saveCookies(browser)
