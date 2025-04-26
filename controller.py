from flask import jsonify, request
import google_sheets_service

# data
def register_routes(app):
    @app.route('/data', methods=['GET'])
    def get_data():
        range_name = 'Sheet1'
        data = google_sheets_service.get_sheet_data(range_name)
        return jsonify(data)

    @app.route('/update-headers', methods=['POST'])
    def update_headers():
        headers = request.json.get('headers', [])
        if not headers:
            return jsonify({"error": "No headers provided"}), 400
        range_name = 'A1:L1'
        result = google_sheets_service.update_sheet_headers(range_name, headers)
        return jsonify({"message": "Headers updated", "updatedCells": result.get('updatedCells')})

    @app.route('/add-row', methods=['POST'])
    def add_row():
        values = request.json.get('values')
        if not values:
            return jsonify({"error": "No values provided"}), 400
        range_name = 'Sheet1'
        result = google_sheets_service.add_row(range_name, values)
        return jsonify(result)

    @app.route('/update-values', methods=['POST'])
    def update_values():
        range_name = request.json.get('range')
        values = request.json.get('values')
        if not range_name or not values:
            return jsonify({"error": "Missing range or values"}), 400
        result = google_sheets_service.update_values(range_name, values)
        return jsonify(result)

    @app.route('/clear-values', methods=['POST'])
    def clear_values():
        range_name = request.json.get('range')
        if not range_name:
            return jsonify({"error": "Missing range"}), 400
        result = google_sheets_service.clear_values(range_name)
        return jsonify(result)

    @app.route('/search', methods=['GET'])
    def search():
        query = request.args.get('query', '')
        if not query:
            return jsonify({"error": "Missing query"}), 400
        row = google_sheets_service.search_sheet(query)
        return jsonify(row or {"message": "No match"}), (200 if row else 404)

    @app.route('/delete-row', methods=['POST'])
    def delete_row():
        r = request.json.get('range')
        if not r:
            return jsonify({"error": "Missing range"}), 400
        try:
            _, rng = r.split('!')
            start = int(rng.split(':')[0][1:]) - 1
        except:
            return jsonify({"error": "Invalid range"}), 400
        requests = [{
            "deleteDimension":{
                "range":{
                    "sheetId":0,"dimension":"ROWS",
                    "startIndex": start, "endIndex": start+1
                }
            }
        }]
        result = google_sheets_service.batch_update(requests)
        return jsonify(result)
