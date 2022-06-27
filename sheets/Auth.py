import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1omlM8qEsqKDE_Av2EPUP7oRPhPav3PjpRYrhp5tGLU4'
SAMPLE_RANGE_NAME = 'ClassA!A2:B'


class SheetAuth:
    def __init__(self):
        self.credentials = None
        self.load_credentials()

    def load_credentials(self):
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('../token.json'):
            self.credentials = Credentials.from_authorized_user_file('../token.json', SCOPES)

        # If there are no (valid) credentials available, let the user log in.
        if not self.credentials or not self.credentials.valid:
            if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                self.credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('../credentials.json', SCOPES)
                self.credentials = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open('../token.json', 'w') as token:
                token.write(self.credentials.to_json())
