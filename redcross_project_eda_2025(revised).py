# -*- coding: utf-8 -*-
"""Redcross Project EDA 2025(revised).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Vd_cmL7wfl3GqjrfIjpaKPUt8KzODENu
"""

#code snippet 0
#setting url
url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQzBYWDif8AqH47QpdaMsxZ0d3aXafgvL6EfnsUk6iN5QPCgrhvEky7hzI16iyfL3L2rfec3QX32JQj/pub?gid=0&single=true&output=csv'

#code snippet 1
#importing pandas and reading the data from url
import pandas as pd
df = pd.read_csv(url)
df

#code snippet 2
#displaying columns to better understand the dataset
df.columns

#code snippet 3
#showing data types of each column

df.dtypes

#code snippet 4
#identifying missing data
import missingno as msno
msno.bar(df)

#code snippet 5
# Libraries to help with reading and manipulating data
import numpy as np
import random
import requests
from io import StringIO

#Code snippet 6
# Setting Zip as integer to remove decimal then converting it to string with 5 places
df2 = df[df['DonorPostalCode'].notna()]

#Code snippet 7
# Setting Zip as integer to remove decimal then converting it to string with 5 places
df2['DonorPostalCode'] = df2['DonorPostalCode'].astype('int').astype(str).str.zfill(5)

#Code snippet 8
#installing zipcodes to map postal code to specific regions
!pip install zipcodes

#Code snippet 9
#importing zipcodes and mapping postal codes to States and Cities
import zipcodes

# Iterate through the zip column in df2
for index, row in df2.iterrows():
    zipcode = row["DonorPostalCode"]

    # Get zipcode details
    zipcode_data = zipcodes.matching(zipcode)

    # Extract state and city if found
    if zipcode_data:
        state = zipcode_data[0]['state']
        city = zipcode_data[0]['city']
    else:
        state = "None"
        city = "None"

    df2.loc[index, "STATE"] = state
    df2.loc[index, "CITY"] = city # Adding city information as well

# Code snippet 10
# Showing the remapped regions
df2[['DonorPostalCode','CITY', 'STATE']]

# prompt: use df2 as the dataset and CITY, STATE, DonorPostalCode as the column - show Donorpostalcode where city or state value is none

# Display DonorPostalCode where CITY or STATE is None
result = df2[(df2['CITY'] == 'None') | (df2['STATE'] == 'None')] [['DonorPostalCode','CITY']]
result

#code snippet 11
# prompt: for columns 'LastFiscalYearDonation', 'Donation2FiscalYearsAgo','Donation3FiscalYearsAgo','Donation4FiscalYearsAgo','Donation5FiscalYearsAgo','CurrentFiscalYearDonation', drop the decimal point, and the $ in front

columns_to_clean = ['LastFiscalYearDonation', 'Donation2FiscalYearsAgo',
                   'Donation3FiscalYearsAgo', 'Donation4FiscalYearsAgo',
                   'Donation5FiscalYearsAgo', 'CurrentFiscalYearDonation']

for column in columns_to_clean:
  df2[column] = df2[column].str.replace('$', '', regex=False)
  df2[column] = df2[column].str.replace('.00', '', regex=False)
  df2[column] = pd.to_numeric(df2[column], errors='coerce')
  df2[column] = df2[column].fillna(0).astype(int)
df2

#code snippet 12
# prompt: for column CumulativeDonationAmount, drop the decimal point

df2['CumulativeDonationAmount'] = df2['CumulativeDonationAmount'].astype(str).str.replace('.', '')

#code snippet 13
#showing unique values for wealth rating
df2['WealthRating'].unique()

#code snippet 14
# prompt: for column 'WealthRating', map 1 for '$1-$24,999', 2 for '$25,000-$49,999', 3 for $50,000-$99,999, 4 for $100,000-$249,999, 5 for $250,000-$499,999, 6 for $500,000-$999,999, 7 for $1,000,000-$2,499,999, 8 for $2,500,000-$4,999,999

# Create a mapping dictionary for WealthRating
wealth_rating_mapping = {
    '$1-$24,999': 1,
    '$25,000-$49,999': 2,
    '$50,000-$99,999': 3,
    '$100,000-$249,999': 4,
    '$250,000-$499,999': 5,
    '$500,000-$999,999': 6,
    '$1,000,000-$2,499,999': 7,
    '$2,500,000-$4,999,999': 8
}

# Map the WealthRating column using the mapping dictionary
df2['WealthRating'] = df2['WealthRating'].map(wealth_rating_mapping)

df2['WealthRating'].unique()

#code snippet 15
#exporting df to csv file
df2.to_csv('Redcross project0404_1.csv', index=False)

#Code snippet 16
#installing ydata for EDA report
!pip install ydata-profiling

#code snippet 17
#drop wealthrating 'DonorUniqueId','DonorPostalCode','DonorDateOfBirth','CumulativeDonationAmount' ,'IsMemberFlag'
df2 = df2.drop(['DonorUniqueId','DonorPostalCode','DonorDateOfBirth' ,'IsMemberFlag', 'WealthRating', 'CITY', 'STATE'], axis=1)

#Code snippet 18
from ydata_profiling import ProfileReport

profile = ProfileReport(df2, title="Redcross project EDA report2025_1", explorative=True)
profile.to_file("Redcross project EDA report2025_1.html")