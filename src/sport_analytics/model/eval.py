import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.preprocessing import StandardScaler
import shap
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import mlflow 
import os 
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


def plot_correlation_heatmap(df):
    # Calculate the correlation matrix
    corr_matrix = df.corr()

    # Create a custom color map that smoothly transitions from dark green to gray
    cmap = sns.diverging_palette(600, 150, as_cmap=True)

    # Create a heatmap using Seaborn with the custom color map
    plt.figure(figsize=(20, 16))
    sns.set(font_scale=1.2)
    sns.heatmap(corr_matrix, cmap=cmap, annot=False, linewidths=0.1, square=True, cbar=True)

    # Set the plot title
    plt.title("Correlation Heatmap")

    # Show the plot
    plt.show()

def plot_feature_importance(model, title=None, top_n=20):
    # Extract feature importances from the model
    if hasattr(model, 'feature_importances_'):
        feature_importances = model.feature_importances_
    elif hasattr(model,'coef_'):
        feature_importances = abs(pd.Series(model.coef_))
    else:
        raise ValueError("Model does not have feature importances.")

    if hasattr(model, 'feature_names_in_'):
        feature_names = model.feature_names_in_
    elif hasattr(model,'feature_name_'):
        feature_names = model.feature_name_
    else:
        raise ValueError("Model does not have feature names.")

    # Create a DataFrame for feature importances
    feature_importance_df = pd.DataFrame()
    feature_importance_df["value"] = feature_importances/feature_importances.sum()
    feature_importance_df["names"] = feature_names
    feature_importance_df = feature_importance_df.sort_values(by="value", ascending=False)

    # Select the top N most important features
    top_features = feature_importance_df.iloc[:top_n, :]

    # Create a stylish horizontal bar plot with a black background and white fonts
    plt.figure(figsize=(10, 8), facecolor='black')
    colors = ['#808080', '#008080', '#6b8e23', '#F8766D', '#7CAE00', '#00BFC4', '#C77CFF', '#F564E3', '#FFB900', '#00D1FF']

    # Specify the font family (e.g., 'Arial', 'Times New Roman', 'Courier New', etc.)
    plt.rcParams['font.family'] = 'Times New Roman'

    plt.barh(top_features["names"], top_features["value"], color=colors[1])
    plt.xlabel('Feature Importance', fontsize=12, color='white')  # Set text color to white
    plt.ylabel('Features', fontsize=12, color='white')  # Set text color to white
    if title:
        plt.title(title, fontsize=16, fontweight='bold', color='white')  # Bold and bigger title
    plt.gca().invert_yaxis()  # Invert y-axis for better readability

    # Add a white grid with specified color
    plt.grid(axis='x', linestyle='--', alpha=0.3, color='white')  # Add a white grid to the x-axis

    plt.gca().spines['top'].set_visible(False)  # Hide the top border
    plt.gca().spines['right'].set_visible(False)  # Hide the right border
    plt.gca().spines['bottom'].set_color('white')  # Set x-axis border color to white
    plt.gca().spines['left'].set_color('white')  # Set y-axis border color to white
    plt.grid(axis='x', linestyle='--', alpha=0.6, color='black')
    # Set color and fontweight of x-axis labels to white and bold
    plt.xticks(fontsize=10, fontweight='bold', color='white',)

    # Set color of y-axis ticks to white
    plt.tick_params(axis='y', colors='white')
    # Save the plot in memory using BytesIO
    # Save the plot as a local file
    plot_filename = "feature_importance_plot.png"
    plt.savefig(plot_filename)
    
    # Log the local file as an artifact
    mlflow.log_figure(figure=plt.gcf(), artifact_file="feature_importance_plot.png")
    # Delete the local file
    os.remove(plot_filename)

    plt.show()
    return list(top_features['names'].values)


def individual_shap_valuess(values, attributes,player_index):
    import pandas as pd
    from sklearn.preprocessing import MinMaxScaler

    shaps = pd.DataFrame(values,columns=attributes,index = player_index)
    # Initialize the MinMaxScaler
    scaler = StandardScaler()

    # Fit and transform the DataFrame using the scaler
    shaps = pd.DataFrame(scaler.fit_transform(shaps), columns=attributes,index=player_index).round(3)
    shaps["summe_shap"] = shaps.T.sum()
    return shaps

def get_shap_plot_indv(skills,explainer):
    print(skills.index.values)
    shap_skills = explainer.shap_values(skills)
    if len(shap_skills)!=1:
        shap_skills = shap_skills[1]
    shap_indv = np.round(shap_skills,2)[0]
    if not type(explainer.expected_value) == np.float32:
        base_line = explainer.expected_value[1]
    else:
        base_line = explainer.expected_value
    shap.plots.force(base_line, shap_indv, skills, matplotlib = True)
    return pd.DataFrame(shap_indv,index=skills.columns,columns=["shap"])





def create_polar_plot(data_series, positive_color= '#5a7b6c', negative_color='#e34234'):
    fig = plt.figure(figsize=(8, 6))
    fig.patch.set_facecolor('black')  # Set background to black
    ax = fig.add_subplot(111, projection="polar")
    font_color = "white"
    # Custom styles
    ax.set_facecolor('black')  # Set clean black background

    # Theta values
    theta = np.arange(len(data_series)) / float(len(data_series)) * 2 * np.pi

    # Values (absolute values)
    values = np.abs(data_series.values)

    # Define a color map based on positive/negative values
    colors = [positive_color if value >= 0 else negative_color for value in data_series]

    # Draw bars for each angle with no edges
    ax.bar(theta, values, width=0.4, alpha=1, color=colors, align='center')

    # Set tick labels
    plt.xticks(theta, data_series.index, color=font_color, size=12, rotation=45)  # Rotate tick labels

    # Set title and axis labels
    plt.title("Skill Impact", fontsize=16, fontweight='bold', color=font_color)
    ax.set_yticklabels([])  # Remove radial tick labels

    # Add polar grid with light and white gridlines
    ax.grid(False, color='white', linestyle='--', linewidth=0.1, alpha=0.7)

    # Show the plot
    plt.show()


