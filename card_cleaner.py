import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re

def clean_card():
    
    """
    Cleans and processes a CSV file containing business card data.

    This function prompts the user to enter the filename of the CSV file that needs cleaning.
    It reads the CSV file into a DataFrame using pandas and performs various cleaning operations,
    including removing duplicated rows, standardizing column names, formatting phone numbers,
    extracting first and last names from full names, converting text columns to uppercase or lowercase,
    and reordering columns.

    The cleaned DataFrame is then exported to a new CSV file with the prefix 'Clean' added to the filename.

    Purpose:
    This function provides a convenient way to clean and process business card data stored in a CSV file,
    preparing it for further analysis or usage.
    """

    # Prompt the user to enter the filename of the CSV file that needs cleaning
    filename = input("Enter the filename that needs cleaning: ")

    # Append the file extension '.csv' to the filename entered by the user
    filename_csv = filename + '.csv'

    # Read the CSV file into a DataFrame using pandas
    bus_card = pd.read_csv(filename_csv)



    # Remove duplicated rows from the DataFrame and update 'bus_card' to contain only unique rows
    bus_card = bus_card[bus_card.duplicated() == False]

    # Reset the index of the DataFrame and drop the 'index' and 'Memo' columns
    # This step ensures that the index is consecutive and starts from 0
    bus_card = bus_card.reset_index().drop(columns=['index', 'Memo'])

    # Convert column names to lowercase and replace special characters ('/', '-', and ' ') with underscores ('_')
    # This standardizes the column names for consistency and ease of use
    bus_card.columns = bus_card.columns.str.lower().str.replace('/', '_').str.replace('-', '_').str.replace(' ', '_')


    # Extract 'phone_number', 'fax_number', and 'mobile_phone' columns from the 'bus_card' DataFrame
    phone_num = bus_card['phone_number']
    fax_num = bus_card['fax_number']
    mobile_num = bus_card['mobile_phone']

    # Define a regular expression pattern to match phone numbers
    regexp = r'\(?\b(\d{3})\)?[.-]?(\d{3})[.-](\d{4})\b'

    # Replace phone numbers in the 'phone_number' column using the defined regex pattern
    bus_card['phone_number'] = phone_num.str.replace(regexp, r'(\1)\2-\3', regex=True)

    # Replace phone numbers in the 'fax_number' column using the defined regex pattern
    bus_card['fax_number'] = fax_num.str.replace(regexp, r'(\1)\2-\3', regex=True)

    # Replace phone numbers in the 'mobile_phone' column using the defined regex pattern
    bus_card['mobile_phone'] = mobile_num.str.replace(regexp, r'(\1)\2-\3', regex=True)


    # Extract the first name from the 'full_name' column and create a new 'first_name' column
    bus_card['first_name'] = bus_card['full_name'].str.split().str[0]

    # Extract the last name from the 'full_name' column and create a new 'last_name' column
    bus_card['last_name'] = bus_card['full_name'].str.split().str[-1]

    # Extract the last part (zip code) from the 'zip_postal_code' column and update the column with it
    bus_card['zip_postal_code'] = bus_card['zip_postal_code'].str.split().str[-1]

    # Convert the 'company' column to uppercase
    bus_card['company'] = bus_card['company'].str.upper()

    # Convert the 'e_mail' column to lowercase
    bus_card['e_mail'] = bus_card['e_mail'].str.lower()

    # Convert the 'website' column to lowercase
    bus_card['website'] = bus_card['website'].str.lower()

    # Define the desired column order
    new_order = ['first_name', 'last_name', 'job_title', 'company', 'department', 
                 'phone_number', 'mobile_phone', 'fax_number', 'e_mail', 
                 'website', 'address', 'zip_postal_code', 'location_region']

    # Reorder the columns in the DataFrame based on the 'new_order' list
    bus_card = bus_card[new_order]
    bus_card.rename(columns = {'first_name':'First Name', 'last_name': 'Last Name', 'job_title': 'Job Title', 'company': 'Employer', 'phone_number': 'Work Phone Number', 'mobile_phone': 'Mobile Phone Number', 'fax_number': 'Fax Number', 'e_mail': 'Work Email', 'website': 'Website', 'address': 'Work Address', 'zip_postal_code': 'Work ZIP Code', 'location_region': 'Work Country',}, inplace=True)
    return bus_card.to_csv(f'Clean {filename_csv}')