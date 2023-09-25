"""
This Script  downloads the standard data of the Players in FIFA
"""


import warnings
warnings.filterwarnings('ignore')

def find_and_append_module_path():
    import os
    import sys
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


from src.sport_analytics.crawler.fifa import download_player_id
import argparse
import requests
import pandas as pd
from tqdm import tqdm
from pandas import DataFrame

# Define default values
DEFAULT_FIFA_VERSIONS = "23,24"
DEFAULT_OFFSETS = 300

# Define the base URL and headers
base_url = "https://sofifa.com/players?offset="
fifa_id_columns = ['ID', 'Name', 'Age', 'Photo', 'Nationality', 'Flag', 'Overall', 'Potential', 'Club',
                   'Club Logo', 'Value', 'Wage', 'Special']
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}


def main():
    # Create an argument parser
    parser = argparse.ArgumentParser(description="FIFA Player Data Scraper")
    
    # Define command-line arguments with default values
    parser.add_argument('--fifa_versions', default=DEFAULT_FIFA_VERSIONS, help='Comma-separated FIFA versions (default: "23,24")')
    parser.add_argument('--offsets', type=int, default=DEFAULT_OFFSETS, help='Number of offsets to scrape (default: 300)')
    
    # Parse the command-line arguments
    args = parser.parse_args()
    
    # Split the comma-separated FIFA versions into a list
    fifa_versions = args.fifa_versions.split(',')
    
    # Iterate through FIFA versions
    for FIFA in fifa_versions:
        data = DataFrame(columns=fifa_id_columns)

        for offset in tqdm(range(args.offsets)):
            url = base_url + str(offset*80)+f"&r={FIFA}0001&set=true"
            source_code = requests.get(url, headers=headers)
            plain_text = source_code.text

            player_data = download_player_id(html_content=plain_text, columns=fifa_id_columns)
            data = pd.concat([data, player_data], axis=0)
            offset+=1
        data = data.drop_duplicates()
        data.to_csv(f'full_player_data_{FIFA}.csv', encoding='utf-8')

    print("Done")

if __name__ == "__main__":
    main()