import shap
import scikitplot as skplt
import mlflow
def plot_auc_curves(y_true,y_proba):
    skplt.metrics.plot_roc(y_true, y_proba)
    
    # Save the plot as a local file
    roc_plot_filename = "roc_curve_plot.png"
    plt.savefig(roc_plot_filename)
    
    # Log the local file as an artifact
    mlflow.log_figure(figure=plt.gcf(), artifact_file="roc_curve_plot.png")
    # Delete the local file
    os.remove(roc_plot_filename)
    plt.show()


def plot_shap_summary(model,df):
    try:
        explainer = shap.Explainer(model)
    except:
        explainer = shap.KernelExplainer(model.predict, df)
    shap_values = explainer.shap_values(df)
    # manche Modelle liefern shap values zu positiven und negativen Prediction
    if len(shap_values)==2:
        shap_values = shap_values[1]
    # Create SHAP summary plot
    shap.summary_plot(shap_values, df,show=False)
    
    # Save the SHAP summary plot as a local file
    shap_plot_filename = "shap_summary_plot.png"
    plt.savefig(shap_plot_filename)
    

    
    # Log the local file as an artifact
    mlflow.log_figure(figure=plt.gcf(), artifact_file="shap_summary_plot.png")
    # Show the plot before logging it
    plt.show()
    # Delete the local file
    os.remove(shap_plot_filename)

def plot_shap_summary_regression(model,df):
    explainer = shap.KernelExplainer(model=model,data=df)
    shap_values = explainer.shap_values(df,nsamples = 10)
    # manche Modelle liefern shap values zu positiven und negativen Prediction
    if len(shap_values)==2:
        shap_values = shap_values[1]
    # Create SHAP summary plot
    shap.summary_plot(shap_values, df,show=False)
    
    # Save the SHAP summary plot as a local file
    shap_plot_filename = "shap_summary_plot.png"
    plt.savefig(shap_plot_filename)
    

    
    # Log the local file as an artifact
    mlflow.log_figure(figure=plt.gcf(), artifact_file="shap_summary_plot.png")
    # Show the plot before logging it
    plt.show()
    # Delete the local file
    os.remove(shap_plot_filename)

import mlflow
import pandas as pd
from sklearn.metrics import (
    roc_auc_score,
    precision_recall_curve,
    auc,
    accuracy_score,
    precision_recall_fscore_support
)

def log_metrics_in_mlflow(y_test,y_prob,y_pred):

    # Assuming y_test and y_pred are defined
    precision_array, recall_array, thresholds = precision_recall_curve(y_test, y_pred)
    area_under_curve_pr = auc(recall_array, precision_array)
    
    if y_prob is not None:
        roc_auc = roc_auc_score(y_test, y_prob)
    else:
        roc_auc = None

    accuracy = accuracy_score(y_test, y_pred)
    # Calculate macro and micro scores
    precision_macro, recall_macro, f1_macro, _ = precision_recall_fscore_support(y_test, y_pred, average='macro')
    precision_micro, recall_micro, f1_micro, _ = precision_recall_fscore_support(y_test, y_pred, average='micro')

    # Calculate precision, recall, and F1 for both positive and negative classes
    precision_pos, recall_pos, f1_pos, _ = precision_recall_fscore_support(y_test, y_pred, labels=[1], average='binary')
    precision_neg, recall_neg, f1_neg, _ = precision_recall_fscore_support(~y_test, y_pred<1, labels=[1], average='binary')

    # Create a dictionary with metrics and their values
    metrics_to_log = {
        "Accuracy": accuracy,
        "AUC": roc_auc,
        "PR_AUC": area_under_curve_pr,
        "Precision_Macro": precision_macro,
        "Recall_Macro": recall_macro,
        "F1_Macro": f1_macro,
        "Precision_Micro": precision_micro,
        "Recall_Micro": recall_micro,
        "F1_Micro": f1_micro,
        "Precision_Positive": precision_pos,
        "Recall_Positive": recall_pos,
        "F1_Positive": f1_pos,
        "Precision_Negative": precision_neg,
        "Recall_Negative": recall_neg,
        "F1_Negative": f1_neg,
    }

    # Log metrics using log_metrics
    mlflow.log_metrics(metrics_to_log)


def log_feature_list_as_artifact(features, filename="feature_list.txt"):
    try:
        # Convert the list to a string
        features_str = "\n".join(map(str, features))

        # Save the string to a text file
        with open(filename, 'w') as file:
            file.write(features_str)

        # Log the text file as an artifact
        mlflow.log_artifact(filename, artifact_path="artifacts")

    finally:
        # Delete the local file, whether an exception occurs or not
        os.remove(filename)


def log_metrics_in_mlflow_regression(y_test, y_pred):
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    # Create a dictionary with metrics and their values
    metrics_to_log = {
        "Mean Squared Error": mse,
        "Mean Absolute Error": mae,
        "R2 Score": r2,
    }

    # Log metrics using log_metrics
    mlflow.log_metrics(metrics_to_log)
