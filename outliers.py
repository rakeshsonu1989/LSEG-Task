import pandas as pd
import numpy as np
import os
from pandas.errors import EmptyDataError, ParserError
from scipy.stats import zscore

def get_random_data_points(file_path):
    try:
        # Check if the file exists
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"The file '{file_path}' does not exist.")
        
        # Load the data
        try:
            data = pd.read_csv(file_path)
        # Check file is empty    
        except EmptyDataError:
            raise ValueError("The CSV file is empty.")
        # Check file is invalid or corrupted
        except ParserError:
            raise ValueError("The CSV file is invalid or corrupted.")
        
        # Check if the required columns are present in the csv file
        required_columns = ['Stock-ID', 'Date', 'Stock_Price']
        if not all(column in data.columns for column in required_columns):
            raise ValueError(f"The CSV file must contain the following columns: {', '.join(required_columns)}")
        
        # Ensure the Date column is of datetime type with the correct format
        try:
            data['Date'] = pd.to_datetime(data['Date'], format='%d-%m-%Y')
        except ValueError:
            raise ValueError("Date format should be '%d-%m-%Y'.")
        
        # Sort the data by Date
        data = data.sort_values('Date').reset_index(drop=True)
        
        # Ensure there are at least 30 data points
        if len(data) < 30:
            raise ValueError("The dataset must contain at least 30 data points.")
        
        # Select a random starting index such that there are at least 29 data points after it
        max_start_index = len(data) - 30
        start_index = np.random.randint(0, max_start_index + 1)
        
        # Extract 30 consecutive data points starting from the random index
        selected_data = data.iloc[start_index:start_index + 30]
        
        return selected_data
    
    except FileNotFoundError as e:
        print(e)
    except ValueError as e:
        print(e)
    except EmptyDataError:
        print("The CSV file is empty.")
    except ParserError:
        print("The CSV file is invalid or corrupted.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# function to define outliners

def identify_outliers(data, threshold=2):
    # Calculate the Z-scores for the 'Stock_Price' column
    data['Z-Score'] = zscore(data['Stock_Price'])
    
    # Print Z-scores for debugging
    print("Z-Scores for data points:")
    print(data[['Stock-ID', 'Date', 'Stock_Price' ,'Z-Score']])
    
    # Define outliers based on the threshold
    outliers = data[(data['Z-Score'] > threshold) | (data['Z-Score'] < -threshold)]
    
    if outliers.empty:
        print(f"No outliers detected with threshold of {threshold}.")
    else:
        print(f"Outliers detected with threshold of {threshold}.")
    
    return outliers

# function to calculate deviations

def calculate_deviations(data, threshold):
    # Calculate the mean of the 'Stock_Price' column
    mean_close = data['Stock_Price'].mean()
    
    # Calculate deviation from the mean
    data['Deviation'] = data['Stock_Price'] - mean_close
    
    # Calculate percentage deviation over the threshold
    data['Percentage Deviation'] = (np.abs(data['Deviation']) / mean_close) * 100
    data['Above Threshold'] = data['Percentage Deviation'] > threshold
    
    return mean_close, data


file_path = 'D:/LSEG/LSE/FLTRLSE.CSV' # Provide path for csv file
random_data_points = get_random_data_points(file_path)
if random_data_points is not None:
    print("Randomly selected data points:")
    print(random_data_points)
    
    outliers = identify_outliers(random_data_points)
    print("\nIdentified outliers:")
    print(outliers)
    
    threshold = 2  # Define the threshold for percentage deviation
    mean_close, data_with_deviations = calculate_deviations(random_data_points, threshold)
    print(f"\nMean of the 30 data points: {mean_close}")
    print("\nData with deviations and percentage deviations:")
    print(data_with_deviations)
