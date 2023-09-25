"""
deprecated
This Script  downloads the ID and standard data of the Players in FIFA
"""
# Initial imports
import numpy as np
import pandas as pd 
from pandas import DataFrame, Series
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

import random
import urllib.request
import requests
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings('ignore')


base_url = "https://sofifa.com/players?offset="
offset = 0
columns = ['ID', 'Name', 'Age', 'Photo', 'Nationality', 'Flag', 'Overall', 'Potential', 'Club', 
           'Club Logo', 'Value', 'Wage', 'Special']
FIFA = "16"

for FIFA in ["16"]:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    }
    from tqdm import tqdm


    data = DataFrame(columns=columns)
    for offset in tqdm(range(300)):
        url = base_url + str(offset*80)+f"&r={FIFA}0001&set=true"
        source_code = requests.get(url,headers=headers)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, 'html.parser')
        table_body = soup.find('tbody')
        for row in table_body.findAll('tr'):
            td = row.findAll('td')
            picture = td[0].find('img').get('data-src')
            pid = td[0].find('img').get('id')
            nationality =  td[1].find('img', class_='flag')['title']
            flag_img = td[1].find('img').get('data-src')
            name = td[1].find('div').text
            age = td[2].text
            overall = td[3].text.strip()
            potential = td[4].text.strip()
            club = td[5].find('a').text
            club_logo = td[5].find('img').get('data-src')
            value = td[6].text.strip()
            wage = td[7].text.strip()
            special = td[8].text.strip()
            player_data = DataFrame([[pid, name, age, picture, nationality, flag_img, overall, 
                                    potential, club, club_logo, value, wage, special]])
            player_data.columns = columns
            data = pd.concat([data,player_data],axis=0)
        offset+=1
        if (offset % 20 == 0):
            print(offset)

    data = data.drop_duplicates()
    data.to_csv(f'full_player_data_{FIFA}.csv', encoding='utf-8')

print("Done")