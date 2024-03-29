import pandas as pd
import os

from sqlalchemy import create_engine
fifa_files = [i for i in os.listdir('data/sport_analytics/processed') if i.endswith('official_data.csv')]
dataframes = []
# Loop through the file paths and load each file into a DataFrame
for file_path in fifa_files:
    dataframe = pd.read_csv(f"data/sport_analytics/processed/{file_path}")
    dataframe['FIFA'] = int(file_path.replace('FIFA','').replace('_official_data.csv',''))+2000
    dataframes.append(dataframe)

# Combine all DataFrames into one
combined_df = pd.concat(dataframes, ignore_index=True,axis=0)
combined_df = combined_df.drop_duplicates()
db_connection_str = 'sqlite:///data/sport_analytics/database/football.db'

# Create a SQLAlchemy engine
engine = create_engine(db_connection_str)


# Save the DataFrame to an SQL table
table_name = 'fifa'
combined_df.to_sql(table_name, con=engine, if_exists='replace', index=False)

# Close the database connection
engine.dispose()
print('database created sucessfully')