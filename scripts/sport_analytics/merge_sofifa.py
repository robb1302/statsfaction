import pandas as pd
import pandas as pd
import numpy as np
import sys
import os
from os import listdir

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

feature_mapping = {
    'ID': 'ID',
    'Crossing': 'Crossing',
    'Finishing': 'Finishing',
    'Heading accuracy': 'HeadingAccuracy',
    'Short passing': 'ShortPassing',
    'Volleys': 'Volleys',
    'Dribbling': 'Dribbling',
    'Curve': 'Curve',
    'FK Accuracy': 'FKAccuracy',
    'Long passing': 'LongPassing',
    'Ball control': 'BallControl',
    'Acceleration': 'Acceleration',
    'Sprint speed': 'SprintSpeed',
    'Agility': 'Agility',
    'Reactions': 'Reactions',
    'Balance': 'Balance',
    'Shot power': 'ShotPower',
    'Jumping': 'Jumping',
    'Stamina': 'Stamina',
    'Strength': 'Strength',
    'Long shots': 'LongShots',
    'Aggression': 'Aggression',
    'Interceptions': 'Interceptions',
    'Positioning': 'Positioning',
    'Vision': 'Vision',
    'Penalties': 'Penalties',
    'Marking': 'Marking',
    'Standing tackle': 'StandingTackle',
    'Sliding tackle': 'SlidingTackle',
    'GK Diving': 'GKDiving',
    'GK Handling': 'GKHandling',
    'GK Kicking': 'GKKicking',
    'GK Positioning': 'GKPositioning',
    'GK Reflexes': 'GKReflexes',
    'Best Position': 'Best Position',
    'Best Overall Rating': 'Best Overall Rating',
    'Release Clause': 'Release Clause',
    'DefensiveAwareness': 'DefensiveAwareness'
}


for year in ["13","14","15","16"]:
    df = pd.read_csv(f'data/sport_analytics/raw/FIFA_{year}_attributes.csv')
    df = df.T.reset_index(drop=True)
    features =  df.loc[0]
    df.columns = features
    df = df.drop(0,errors='ignore')
    df = df.set_index('ID')
    df.head()
    df_players = pd.read_csv(f"data/sport_analytics/raw/full_player_data_{year}.csv",index_col=0)
    df_players = df_players.set_index('ID')
    df_merge = pd.concat([df_players,df],axis=1)
    df_merge = df_merge.rename(feature_mapping,axis=1)
    df_merge.to_csv(f"data/sport_analytics/processed/FIFA{year}_official_data.csv")


