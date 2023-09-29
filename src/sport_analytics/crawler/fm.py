import requests
from bs4 import BeautifulSoup
import pandas as pd 
from tqdm import tqdm

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

def download_player_id(html_content):
    print('read content...')
    soup = BeautifulSoup(html_content, 'html.parser')
    print('find players...')
    player_container = soup.find('div', class_='players')
    
    # Find all player elements within the container
    player_ul_elements = player_container.find_all('ul', class_='player')
    
    # Initialize a list to store player data
    players_data = []
    print('extract attributes...')    
    # Loop through each player <ul> element and extract the desired information
    for player_ul in tqdm(player_ul_elements):
        # Extract player data here
        # Modify the code to extract name, ID, age, rating, and potential
        
        name = player_ul.find('span', class_='name').a.get('title')
        player_id = player_ul.find('span', class_='name').a.get('href')
        age = int(player_ul.find('li', class_='age').text)
        rating = int(player_ul.find('li', class_='rating').span.text)
        potential_text = player_ul.find('li', class_='potential').span.text 
        if potential_text  == "":
            potential = 100
        else:
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

