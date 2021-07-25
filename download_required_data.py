''' this code downloads delivery data of today. it is assumed to be working on windows
so, downloaded file goes to downloaded. It then renames this file and move it to
our target folder for further processing'''

import sys
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
    n = len(sys.argv)
    date_value = str(pd.to_datetime('today').date())
    if n > 1:
        date_arg = sys.argv[1]
        if date_arg == "-date":
           date_value = sys.argv[2]   ### "2021-07-25"

    try:
        os.stat(date_value)
    except:
        os.mkdir(date_value)
    return date_value


def getfiles(date_value):
    options = webdriver.ChromeOptions()
    #options.headless = True
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    date_today = date_value.split('-')
    yr = date_today[0]
    mnt = date_today[1]
    dt = date_today[2]
    
    filename = 'https://archives.nseindia.com/products/content/sec_bhavdata_full_'+dt+mnt+yr+'.csv'
    driver.get(filename)
    print('download complete')
    time.sleep(3)

    status = 0
    source = r'C:\Users\ashishsh\Downloads\sec_bhavdata_full_'+dt+mnt+yr+'.csv'
    if os.path.isfile(source):    
        destination = r'C:\Users\ashishsh\Desktop\delivery_analysis'+'\\'+date_value+'\sec_bhavdata_full.csv'
        shutil.move(source,destination)
        status = 1
    else:
        status = 0
    driver.quit()
    return status
    
