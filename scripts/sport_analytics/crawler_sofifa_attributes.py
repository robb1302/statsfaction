# Initial imports
import random
import urllib.request
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import seaborn as sns
from bs4 import BeautifulSoup
from pandas import DataFrame, Series
from scipy import stats
from tqdm import tqdm

warnings.filterwarnings('ignore')

FIFA = '13'
data = pd.read_csv(f"full_player_data_{FIFA}.csv")
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}

def flatten_dict(data):

    flat_data = []
    for category, attributes in data.items():
        for attribute, value in attributes.items():
            flat_data.append({'Attribute': attribute, 'Value': value})
    return flat_data


master_data = pd.DataFrame()
# player_data_url = f'https://sofifa.com/player/{ID}?r={FIFA}0001&set=true'
for index, row in tqdm(data.iterrows(), total=data.shape[0]):
    try:
        skill_names = []
        skill_map = {'ID' : str(row['ID'])}
        # url = player_data_url + str(row['ID'])
        url = f'https://sofifa.com/player/{str(row["ID"])}?r={FIFA}0001&set=true'

        source_code = requests.get(url,headers=headers)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text)

        # Find all elements with the class "block-quarter"

        block_quarters = soup.find_all('div', class_='block-quarter')

        # Initialize a dictionary to store skills
        skills = {}

        # Loop through each "block-quarter" section
        for block in block_quarters:
            # Get the category name (e.g., 'Attacking', 'Movement', etc.)
            try:
                category_name = block.find('h5').text.strip()
            except:
                category_name = ""

            # Check if the category name is 'Attacking' or 'Movement'
            if category_name.lower() in ['attacking', 'movement','skill','mentality','defending','goalkeeping','power']:
                # Find all skill elements within the block
                skill_elements = block.find_all('li')

                # Initialize a dictionary to store the skills within the category
                skills_in_category = {}

                # Loop through each skill element
                for skill_element in skill_elements:
                    # Extract skill name and rating
                    rating = skill_element.find('span', class_='bp3-tag').text.strip()
                    skill_name = skill_element.find('span', role='tooltip').text.strip()

                    # Add the skill to the dictionary
                    skills_in_category[skill_name] = rating

                # Add the category and its skills to the main skills dictionary
                skills[category_name] = skills_in_category

        skills['ID']={'ID':row['ID']}
        attributes = pd.DataFrame(flatten_dict(skills))
        attributes = attributes.set_index('Attribute')
        
        # Print the extracted skills
        master_data = pd.concat([attributes,master_data],axis=1)
    except:
        master_data.to_csv(f"FIFA_{FIFA}_attributes.csv")


# You can also save the skills to a file or further process them as needed


master_data.to_csv(f"FIFA_{FIFA}_attributes.csv")
    