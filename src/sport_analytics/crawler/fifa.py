from pandas import DataFrame, Series
from bs4 import BeautifulSoup
import pandas as pd

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
        player_data = DataFrame([[pid, name, age, picture, nationality, flag_img, overall, 
                                potential, club, club_logo, value, wage, special]])
        player_data.columns = columns
        data = pd.concat([data, player_data], axis=0)

    data = data.drop_duplicates()
       
    return data