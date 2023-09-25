"""
This Script clicks through the fminside page and gets the player ids. After that it downloads the attributes with the IDs
"""


import argparse
import os
import sys
import time
from os import listdir

import numpy as np
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from tqdm import tqdm


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



def main(database_version="FM 23 (23.4.0)"):
    # Initialize the WebDriver (you may need to specify the path to your chromedriver executable)
    driver = webdriver.Chrome()

    # Navigate to the webpage
    url = 'https://fminside.net/players#'
    # Open the webpage
    driver.get(url)

    # Wait for the "Load more" button to be clickable
    wait = WebDriverWait(driver, 10)

    # Locate the select element for FM database version
    select_element = driver.find_element(By.NAME, 'database_version')

    # Create a Select object
    select = Select(select_element)

    # Select the specified database_version argument
    select.select_by_visible_text(database_version)

    # Wait for a short moment to allow the page to update
    time.sleep(2)

    for i in tqdm(range(400)):  # Perform 3000 clicks
        j = 0
        while True:  # Retry up to 3 times if the button is not clickable
            try:

                time.sleep(2)
                load_more_button = driver.find_element(By.CLASS_NAME, 'loadmore')
                driver.execute_script("arguments[0].scrollIntoView();", load_more_button)
                load_more_button.click()
                break  # If the click succeeds, exit the retry loop
            except Exception as e:
                j = j+1
                html_content = driver.page_source
                with open(f'temp.txt', 'w', encoding='utf-8') as file:
                    file.write(html_content)
                print(f"Retry failed: {i}")
                time.sleep(2)  # Wait for 2 seconds before retrying

    print('Parse')

    html_content = driver.page_source
    with open(f'page_source.txt', 'w', encoding='utf-8') as file:
        file.write(html_content)

    # Perform any additional actions you need on the loaded content

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }

    from src.sport_analytics.crawler.fm import download_player_id
    source_code = requests.get(url, headers=headers)
    plain_text = source_code.text
    player_list = download_player_id(html_content)
    player_list.to_csv("player_list_fm_22.csv")

    print("Shutting down")
    driver.quit()  # Don't forget to quit the driver when you're done

if __name__ == "__main__":
    # FM 23 (23.4.0)
    # FM 22 (22.1.0)
    # FM 21 (21.0.0)
    parser = argparse.ArgumentParser(description="FM Inside Web Scraper")
    parser.add_argument("--database_version", type=str, help="Database version to select, e.g., 'FM 22 (22.1.0)'",default='FM 22 (22.1.0)')
    find_and_append_module_path()

    args = parser.parse_args()
    main(args.database_version)
