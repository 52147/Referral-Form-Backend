import os
import base64
import json
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Scopes required for accessing and modifying Google Sheets
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Mapping for column indices to sheet column names
COLUMN_NAMES = {
    1: "Name",
    2: "Phone Number",
    3: "Email Address",
    4: "Company Name",
    5: "Current Position/Title",
    6: "Position you can provide referral",
    7: "Provide Sponsorship",
    8: "Candidate's Visa Requirements",
    9: "Additional Information Required",
    10: "Expected Time to Respond",
    11: "Date Added",
    12: "Referrals Status"
}


def get_credentials():
    """
    Load and return service account credentials from the
    GOOGLE_SERVICE_ACCOUNT_JSON_BASE64 environment variable.
    """
    encoded_json = os.environ.get('GOOGLE_SERVICE_ACCOUNT_JSON_BASE64')
    if not encoded_json:
        raise ValueError(
            "The GOOGLE_SERVICE_ACCOUNT_JSON_BASE64 environment variable is not set or empty."
        )
    decoded = base64.b64decode(encoded_json).decode('utf-8')
    info = json.loads(decoded)
    creds = Credentials.from_service_account_info(info, scopes=SCOPES)
    return creds


def get_service():
    """
    Build and return the Google Sheets API service client.
    """
    creds = get_credentials()
    service = build('sheets', 'v4', credentials=creds)
    return service.spreadsheets()


def get_sheet_data(range_name: str) -> list:
    """
    Retrieve values from the specified range in the sheet.
    """
    sheet = get_service()
    spreadsheet_id = os.environ.get('GOOGLE_SPREADSHEET_ID')
    result = sheet.values().get(
        spreadsheetId=spreadsheet_id,
        range=range_name
    ).execute()
    return result.get('values', [])


def update_sheet_headers(range_name: str, headers: list) -> dict:
    """
    Update the header row in the sheet at the given range.
    """
    sheet = get_service()
    spreadsheet_id = os.environ.get('GOOGLE_SPREADSHEET_ID')
    body = {'values': [headers]}
    result = sheet.values().update(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption="RAW",
        body=body
    ).execute()
    return result


def add_row(range_name: str, row_values: list) -> dict:
    """
    Append a single row of values to the sheet.
    """
    sheet = get_service()
    spreadsheet_id = os.environ.get('GOOGLE_SPREADSHEET_ID')
    body = {'values': [row_values]}
    result = sheet.values().append(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption="RAW",
        body=body,
        insertDataOption="INSERT_ROWS"
    ).execute()
    return result


def update_values(range_name: str, values: list) -> dict:
    """
    Update values in the given range of the sheet.
    """
    sheet = get_service()
    spreadsheet_id = os.environ.get('GOOGLE_SPREADSHEET_ID')
    body = {'values': [values]}
    result = sheet.values().update(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption="RAW",
        body=body
    ).execute()
    return result


def clear_values(range_name: str) -> dict:
    """
    Clear values in the specified range of the sheet.
    """
    sheet = get_service()
    spreadsheet_id = os.environ.get('GOOGLE_SPREADSHEET_ID')
    result = sheet.values().clear(
        spreadsheetId=spreadsheet_id,
        range=range_name
    ).execute()
    return result


def search_sheet(query: str) -> dict:
    """
    Search the sheet for rows containing the query text.
    Returns a dict mapping column names to cell values for the first match.
    """
    sheet = get_service()
    spreadsheet_id = os.environ.get('GOOGLE_SPREADSHEET_ID')
    result = sheet.values().get(
        spreadsheetId=spreadsheet_id,
        range="Sheet1"
    ).execute()
    rows = result.get('values', [])
    for row in rows:
        if any(query.lower() in str(cell).lower() for cell in row):
            return {
                COLUMN_NAMES.get(i+1, f"Column {i+1}"): cell
                for i, cell in enumerate(row)
            }
    return {}


def batch_update(requests_body: list) -> dict:
    """
    Perform batch update operations (e.g., deleting rows) using the provided request bodies.
    """
    sheet = get_service()
    spreadsheet_id = os.environ.get('GOOGLE_SPREADSHEET_ID')
    result = sheet.batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={'requests': requests_body}
    ).execute()
    return result
