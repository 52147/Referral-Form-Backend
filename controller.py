from flask import Flask, jsonify, request  # Make sure to import 'request' here
import googleapiclient.discovery
import google_sheets_service
import os
from flask_cors import CORS

SPREADSHEET_ID = os.getenv('GOOGLE_SPREADSHEET_ID')

app = Flask(__name__)
# Enable CORS for all domains on all routes. Adjust according to your needs.
CORS(app)
@app.route('/data', methods=['GET'])
def get_data():
    range_name = 'Sheet1'  # Specify the actual range
    data = google_sheets_service.get_sheet_data(range_name)
    return jsonify(data)

@app.route('/update-headers', methods=['POST'])
def update_headers():
    headers = request.json.get('headers', [])
    if not headers:
        return jsonify({"error": "No headers provided"}), 400
    range_name = 'A1:J1'  # Update this range as needed
    result = google_sheets_service.update_sheet_headers(SPREADSHEET_ID, range_name, headers)
    return jsonify({"message": "Headers updated successfully", "updatedCells": result.get('updatedCells')})


@app.route('/add-row', methods=['POST'])
def add_row():
    data = request.json
    values = data.get('values')
    range_name = 'A1:J1'  # Specify the range or sheet name as needed
    result = google_sheets_service.add_row(SPREADSHEET_ID, range_name, values)
    return jsonify(result)


@app.route('/update-values', methods=['POST'])
def update_values():
    data = request.json
    range_name = data.get('range')  # Corrected from data.get('A1:J1')
    values = data.get('values')
    if not range_name or not values:
        return jsonify({"error": "Missing range or values"}), 400
    result = google_sheets_service.update_values(SPREADSHEET_ID, range_name, values)
    return jsonify(result)

@app.route('/clear-values', methods=['POST'])
def clear_values():
    data = request.json
    range_name = data.get('range')  # Corrected from data.get('A1:J1')
    if not range_name:
        return jsonify({"error": "Missing range"}), 400
    result = google_sheets_service.clear_values(SPREADSHEET_ID, range_name)
    return jsonify(result)


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    if not query:
        return jsonify({"error": "Missing query parameter"}), 400

    row_data = google_sheets_service.search_sheet(SPREADSHEET_ID, query)
    if row_data:
        return jsonify(row_data)
    else:
        return jsonify({"message": "No match found"}), 404

@app.route('/delete-row', methods=['POST'])
def delete_row():
    data = request.json
    range_name = data.get('range')
    if not range_name:
        return jsonify({"error": "Missing range"}), 400
    
    try:
        sheet_name, row_range = range_name.split('!')
        start_row = int(row_range[1:]) - 1  # Convert to 0-based index for the API
    except ValueError:
        return jsonify({"error": "Invalid range format"}), 400

    # Assuming google_sheets_service is already authenticated and set up
    batch_update_request_body = {
        "requests": [
            {
                "deleteDimension": {
                    "range": {
                        "sheetId": SPREADSHEET_ID,  # You need to specify the correct sheet ID here
                        "dimension": "ROWS",
                        "startIndex": start_row,
                        "endIndex": start_row + 1
                    }
                }
            }
        ]
    }

    try:
        result = google_sheets_service.batchUpdate(spreadsheetId=SPREADSHEET_ID, body=batch_update_request_body).execute()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
