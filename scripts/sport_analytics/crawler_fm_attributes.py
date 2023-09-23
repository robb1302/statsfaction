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

import requests
from bs4 import BeautifulSoup

def read_html_from_file(file_path):
    try:
        # Open the file in read mode
        with open(file_path, 'r', encoding='utf-8') as file:
            # Read the contents of the file
            html_content = file.read()
        return html_content
    except Exception as e:
        # Handle exceptions, such as file not found or permission issues
        print(f"Error: {str(e)}")
        return None

def download_fm_player_list(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    player_container = soup.find('div', class_='players')
    
    # Find all player elements within the container
    player_ul_elements = player_container.find_all('ul', class_='player')
    
    # Initialize a list to store player data
    players_data = []
    
    # Loop through each player <ul> element and extract the desired information
    for player_ul in player_ul_elements:
        # Extract player data here
        # Modify the code to extract name, ID, age, rating, and potential
        
        name = player_ul.find('span', class_='name').a.get('title')
        player_id = player_ul.find('span', class_='name').a.get('href')
        age = int(player_ul.find('li', class_='age').text)
        rating = int(player_ul.find('li', class_='rating').span.text)
        potential = int(player_ul.find('li', class_='potential').span.text)
        positions_list = [i.text for i in player_ul.find_all('span', {'class': 'position', 'title': 'Natural'})]
        position = ', '.join(set(positions_list))
        
        player_info = {
            'Name': name,
            'Player ID': player_id,
            'Age': age,
            'Rating': rating,
            'Potential': potential,
            'Position': position
        }
        
        # Append the player's data to the list
        players_data.append(player_info)
    
    return pd.DataFrame(players_data)


file_path = 'experiements/fifa/test_fm.txt'  # Replace with the path to your .txt file containing HTML
html_content = read_html_from_file(file_path)

# Check if the request was successful

# Parse the HTML content of the page
file_path = 'experiements/fifa/test_fm.txt'  # Replace with the path to your .txt file containing HTML
html_content = read_html_from_file(file_path)
player_list = download_fm_player_list(html_content)


player_list.to_csv("player_list_fm.csv")

from tqdm import tqdm
main_attributes = pd.DataFrame()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}

print("download attributes")
for player_url in tqdm(player_list["Player ID"]):

    # Create a BeautifulSoup object
    url =  f"https://fminside.net/{player_url}"
    response = requests.get(url,headers=headers)    
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all <tr> elements with an "id" attribute
    tr_elements = soup.find_all('tr', id=True)

    # Iterate through the <tr> elements
    attributes = pd.Series()
    attributes["Player ID"] = player_url
    for tr in  tr_elements:
        attributes[tr['id']] = tr.findAll()[2].text

    main_attributes = pd.concat([pd.DataFrame(attributes),main_attributes],axis=1)

main_attributes = main_attributes.T
main_attributes = main_attributes.set_index("Player ID")


pd.concat([player_list.set_index("Player ID"),main_attributes],axis=1).to_csv('fm_attributes.csv')
print('done')