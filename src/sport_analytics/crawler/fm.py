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
        UID = extract_id(player_id)
        age = int(player_ul.find('li', class_='age').text)
        try:
            wage = player_ul.find('li', class_='wage').text
        except:
            wage = 'None'
            pass
        rating = int(player_ul.find('li', class_='rating').span.text)

        try:
            value = str(player_ul.find('li', class_='value').text)
        except:
            value = 'None'
            pass
        # Use regular expressions to extract the ID from the URL
        
        potential_html = player_ul.find('li', class_='potential')
       
        potential, dynamic =   get_potential(potential_html) 

        positions_list = [i.text for i in player_ul.find_all('span', {'class': 'position', 'title': 'Natural'})]
        position = ', '.join(set(positions_list))
        
        player_info = {
            'Name': name,
            'Player ID': player_id,
            'UID':UID,
            'Age': age,
            'Value': value,
            'Wage':wage,
            'Rating': rating,
            'Potential': potential,
            'Dynamic_Potential':dynamic,
            'Position': position
        }
        
        # Append the player's data to the list
        players_data.append(player_info)
    
    return pd.DataFrame(players_data)


def get_potential(potential_li):

    span_element = potential_li.find('span')

    if not span_element:
        return None, None  # Return None if the <span> element is not found

    class_attribute = span_element.get('class', [])

    if 'dynamic' not in class_attribute:
        pot = int(span_element.text)

        pot_art = False
    else:
        # If 'dynamic' is not in the class, determine potential based on class names
        if 'superstar' in class_attribute:
            pot = 100
        elif 'excellent' in class_attribute:
            pot = 90
        elif 'good' in class_attribute:
            pot = 80
        elif 'decent' in class_attribute:
            pot = 70
        else:
            pot = 60
        pot_art = True

    return pot, pot_art



def extract_id(input_string):
    # Find the first "/" from the right
    last_slash_index = input_string.rfind('/')

    if last_slash_index != -1:
        # Find the first "-" after the last "/"
        first_dash_index = input_string[last_slash_index:].find('-')

        if first_dash_index != -1:
            # Extract the ID
            player_id = input_string[last_slash_index + 1:last_slash_index + first_dash_index]
            return player_id
        else:
            return None  # Dash not found after the last slash
    else:
        return None  # Last slash not found