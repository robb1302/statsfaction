from pandas import DataFrame, Series
from bs4 import BeautifulSoup
import pandas as pd
import requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}
def download_player_id(html_content,columns=None):
    data = DataFrame()    
    soup = BeautifulSoup(html_content, 'html.parser')
    table_body = soup.find('tbody')
    for row in table_body.findAll('tr'):
        td = row.findAll('td')
        picture = td[0].find('img').get('data-src')
        pid = td[0].find('img').get('id')
        nationality =  td[1].find('img', class_='flag')['title']
        flag_img = td[1].find('img').get('data-src')
        name = td[1].find('a').text
        age = td[2].text
        overall_str = td[3].find('em').text
        overall = int(''.join(filter(str.isdigit, overall_str)))
        potential = td[4].text.strip()
        club = td[5].find('a').text
        club_logo = td[5].find('img').get('data-src')
        value = td[6].text.strip()
        wage = td[7].text.strip()
        special = td[8].text.strip()

        # Join the positions into a single string
        positions_str = td[1].find('div').text


        player_data = DataFrame([[pid, name, age, picture, nationality, flag_img, overall, 
                                potential, club, club_logo, value, wage, special,positions_str]])
        player_data.columns = columns
        data = pd.concat([data, player_data], axis=0)

    data = data.drop_duplicates()
       
    return data

def flatten_dict(data):

    flat_data = []
    for category, attributes in data.items():
        for attribute, value in attributes.items():
            flat_data.append({'Attribute': attribute, 'Value': value})
    return flat_data


def get_ratings(html_text, skill_names):
    """
    Extracts ratings for the given skill names from the provided HTML.

    Parameters:
    - html_text: str, the HTML code
    - skill_names: list, a list of skill names

    Returns:
    - A dictionary with skill names as keys and their corresponding ratings as values.
    """
    skill_elements = html_text.find_all('span', {'data-tippy-content': True})
    
    skills_dict = {}

    for skill_element in skill_elements:
        rating = int(skill_element.find_previous('em')['title'])
        skill_name = skill_element.text.strip()

        if skill_name in skill_names:
            skills_dict[skill_name] = rating

    return skills_dict


def extract_attributes(soup, id):

    extended_skill_names = [
        'Crossing', 'Finishing', 'Heading accuracy', 'Short passing', 'Volleys',
        'Dribbling', 'Curve', 'FK Accuracy', 'Long passing', 'Ball control',
        'Acceleration', 'Sprint speed', 'Agility', 'Reactions', 'Balance',
        'Shot power', 'Jumping', 'Stamina', 'Strength', 'Long shots', 'Aggression',
        'Interceptions', 'Positioning', 'Att. Position','Vision', 'Penalties', 'Composure',
        'Defensive awareness', 'Standing tackle', 'Sliding tackle',
        'GK Diving', 'GK Handling', 'GK Kicking', 'GK Positioning', 'GK Reflexes'
    ]
    skills = get_ratings(soup, extended_skill_names)
    skills['ID'] = id
    return pd.DataFrame(pd.Series(skills)).T

def get_fifa_soup(id,FIFA,version="01"):
    url = f'https://sofifa.com/player/{str(id)}?r={FIFA}00{version}&set=true'
    source_code = requests.get(url, headers=headers)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    return soup