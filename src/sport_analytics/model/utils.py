import pickle

def save_dict_as_pickle(data_dict, file_path):
    """
    Save a dictionary as a pickle file.

    Parameters:
    - data_dict (dict): The dictionary to be saved.
    - file_path (str): The path to the pickle file.

    Returns:
    - None
    """
    with open(file_path, 'wb') as file:
        pickle.dump(data_dict, file)