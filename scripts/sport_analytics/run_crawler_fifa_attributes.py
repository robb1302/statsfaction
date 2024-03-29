"""
This Script  downloads the attributes of the Players in FIFA
there has to be a player id file first
"""

import argparse
import os
# Initial imports
import sys
import warnings

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import time
warnings.filterwarnings('ignore')


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

def main(fifa_versions):

    fifa_versions = args.fifa_versions.split(',')

    for FIFA in fifa_versions:
        data = pd.read_csv(f"data/sport_analytics/raw/full_player_data_{FIFA}.csv")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        }

        master_data = pd.DataFrame()

        for _, row in tqdm(data.iterrows(), total=data.shape[0]):
            try:
                id = row["ID"]
                counter = 0
                attributes = pd.DataFrame()
                
                while (attributes.shape[1]<=1):
                    
                    soup = get_fifa_soup(id = id,FIFA=FIFA,version="01")
                    attributes = extract_attributes(soup, id)
                    counter = counter + 1
                    
                    if counter>1:
                        # print("something went wrong")
                        time.sleep(2)

                if counter >1:
                    print(id,counter)
               
                master_data = pd.concat([attributes, master_data], axis=0)        
               
                if attributes.empty:
                    print('Failed',id)

            except:
                master_data = master_data.reset_index(drop=True)
                master_data.to_csv(f"data/sport_analytics/raw/FIFA_{FIFA}.csv")

        master_data = master_data.reset_index(drop=True)
        master_data.to_csv(f"data/sport_analytics/raw/FIFA_{FIFA}.csv")

if __name__ == "__main__":
    DEFAULT_FIFA_VERSIONS = "24"
    DEFAULT_OFFSETS = 300
    
    find_and_append_module_path()
    
    parser = argparse.ArgumentParser(description="FIFA Player Data Scraper")
    parser.add_argument('--fifa_versions', default=DEFAULT_FIFA_VERSIONS, help='Comma-separated FIFA versions (default: "13")')
    # parser.add_argument('--offsets', type=int, default=DEFAULT_OFFSETS, help='Number of offsets to scrape (default: 300)')
    args = parser.parse_args()
    
    from src.sport_analytics.crawler.fifa import extract_attributes,get_fifa_soup
    
    main(fifa_versions=args.fifa_versions)


 