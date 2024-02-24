import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Assuming the environment variables are set correctly
SERVICE_ACCOUNT_FILE = os.getenv('GOOGLE_SERVICE_ACCOUNT_FILE')  # Corrected environment variable name
SPREADSHEET_ID = os.getenv('GOOGLE_SPREADSHEET_ID')

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def get_sheet_data(range_name):
    credentials = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=range_name).execute()
    values = result.get('values', [])
    return values

def update_sheet_headers(spreadsheet_id, range_name, values):
    credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)
    body = {'values': [values]}
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption="RAW", body=body).execute()
    return result

def add_row(spreadsheet_id, range_name, values):
    credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)
    body = {'values': [values]}
    result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption="RAW", body=body, insertDataOption="INSERT_ROWS").execute()
    return result

def update_values(spreadsheet_id, range_name, values):
    credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)
    body = {'values': [values]}
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption="RAW", body=body).execute()
    return result

def clear_values(spreadsheet_id, range_name):
    credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=credentials)
    result = service.spreadsheets().values().clear(
        spreadsheetId=spreadsheet_id, range=range_name).execute()
    return result
