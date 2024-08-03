import pandas as pd
import numpy as np
import os
import glob
from pandas.errors import EmptyDataError, ParserError
from scipy.stats import zscore

def get_all_xlsx_files(directory):
    # find all xlsx files in the given directory
    return glob.glob(os.path.join(directory, '**/*.xlsx'), recursive=True)

def get_random_data_points(file_path):
    try:
        # Check if the file exists
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"The file '{file_path}' does not exist.")
        
      
        try:
            data = pd.read_excel(file_path)
        except EmptyDataError:
            raise ValueError("The xlsx file is empty.")
        except ParserError:
            raise ValueError("The xlsx file is invalid or corrupted.")
        
        # Check columns are present or not
        required_columns = ['Stock_ID', 'Date', 'Stock_Price']
        if not all(column in data.columns for column in required_columns):
            raise ValueError(f"The xlsx file must contain the following columns: {', '.join(required_columns)}")
        
        # Ensure the Date correct format
        try:
            data['Date'] = pd.to_datetime(data['Date'], format='%d-%m-%Y')
        except ValueError:
            raise ValueError("Date format should be '%d-%m-%Y'.")
        
        # Sort data by Date
        data = data.sort_values('Date').reset_index(drop=True)
        
    
        if len(data) < 30:
            raise ValueError("The dataset must contain at least 30 data points.")
        
       
        max_start_index = len(data) - 30
        start_index = np.random.randint(0, max_start_index + 1)
        
        # Extract 30 consecutive data points 
        selected_data = data.iloc[start_index:start_index + 30]
        
        return selected_data
    
    except FileNotFoundError as e:
        print(e)
    except ValueError as e:
        print(e)
    except EmptyDataError:
        print("The xlsx file is empty.")
    except ParserError:
        print("The xlsx file is invalid or corrupted.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def identify_outliers(data, threshold=3):
    # Calculate the Z-scores for the 'Stock_Price' column
    data['Z-Score'] = zscore(data['Stock_Price'])
    
    # Print Z-scores for debug purpose
    print("Z-Scores for data points:")
    print(data[['Stock_ID', 'Date', 'Stock_Price','Z-Score']])
    
    # Define outliers based on the threshold
    outliers = data[(data['Z-Score'] > threshold) | (data['Z-Score'] < -threshold)]
    
    if outliers.empty:
        print(f"No outliers detected with threshold of {threshold}.")
    else:
        print(f"Outliers detected with threshold of {threshold}.")
    
    return outliers

def calculate_deviations(data, threshold):
    # Calculate the mean of the 'Stock_Price' column
    mean_close = data['Stock_Price'].mean()
    
    # Calculate deviation from the mean
    data['Deviation'] = data['Stock_Price'] - mean_close
    
    # Calculate percentage deviation over the threshold
    data['Percentage Deviation'] = (np.abs(data['Deviation']) / mean_close) * 100
    data['Above Threshold'] = data['Percentage Deviation'] > threshold
    
    return mean_close, data

def process_all_xlsx_files(directory):
    xlsx_files = get_all_xlsx_files(directory)
    results = []
    
    for file_path in xlsx_files:
        print(f"\nProcessing file: {file_path}")
        random_data_points = get_random_data_points(file_path)
        if random_data_points is not None:
            print("Randomly selected data points:")
            print(random_data_points)
            
            threshold = 2  # Adjust the threshold as needed
            outliers = identify_outliers(random_data_points, threshold)
            print("\nIdentified outliers:")
            print(outliers)
            
            threshold = 5  # Define the threshold for percentage deviation
            mean_close, data_with_deviations = calculate_deviations(random_data_points, threshold)
            print(f"\nMean of the 30 data points: {mean_close}")
            print("\nData with deviations and percentage deviations:")
            print(data_with_deviations)
            
            results.append({
                'file_path': file_path,
                'random_data_points': random_data_points,
                'outliers': outliers,
                'mean_close': mean_close,
                'data_with_deviations': data_with_deviations
            })
    
    return results


directory = 'D:/LSEG/STOCK_PRICE_DATA/'  # Set this to the directory containing your xlsx files
all_results = process_all_xlsx_files(directory)
