import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import FirefoxOptions
import time
import pandas as pd


# 即時重大訊息
realtime_stock_news_url = "https://mops.twse.com.tw/mops/web/t05sr01_1"
# 當日重大訊息
days_stock_news_url = "https://mops.twse.com.tw/mops/web/t05st02"

def get_day_stocks_news(driver, year=112, month=10, day=18):
    # 當日大訊息
    wait = WebDriverWait(driver, 10)
    driver.get(days_stock_news_url)
    years = driver.find_element(By.ID, "year")
    years.clear()
    years.send_keys(year)
    driver.find_element(By.ID, "month").send_keys(month)
    driver.find_element(By.ID, "day").send_keys(day)
    button = driver.find_element(By.XPATH, "//input[@value=' 查詢 ']")
    button.click()
    condition = (By.XPATH, "//input[@value='詳細資料']")
    wait.until(EC.element_to_be_clickable(condition))
    # button = driver.find_element(By.XPATH, "//input[@value='詳細資料']")
    for button in driver.find_elements(By.XPATH, "//input[@value='詳細資料']"):
        time.sleep(1)
        button.click()
    time.sleep(5)


def get_realtime_stocks_news(driver):
    wait = WebDriverWait(driver, 10)
    driver.get(realtime_stock_news_url)
    original = driver.current_window_handle
    # print(original)
    dict1 = {}
    for i, button in enumerate(driver.find_elements(By.XPATH, "//input[@value='詳細資料']")):
        # time.sleep(1)
        button.click()
        wait.until(EC.presence_of_element_located((By.ID, "table01")))
        # wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        driver.switch_to.window(driver.window_handles[1])
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))
        content = driver.find_element(By.TAG_NAME, "pre")
        dict1[i] = content.text
        # print(text.text)
        entire_window = driver.find_element(By.TAG_NAME, "body")
        time.sleep(1)
        entire_window.screenshot(f"{i}.png")
        print(f"{i}.png download!")
        driver.close()
        driver.switch_to.window(original)
        time.sleep(1)
    return dict1


if __name__ == "__main__":
    options = FirefoxOptions()
    options.add_argument("--headless")
    with webdriver.Firefox(options=options) as browser_driver:  # with webdriver.Chrome() as driver:
        # get_day_stocks_news(driver, year=112, month=10, day=17)

        data = get_realtime_stocks_news(browser_driver)
        pd.DataFrame(data, index=["data"]).T.to_csv("news.csv")
