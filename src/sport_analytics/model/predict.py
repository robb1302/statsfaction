from src.sport_analytics.model.prepare import add_features_raw_datadf_raw
import shap
import pandas as pd
import numpy as np

def predict_and_explain_players(df_raw,attributes,model,scaler):
    
    df_raw = add_features_raw_datadf_raw(df_raw)

    # transform raw_data
    matrix_scaled = scaler.transform(df_raw[attributes].fillna(0))
    df_scaled = pd.DataFrame(matrix_scaled, index=df_raw.index, columns=attributes)

    # player_skills['offense']  = 2
    explainer = shap.Explainer(model)
    shap_values = explainer.shap_values(df_scaled)
    shap.summary_plot(shap_values[1], df_scaled)

    # Explain Prediction
    from src.sport_analytics.model.eval import individual_shap_valuess
    shaps = individual_shap_valuess(values = shap_values[1], attributes = attributes,player_index = df_scaled.index)

    prospects = pd.DataFrame(model.predict_proba(df_scaled)[:,1],columns=["prediction"],index=df_scaled.index)
    return shaps.join(prospects).sort_values('prediction',ascending=False)


def analyze_individual_ID(ID,df_raw,attributes,model,scaler):
    
    df_raw = df_raw[df_raw['ID'] == ID]
    df_raw = add_features_raw_datadf_raw(df_raw)
    
    explainer = shap.Explainer(model)
    X_scaled = scaler.transform(df_raw[attributes].fillna(0))
    X_scaled_df = pd.DataFrame(X_scaled, index=df_raw.index, columns=attributes)

    player_skills = np.round(X_scaled_df[X_scaled_df.index.get_level_values('ID')==ID],3)
    # player_skills['offense']  = 2
    pred = model.predict_proba(player_skills)[0][1]
    print("pred",pred)
    from src.sport_analytics.model.eval import get_shap_plot_indv


    get_shap_plot_indv(skills = player_skills,explainer=explainer)
    print(df_raw.loc[player_skills.index.values[0]][attributes].T)

