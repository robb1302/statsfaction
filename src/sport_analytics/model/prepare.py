import pandas as pd

def add_features_raw_datadf_raw(df_raw):
    df_raw = df_raw.set_index(['ID','Name','FIFA'])
    best_pos = lambda x: x.split(',')[0]

    # Apply the lambda function to add best position
    df_raw["best_position"] = df_raw['Position'].apply(best_pos)
    df_raw["best_position"].value_counts()
    encoded_pos = pd.read_csv("src/sport_analytics/utils/position_mapping.csv")
    df_raw = pd.merge(df_raw.reset_index(), encoded_pos, left_on='best_position', right_on='best_position', how='inner')
    df_raw = df_raw.set_index(['ID','Name','FIFA'])
    df_raw['Defense'] =  df_raw['Defensive awareness'].fillna(0)+df_raw['Marking'].fillna(0)
    return df_raw