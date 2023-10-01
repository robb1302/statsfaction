import os
import sys

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
import pandas as pd
from sqlalchemy import create_engine

mapping = {
    "":"UID",
    "Name": "Name",
    "Position": "Position",
    "Age": "Age",
    "Value": "Value",
    "Wage": "Wage",
    "CA": "Rating",
    "PA": "Potential",
    "Wor": "work-rate",
    "Vis": "vision",
    "Thr": "throwing",
    "Tec": "technique",
    "Tea": "teamwork",
    "Tck": "tackling",
    "Str": "strength",
    "Sta": "stamina",
    "TRO": "rushing-out-tendency",
    "Ref": "reflexes",
    "Pun": "punching-tendency",
    "Pos": "positioning",
    "Pen": "penalty-taking",
    "Pas": "passing",
    "Pac": "pace",
    "1v1": "one-on-ones",
    "OtB": "off-the-ball",
    "Nat": "natural-fitness",
    "Mar": "marking",
    "L Th": "long-throws",
    "Lon": "long-shots",
    "Ldr": "leadership",
    "Kic": "kicking",
    "Jum": "jumping-reach",
    "Hea": "heading",
    "Han": "handling",
    "Fre": "free-kick-taking",
    "Fla": "flair",
    "Fir": "first-touch",
    "Fin": "finishing",
    "Ecc": "eccentricity",
    "Dri": "dribbling",
    "Det": "determination",
    "Dec": "decisions",
    "Cro": "crossing",
    "Cor": "corners",
    "Cnt": "concentration",
    "Cmp": "composure",
    "Com": "communication",
    "Cmd": "command-of-area",
    "Bra": "bravery",
    "Bal": "balance",
    "Ant": "anticipation",
    "Agi": "agility",
    "Agg": "aggression",
    "Aer": "aerial-reach",
    "Acc": "acceleration"
}
features = pd.Series(mapping).values
data_names = [i for i in os.listdir('data/sport_analytics/processed/') if 'FM' in i and i.endswith('.csv')]

main_df = pd.DataFrame()
for name in data_names:
    df = pd.read_csv(f'data/sport_analytics/processed/{name}')
    
    df = df.rename(columns = mapping)[features]
    df['database']=name.replace('.csv','')
    df['fm'] = int(name[3:5])
    main_df = pd.concat([df,main_df],axis=0)
    
    df.head()
main_df = main_df.reset_index(drop=True)

db_connection_str = 'sqlite:///data/sport_analytics/database/football.db'

# Create a SQLAlchemy engine
engine = create_engine(db_connection_str)


# Save the DataFrame to an SQL table
table_name = 'fm'
main_df.to_sql(table_name, con=engine, if_exists='replace', index=False)

# Close the database connection
engine.dispose()
print('database created sucessfully')