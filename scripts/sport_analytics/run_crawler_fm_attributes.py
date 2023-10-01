import argparse
import os
import sys
from os import listdir

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


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

def main(database_version):
    main_attributes = pd.DataFrame()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }
    player_list = pd.read_csv(f"data/sport_analytics/raw/player_list_fm_{database_version}.csv",index_col=0)
    player_list = player_list.drop_duplicates()
    print("download attributes")
    for player_url in tqdm(player_list["Player ID"]):
        try:
            attributes = pd.Series()
            while len(attributes)<2:
                # Create a BeautifulSoup object
                url =  f"https://fminside.net/{player_url}"
                response = requests.get(url,headers=headers)    
                html_content = response.text
                soup = BeautifulSoup(html_content, 'html.parser')

                # Find all <tr> elements with an "id" attribute
                tr_elements = soup.find_all('tr', id=True)

                # Iterate through the <tr> elements
            
                attributes["Player ID"] = player_url
                for tr in  tr_elements:
                    attributes[tr['id']] = tr.findAll()[2].text

            main_attributes = pd.concat([pd.DataFrame(attributes),main_attributes],axis=1)
        except:
            print("Error:",player_url)
            pass
    main_attributes = main_attributes.T
    main_attributes = main_attributes.set_index("Player ID")

    merged_data =  pd.concat([player_list.set_index("Player ID"),main_attributes],axis=1)

    merged_data.to_csv(f"data/sport_analytics/processed/{database_version}.csv")
    print('done')

if __name__ == "__main__":
    # FM 23 (23.4.0)
    # FM 22 (22.1.0)
    # FM 21 (21.0.0)
    parser = argparse.ArgumentParser(description="FM Inside Web Scraper")
    parser.add_argument("--database_version", type=str, help="Database version to select, e.g., 'FM 22 (22.1.0)'",default="FM 22 (22.1.0)")
    find_and_append_module_path()

    args = parser.parse_args()
    main(args.database_version)
