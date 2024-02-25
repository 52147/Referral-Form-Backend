

# Google Sheets Referral Form Backend

This project provides a backend solution for users in China who cannot directly access Google Sheets. It facilitates the addition of referral information to a Google Sheet via a Flask-based API. This solution is particularly useful for scenarios where direct interaction with Google's services is restricted or unreliable.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.6 or higher
- Flask
- Google API Python Client
- A Google Cloud Platform account with the Sheets API enabled
- A service account key file (`service-account.json`)

### Setting Up

1. **Clone the Repository**

```bash
git clone https://yourrepositorylink.git
cd google-sheets-referral-backend
```

2. **Install Dependencies**

```bash
pip install Flask google-api-python-client google-auth
```

3. **Configure Environment Variables**

Create a `.env` file in the root directory of your project and add your Google Sheets ID:

```plaintext
GOOGLE_SPREADSHEET_ID=your_spreadsheet_id_here
```

Remember to replace `your_spreadsheet_id_here` with the actual ID of your Google Sheet.

4. **Start the Flask Application**

```bash
flask run
```

This will start the server on `http://127.0.0.1:5000/`.

## Usage

The API provides endpoints to add referral information, update existing entries, and clear entries in a Google Sheet.

### Add Referral Information

To add a new referral entry:

```bash
curl -X POST http://127.0.0.1:5000/add-row \
-H "Content-Type: application/json" \
-d '{"values": ["Name", "Phone Number", "Email Address", "Company Name", "Current Position/Title", "Position you can provide referral", "Candidate Visa Requirements", "Candidate's Work Authorization", "Additional Information Required", "Expected Time to Respond"]}'
```

### Update an Entry

To update an existing entry in a specific range:

```bash
curl -X POST http://127.0.0.1:5000/update-values \
-H "Content-Type: application/json" \
-d '{"range": "Sheet1!A2:J2", "values": ["Updated Name", "Updated Phone Number", ...]}'
```

### Clear an Entry

To clear (delete) an entry in a specified range:

```bash
curl -X POST http://127.0.0.1:5000/clear-values \
-H "Content-Type: application/json" \
-d '{"range": "Sheet1!A2:J2"}'
```
### Search for Referral Information
Search for a referral entry by name and return all associated data:
```bash
curl "http://127.0.0.1:5000/search?query=John%20Doe"
```
This search will return all column data for the row where "John Doe" was found, labeled by column name.
Return result:
```bash
{
  "Additional Information Required": "None",
  "Candidate Visa Requirements": "None",
  "Candidate's Work Authorization": "Citizen",
  "Company Name": "Example Company",
  "Current Position/Title": "Software Engineer",
  "Email Address": "johndoe@example.com",
  "Expected Time to Respond": "1 week",
  "Name": "John Doe",
  "Phone Number": "123-456-7890",
  "Position you can provide referral": "Engineering"
}
```

## Contributing

Contributions are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to everyone who has contributed to this project.
- Special thanks to the Flask and Google Sheets API teams for their excellent documentation.
