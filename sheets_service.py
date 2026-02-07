import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from typing import List, Dict, Any, Optional

class SheetsService:
    def __init__(self, credentials_path: str, sheet_url: str):
        self.scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        self.credentials_path = credentials_path
        self.sheet_url = sheet_url
        self.client = None
        self.spreadsheet = None
        self.current_sheet = None
        self._authenticate()

    def _authenticate(self):
        try:
            creds = Credentials.from_service_account_file(self.credentials_path, scopes=self.scope)
            self.client = gspread.authorize(creds)
            self.spreadsheet = self.client.open_by_url(self.sheet_url)
            # Mặc định lấy sheet đầu tiên
            self.current_sheet = self.spreadsheet.get_worksheet(0)
        except Exception as e:
            print(f"Authentication failed: {e}")

    def get_all_sheet_names(self) -> List[str]:
        if not self.spreadsheet:
            return []
        return [ws.title for ws in self.spreadsheet.worksheets()]

    def set_worksheet(self, name: str):
        if not self.spreadsheet:
            return
        self.current_sheet = self.spreadsheet.worksheet(name)

    def get_all_data(self, sheet_name: Optional[str] = None) -> List[Dict[str, Any]]:
        if sheet_name:
            self.set_worksheet(sheet_name)
        if not self.current_sheet:
            return []
        return self.current_sheet.get_all_records()

    def add_row(self, sheet_name: str, data: Dict[str, Any]):
        self.set_worksheet(sheet_name)
        if not self.current_sheet:
            return
        headers = self.current_sheet.row_values(1)
        row = [data.get(header, "") for header in headers]
        self.current_sheet.append_row(row)

    def update_row(self, sheet_name: str, row_index: int, data: Dict[str, Any]):
        self.set_worksheet(sheet_name)
        if not self.current_sheet:
            return
        headers = self.current_sheet.row_values(1)
        for header, value in data.items():
            if header in headers:
                col_index = headers.index(header) + 1
                self.current_sheet.update_cell(row_index, col_index, value)

    def delete_row(self, sheet_name: str, row_index: int):
        self.set_worksheet(sheet_name)
        if not self.current_sheet:
            return
        self.current_sheet.delete_rows(row_index)

    def get_headers(self, sheet_name: str) -> List[str]:
        self.set_worksheet(sheet_name)
        if not self.current_sheet:
            return []
        return self.current_sheet.row_values(1)
    
    def create_new_sheet_with_headers(self, new_sheet_name: str, template_sheet_name: str) -> str:
        """
        Tạo sheet con mới và copy header từ template sheet
        Returns: URL trực tiếp đến sheet mới
        """
        if not self.spreadsheet:
            raise Exception("Spreadsheet not initialized")
        
        # Kiểm tra xem sheet đã tồn tại chưa
        existing_sheets = [ws.title for ws in self.spreadsheet.worksheets()]
        if new_sheet_name in existing_sheets:
            raise Exception(f"Sheet '{new_sheet_name}' đã tồn tại!")
        
        # Lấy headers từ template sheet
        headers = self.get_headers(template_sheet_name)
        if not headers:
            raise Exception(f"Không thể lấy headers từ sheet '{template_sheet_name}'")
        
        # Tạo worksheet mới
        new_worksheet = self.spreadsheet.add_worksheet(title=new_sheet_name, rows=1000, cols=len(headers))
        
        # Copy headers vào dòng đầu tiên
        new_worksheet.update('A1', [headers])
        
        # Lấy spreadsheet_id và sheet_id để tạo URL
        spreadsheet_id = self.spreadsheet.id
        sheet_id = new_worksheet.id
        
        # Tạo URL trực tiếp đến sheet mới
        sheet_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit#gid={sheet_id}"
        
        return sheet_url
