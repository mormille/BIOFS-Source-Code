# upload_csv.py
# upload / update csv file on google cloud
# 2024-10-30


import gspread
from oauth2client.service_account import ServiceAccountCredentials
import csv

# Path to your service account key file
SERVICE_ACCOUNT_FILE = '../../credentials/biofs-v1-d9781d73191a.json'

# Define the scope
SCOPE = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# Authorize and connect to the Google Sheets API
credentials = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, SCOPE)


#gc = gspread.service_account(filename="biofs-v1-936568fca76c.json") # connection test

#spreadsheets = gc.openall() # connection tests
#for sheet in spreadsheets: # connection test
#    print(sheet.title) # connection test
    
gc = gspread.authorize(credentials)

# Open the Google Sheet by its name or URL
spreadsheet = gc.open("BIOFS_Spreadsheet_Data")  # e.g., 'DataLog'
worksheet = spreadsheet.sheet1  # Access the first sheet

# Path to your CSV file
CSV_FILE_PATH = 'logs/BIOFS_log.csv'

# Open the CSV file and read its contents
with open(CSV_FILE_PATH, 'r') as file:
    csv_reader = csv.reader(file)
    data = list(csv_reader)

# Append each row from the CSV file to the Google Sheet
for row in data:
    worksheet.append_row(row)

print("Data has been successfully uploaded to Google Sheets.")
