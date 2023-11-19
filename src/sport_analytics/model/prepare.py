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
    df_raw["overall_age_ratio"] = df_raw.Overall/(df_raw.Age**2)
    df_raw['youth_player'] = df_raw.Age<20
    
    df_raw['shooting'] = (df_raw['Finishing']+df_raw['Positioning'] +df_raw['FKAccuracy'])/3
    df_raw['shooting_technique'] = (df_raw['Finishing']+df_raw['ShotPower']+df_raw['LongShots']+df_raw['Volleys']+df_raw['FKAccuracy'] )/5
    df_raw['mental'] =    (df_raw['Penalties'] +   df_raw['Composure'])/2
    df_raw['physique'] =  (df_raw['Stamina'] + df_raw['Strength'])/2
    df_raw['Speed'] =  (df_raw['Acceleration'] + df_raw['SprintSpeed'])/2
    df_raw['ball_handling'] = (df_raw['Balance']+df_raw['Agility']+df_raw['Dribbling'] +df_raw['BallControl']*2 )/5
    
    for attribut in ['Reactions',"physique",'shooting_technique','Stamina','Positioning','Vision','Finishing','Stamina','BallControl','shooting']:
        df_raw[f'age_based_{attribut}'] = df_raw[attribut] - df_raw.groupby(['FIFA','Age'])[attribut].transform('mean')
        # df_raw[f'{attribut}'] = df_raw[attribut] - df_raw.groupby(['FIFA','Age'])[attribut].transform('mean')
   
    return df_raw