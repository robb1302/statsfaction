from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import numpy as np
import sys
import os
from os import listdir

pd.set_option('display.max_columns', 500)

def find_and_append_module_path():
    current_dir = os.getcwd()
    substring_to_find = 'statsfaction'
    index = current_dir.rfind(substring_to_find)
    
    if index != -1:
        # Extract the directory path up to and including the last "mypath" occurrence
        new_dir = current_dir[:index + (len(substring_to_find))]

        # Change the current working directory to the new directory
        os.chdir(new_dir)
        sys.path.append(new_dir)
        # Verify the new current directory
        print("New current directory:", os.getcwd())
    else:
        print("No 'mypath' found in the current directory")

find_and_append_module_path()

# Initialize the WebDriver (you may need to specify the path to your chromedriver executable)
driver = webdriver.Chrome()

# Navigate to the webpage
url = 'https://fminside.net/players#'
# Open the webpage
driver.get(url)

# Wait for the "Load more" button to be clickable
wait = WebDriverWait(driver, 10)
import time
for _ in range(5):  # Perform 5 clicks
    time.sleep(10)
    load_more_button = driver.find_element(By.CLASS_NAME, 'loadmore')
    driver.execute_script("arguments[0].scrollIntoView();", load_more_button)
    
    # Wait for the intercepting element to disappear
    wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, 'fc-header')))
    
    # Click the "Load more" button
    load_more_button.click()

print('Done')
# Perform any additional actions you need on the loaded content
