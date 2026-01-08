import csv
import time
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

URL = "https://ks-giftcode.centurygame.com/"
GIFT_CODE = input("enter giftcode: ").strip()

script_folder = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_folder, "UID.csv")

with open(csv_path, 'r', encoding='utf-8') as f:
    PLAYER_IDS = [row[0].strip() for row in csv.reader(f) if row and row[0].strip()]

chrome_options = Options()
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
chrome_options.add_argument('--log-level=3')
chrome_options.add_argument('--disable-features=GCM')
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
driver = webdriver.Chrome(options=chrome_options)

total = len(PLAYER_IDS)
success_count = 0
fail_count = 0
error_count = 0

print(f"\nTotal accounts to process: {total}")
print("-" * 50)

start_time = time.time()

for idx, player_id in enumerate(PLAYER_IDS, 1):
    elapsed = time.time() - start_time
    avg_time = elapsed / idx if idx > 0 else 0
    eta_seconds = avg_time * (total - idx)
    eta_minutes = int(eta_seconds // 60)
    eta_seconds_rem = int(eta_seconds % 60)
    status = f"{idx:3d}/{total} | ETA: {eta_minutes:02d}:{eta_seconds_rem:02d} | ✓:{success_count:2d} ✗:{fail_count:2d} ⚠:{error_count:2d}"
    sys.stdout.write("\r" + " " * 80 + "\r")
    sys.stdout.write(status)
    sys.stdout.flush()
    
    try:
        driver.get(URL)
        time.sleep(0.8)
        driver.find_element(By.XPATH, "//input[@placeholder='Player ID']").send_keys(player_id)
        time.sleep(0.8)
        driver.find_element(By.XPATH, "//div[contains(@class, 'login_btn')]").click()
        time.sleep(1.5)
        driver.find_element(By.XPATH, "//input[@placeholder='Enter Gift Code']").send_keys(GIFT_CODE)
        time.sleep(0.8)
        driver.find_element(By.XPATH, "//div[contains(@class, 'exchange_btn')]").click()
        time.sleep(1.5)
        
        msg_element = driver.find_element(By.CSS_SELECTOR, ".msg")
        msg_text = msg_element.text.strip()

        if 'redeemed' in msg_text.lower():
            success_count += 1
            result_symbol = "✓"
        else:
            fail_count += 1
            result_symbol = "✗"
            
    except Exception as e:
        error_count += 1
        result_symbol = "⚠"
    
    result_display = f"{idx:3d}/{total} | ETA: {eta_minutes:02d}:{eta_seconds_rem:02d} | ✓:{success_count:2d} ✗:{fail_count:2d} ⚠:{error_count:2d} | {player_id}: {result_symbol}"
    sys.stdout.write("\r" + " " * 80 + "\r")
    sys.stdout.write(result_display)
    sys.stdout.flush()
    time.sleep(0.5)
    sys.stdout.write("\r" + " " * 80 + "\r")
    sys.stdout.write(status)
    sys.stdout.flush()

total_elapsed = time.time() - start_time
total_minutes = int(total_elapsed // 60)
total_seconds = int(total_elapsed % 60)

sys.stdout.write("\r" + " " * 80 + "\r")
sys.stdout.flush()

print("\n" + "=" * 50)
print("PROCESSING COMPLETE!")
print("=" * 50)
print(f"Total Processed: {total}")
print(f"Successful: {success_count}")
print(f"Failed: {fail_count}")
print(f"Errors: {error_count}")
if total > 0:
    success_rate = (success_count/total*100)
    print(f"Success Rate: {success_rate:.1f}%")
print(f"Total Time: {total_minutes:02d}:{total_seconds:02d}")
print(f"Average Time/Account: {(total_elapsed/total):.1f}s")
print("-" * 50)

driver.quit()
print("Done!")