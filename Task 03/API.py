import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = "1ohQXqdGZLJJgsV6GSN2Y1ilyv4np1lrXxZq2e6niBZ0"

def main():
    credentials = None
    # Check credentials
    if os.path.exists('token.json'):
        credentials = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not credentials or not credentials.valid:
        # Refresh credentials
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            # Get credentials
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            credentials = flow.run_local_server(port=0)
        # Save credentials
        with open("token.json", "w") as token:
            token.write(credentials.to_json())
    
    try:
        # Get data from spreadsheet
        service = build("sheets", "v4", credentials=credentials)
        # Call the Sheets API
        sheet = service.spreadsheets()
        # Get data from spreadsheet
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="Sheet4!C1:J9").execute()
        # Get values from result
        values = result.get("values", [])

        # Print values
        for row in values:
            print(row)
    
    # Error Handaling
    except HttpError as e:
        print(f"An error occured: {e}") 

if __name__ == "__main__":
    main()