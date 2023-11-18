import pandas as pd
import json

def load_and_organize_data(file_path):
    """
    Load cryptocurrency data from a JSON file and organize it into a pandas DataFrame.

    Parameters:
    file_path (str): The path to the JSON file containing the data.

    Returns:
    pd.DataFrame: A pandas DataFrame with the organized data.
    """
    try:
        # Load the JSON data
        with open(file_path, 'r') as file:
            data = json.load(file)
        

        # Convert the data into a pandas DataFrame
        df = pd.DataFrame(data)
        
        # Convert the index to datetime for easier handling of dates
        df.index = pd.to_datetime(df.index)
        
        return df
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

