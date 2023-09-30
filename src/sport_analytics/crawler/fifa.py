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
        name = td[1].find('div').text
        age = td[2].text
        overall = td[3].text.strip()
        potential = td[4].text.strip()
        club = td[5].find('a').text
        club_logo = td[5].find('img').get('data-src')
        value = td[6].text.strip()
        wage = td[7].text.strip()
        special = td[8].text.strip()

        # Find the <span> elements with class "pos" inside the <td> with class "col-name"
        positions = [span.text for span in row.select('td.col-name span.pos')]

        # Join the positions into a single string
        positions_str = ','.join(positions)


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


def extract_attributes(soup, id):
    block_quarters = soup.find_all('div', class_='block-quarter')

    skills = {}

    for block in block_quarters:
        try:
            category_name = block.find('h5').text.strip()
        except:
            category_name = ""

        if category_name.lower() in ['attacking', 'movement', 'skill', 'mentality', 'defending', 'goalkeeping', 'power']:
            skill_elements = block.find_all('li')
            skills_in_category = {}

            for skill_element in skill_elements:
                rating = skill_element.find('span', class_='bp3-tag').text.strip()
                skill_name = skill_element.find('span', role='tooltip').text.strip()

                skills_in_category[skill_name] = rating

            skills[category_name] = skills_in_category

    skills['ID'] = {'ID':id}
    attributes = pd.DataFrame(flatten_dict(skills))
    attributes = attributes.set_index('Attribute')

    return attributes.T

def get_fifa_soup(id,FIFA):
    url = f'https://sofifa.com/player/{str(id)}?r={FIFA}0001&set=true'
    source_code = requests.get(url, headers=headers)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    return soup