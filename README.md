# Stock Price Outlier Detection

# This function process all the xlsx file present in the STOCK_DATA

This project includes a Python script that performs the following tasks:
1. **Extracts 30 consecutive data points** from a xlsx file containing stock prices, starting from a random timestamp within the file.
2. **Calculates the mean** of these 30 data points.
3. **Identifies outliers** in these 30 data points using Z-scores.
4. **Calculates deviations** from the mean and determines the percentage deviation over a specified threshold.

## Requirements

To run the script, you'll need the following Python libraries:
- pandas
- numpy
- scipy

# To process xlsx file you need to install module openpyxl
pip install openpyxl


# Install required libraries for  the function
Install these libraries using pip:

bash
pip install pandas numpy scipy

## To execute the python code use below command

python outliers.py

# Stock Price Outlier Detection with Docker

The Docker container ensures that the script runs consistently across different environments.

## Requirements

 Ensure Docker is installed on your machine.

## Setup

### 1. Dockerfile

The `Dockerfile` sets up the environment and dependencies needed to run the script. It uses the official Python 3.11 slim image and installs the required Python libraries.

### 2. `requirements.txt`

The `requirements.txt` file lists the Python libraries needed:
- pandas
- numpy
- scipy

## Building the Docker Image

To build the Docker image, navigate to the directory containing the `Dockerfile` and run:

```bash
docker build -t stock-price-outlier-detection .