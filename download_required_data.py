''' this code downloads delivery data of today. it is assumed to be working on windows
so, downloaded file goes to downloaded. It then renames this file and move it to
our target folder for further processing'''

import pandas as pd
import numpy as np
import shutil
import os
import time
import random
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def create_dir():
    directory = str(pd.to_datetime('today').date())
    try:
        os.stat(directory)
    except:
        os.mkdir(directory)
    return directory


def getfiles(dir_path):
    options = webdriver.ChromeOptions()
    #options.headless = True
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    

    URL = 'https://www.nseindia.com/all-reports'
    driver.get(URL)
    WebDriverWait(driver,10000).until(EC.visibility_of_element_located((By.TAG_NAME,'body')))
    print(driver.current_url)
    date_today = pd.to_datetime('today').date()
    dt = '{:02d}'.format(date_today.day)
    mnt = '{:02d}'.format(date_today.month)
    yr = str(date_today.year)
    filename = 'https://archives.nseindia.com/products/content/sec_bhavdata_full_'+dt+mnt+yr+'.csv'
    driver.get(filename)
    print('download complete')
    time.sleep(3)

    source = r'C:\Users\ashishsh\Downloads\sec_bhavdata_full_'+dt+mnt+yr+'.csv'
    destination = r'C:\Users\ashishsh\Desktop\Python\test11\sec_bhavdata_full_'+dt+mnt+yr+'.csv'
    shutil.move(source,destination)
    
    driver.quit()


def main():
    dir_path = create_dir()
    getfiles(dir_path)

if __name__ == "__main__":
    main()
