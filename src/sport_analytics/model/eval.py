import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.preprocessing import StandardScaler
import shap
import numpy as np


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

def plot_feature_importance(model, title=None, top_n=10):
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
    shap_indv = np.round(explainer.shap_values(skills)[1],2)[0]
    base_line = explainer.expected_value[1]
    shap.plots.force(base_line, shap_indv, skills, matplotlib = True)