from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from sheets.Auth import SheetAuth
from utils.parser import parser


class SheetService:
    def __init__(self, auth: SheetAuth):
        service = build('sheets', 'v4', credentials=auth.credentials)
        self.sheet_id = parser.get('sheets', 'id')
        self.table_name = parser.get('sheets', 'tableName')

        # Call the Sheets API
        self.sheet = service.spreadsheets()

    def read(self, _range: str) -> list:
        """
        reads cells from the google sheet by given range
        :param _range: rows to read (example. A1:10)
        :return: List
        """
        try:
            result = self.sheet.values().get(spreadsheetId=self.sheet_id, range=_range).execute()
        except HttpError as error:
            print(f"An error occurred: {error}")
            return []
        return result.get('values', [])

    def write(self, _range, value_input_option, _values):
        body = {
            'values': _values
        }

        result = self.sheet.values().update(
            spreadsheetId=self.sheet_id, range=_range,
            valueInputOption=value_input_option, body=body).execute()

        print(f"{result.get('updatedCells')} cells updated.")
