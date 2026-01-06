import csv
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By

URL = "https://ks-giftcode.centurygame.com/"
GIFT_CODE = input("enter giftcode: ").strip()

script_folder = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_folder, "UID.csv")

with open(csv_path, 'r', encoding='utf-8') as f:
    PLAYER_IDS = [row[0].strip() for row in csv.reader(f) if row and row[0].strip()]

driver = webdriver.Chrome()

for player_id in PLAYER_IDS:
    try:
        driver.get(URL)
        time.sleep(1)
        driver.find_element(By.XPATH, "//input[@placeholder='Player ID']").send_keys(player_id)
        time.sleep(1)
        driver.find_element(By.XPATH, "//div[contains(@class, 'login_btn')]").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "//input[@placeholder='Enter Gift Code']").send_keys(GIFT_CODE)
        time.sleep(1)
        driver.find_element(By.XPATH, "//div[contains(@class, 'exchange_btn')]").click()
        time.sleep(1)
        
        if 'success' in driver.page_source.lower():
            print(f"{player_id}: OK")
        else:
            print(f"{player_id}: FAIL")
            
    except Exception:
        print(f"{player_id}: ERROR")
    
    time.sleep(1)

driver.quit()
print("Done!")