import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import base64
import json

COLUMN_NAMES = {
    1: "Name",
    2: "Phone Number",
    3: "Email Address",
    4: "Company Name",
    5: "Current Position/Title",
    6: "Position you can provide referral",
    7: "Candidate Visa Requirements",
    8: "Candidate's Work Authorization",
    9: "Additional Information Required",
    10: "Expected Time to Respond"
}

# Assuming the environment variables are set correctly
# SERVICE_ACCOUNT_FILE = os.getenv('GOOGLE_SERVICE_ACCOUNT_FILE')  # Corrected environment variable name
SPREADSHEET_ID = os.getenv('GOOGLE_SPREADSHEET_ID')
# Load the base64 encoded service account key from an environment variable
encoded_service_account_json = os.environ.get('GOOGLE_SERVICE_ACCOUNT_JSON_BASE64')
if encoded_service_account_json is None:
    raise ValueError("The GOOGLE_SERVICE_ACCOUNT_JSON_BASE64 environment variable is not set or empty.")

# Decode the service account JSON
decoded_json = base64.b64decode(encoded_service_account_json).decode('utf-8')
service_account_info = json.loads(decoded_json)

# Use the service account to authenticate
credentials = Credentials.from_service_account_info(service_account_info)

# Now you can use `credentials` for Google API clients that require authenticatio
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_sheet_data(range_name):
    # Use the credentials that were already set up
    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=range_name).execute()
    values = result.get('values', [])
    return values

def update_sheet_headers(spreadsheet_id, range_name, values):
    service = build('sheets', 'v4', credentials=credentials)
    body = {'values': [values]}
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption="RAW", body=body).execute()
    return result

def add_row(spreadsheet_id, range_name, values):
    service = build('sheets', 'v4', credentials=credentials)
    body = {'values': [values]}
    result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption="RAW", body=body, insertDataOption="INSERT_ROWS").execute()
    return result

def update_values(spreadsheet_id, range_name, values):
    service = build('sheets', 'v4', credentials=credentials)
    body = {'values': [values]}
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption="RAW", body=body).execute()
    return result

def clear_values(spreadsheet_id, range_name):
    service = build('sheets', 'v4', credentials=credentials)
    result = service.spreadsheets().values().clear(
        spreadsheetId=spreadsheet_id, range=range_name).execute()
    return result

def search_sheet(spreadsheet_id, query):
    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range="Sheet1").execute()
    values = result.get('values', [])
    # Adjust the logic to return all data from the row where a match is found
    for row in values:
        # Search for the query in the row; if found, return all data from this row
        if any(query.lower() in str(cell).lower() for cell in row):
            # Map the row's data with their corresponding column names
            row_data = {COLUMN_NAMES.get(i+1, f"Column {i+1}"): cell for i, cell in enumerate(row)}
            return row_data  # Return the first matching row's data

    return {}  # Return an empty dict if no match is found