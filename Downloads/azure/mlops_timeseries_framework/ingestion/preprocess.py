import os
from mlops_timeseries_framework.ingestion.ingest import read_data
import pandas as pd
from mlops_timeseries_framework.utils.helpers import get_root_dir, read_config,get_storage_output_path
# from pyspark.dbutils import DBUtils



def drop_duplicate_data(dataframe: pd.DataFrame):
    """
    Check for and drop duplicate data in a DataFrame.

    This function identifies and removes duplicate rows in the given DataFrame. It prints
    the number of rows dropped due to duplication.

    Args:
        dataframe (pd.DataFrame): The input DataFrame to be checked for duplicates.

    Returns:
        pd.DataFrame: The DataFrame after removing duplicate rows.

    Example:
        data = drop_duplicate_data(dataframe)
        print(data)
    """
    orignal_row = dataframe.shape[0]
    dataframe.drop_duplicates(inplace=True)
    current_row = dataframe.shape[0]

    if current_row == orignal_row:
        print("No duplicates data found. Number of rows: {}".format(current_row))
    else:
        print("Duplicates data found and number of rows dropped: {}".format(orignal_row - current_row))

    return dataframe

def preprocess(config):
    """
    Preprocess time series data for the dashboard.

    This function reads the time series data from the specified file path in the configuration,
    converts the date column to datetime format, and drops the 'Unnamed: 0' column.

    Args:
        config (dict): The configuration dictionary containing file paths.

    Example:
        preprocess_dashboard_data_time(config)
    """
    path = get_root_dir()
    root_dir = os.path.dirname(path)
    datasets_time_series = read_data(f"{config['input_data']['file_path']}")
    modified_data = datasets_time_series
    modified_data["date"] = pd.to_datetime(modified_data["date"])
    modified_data.drop(["Unnamed: 0"], inplace=True, axis=1)

def main_ingestion(config=None):
    """
    Main ingestion function to preprocess and save data.

    This function reads the configuration, loads the data, removes duplicates, preprocesses the
    time series data for the dashboard, and saves the preprocessed data to MLflow and CSV files.

    Args:
        config (dict, optional): The configuration dictionary. If not provided, it will be read from 'config.yml'.

    Example:
        main_ingestion()
    """
    # reading input data
    datasets = read_data(f"{config['input_data']['file_path']}")
    data = drop_duplicate_data(dataframe=datasets)
    preprocess(config)

    # save preprocessed data 
    storage_output_path=get_storage_output_path()
    data.to_csv(f"/{storage_output_path}/{config['output_data']['preprocessed']}")     


if __name__ == "__main__":
    config = read_config()
    main_ingestion(config)
