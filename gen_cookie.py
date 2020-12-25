from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
from chromedriver_py import binary_path
import os
from newegg import logger


app_logger = logger.Logger()


def saveCookies(sel, file_name: str):
    try:
        if not os.path.exists("./cookies"):
            os.makedirs("./cookies")
        d = {}
        for c in sel.get_cookies():
            d[c["name"]] = c["value"]
        j = json.dumps(d)
        f = open(f"cookies/{file_name}", "w")
        f.write(j)
        f.close()
        app_logger.log_success(f"Saved cookies in {file_name}!")
    except Exception as e:
        app_logger.handle_err(e)


def initBrowser(url):
    chrome_options = Options()
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
    chrome_options.add_argument("disable-gpu")
    chrome_options.add_argument("--log-level=OFF")
    browser = webdriver.Chrome(executable_path=binary_path, options=chrome_options)
    browser.get(url)
    return browser


browser = initBrowser("https://www.newegg.com")
app_logger.log_important("Enter cookie file name to save to cookies folder:")
file_name = input()
app_logger.log_important("Press key when page is done loading after you logged in:")
input()
saveCookies(browser, file_name)
browser.close()
