import argparse
import os
import sys
from os import listdir
from tqdm import tqdm
import pandas as pd

# this script merges data

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


def main(fifa_versions):

    fifa_versions = args.fifa_versions.split(',')

    for fifa in tqdm(fifa_versions):
        print("FIFA",fifa)
        df_player_ids = pd.read_csv(f"data/sport_analytics/raw/full_player_data_{fifa}.csv",index_col=0)
        df_player_ids["ID"] = df_player_ids["ID"].astype('int')
        df_attributes = pd.read_csv(f'data/sport_analytics/raw/FIFA_{fifa}.csv')  
        df_attributes["ID"] = df_attributes["ID"].astype('int')
        
        try:
            import config as CONFIG
            df_attributes = df_attributes.drop_duplicates()
            df_player_ids = df_player_ids.drop_duplicates()

            df_attributes = df_attributes.set_index('ID')
            df_player_ids = df_player_ids.set_index('ID')

            df_merge = pd.concat([df_player_ids,df_attributes],axis=1)
            df_merge = df_merge.rename(CONFIG.FEATURE_MAPPING,axis=1)
            
            drop_nas = (df_merge.drop('Club',axis=1).isna().T.sum()>0)
            if drop_nas.sum()>0:
                print("Fifa",drop_nas.sum())
                df_merge = df_merge[~drop_nas]

            df_merge.to_csv(f"data/sport_analytics/processed/FIFA{fifa}_official_data.csv")
        except:
            print('Error while merging',fifa)
            pass




if __name__ == "__main__":
    DEFAULT_FIFA_VERSIONS = "17"
    # DEFAULT_FIFA_VERSIONS = "12"
    find_and_append_module_path()
    
    parser = argparse.ArgumentParser(description="FIFA Player Data Scraper")
    parser.add_argument('--fifa_versions', default=DEFAULT_FIFA_VERSIONS, help='Comma-separated FIFA versions (default: "13")')
    # parser.add_argument('--offsets', type=int, default=DEFAULT_OFFSETS, help='Number of offsets to scrape (default: 300)')
    args = parser.parse_args()
    
    main(args.fifa_versions)
