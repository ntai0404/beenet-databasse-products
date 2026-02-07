from sheets_service import SheetsService
import os
from dotenv import load_dotenv

load_dotenv()
CREDENTIALS_PATH = os.getenv("CREDENTIALS_FILE", "ggsheet-key.json")
SHEET_URL = os.getenv("SHEET_URL")

service = SheetsService(CREDENTIALS_PATH, SHEET_URL)
spreadsheet = service.client.open_by_url(SHEET_URL)
worksheets = spreadsheet.worksheets()

print("Worksheets found:")
for ws in worksheets:
    print(f"- {ws.title}")
