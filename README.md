# SheetFlow Setup Guide

Welcome to your Premium Google Sheets CRUD system. 

## 🚀 Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   - Create a `.env` file in the project root (template provided in `.env`).
   - Set `SHEET_URL` to your Google Sheet URL.
   - Set `CREDENTIALS_FILE` to the name of your JSON key file (e.g., `firebase-key.json`).

3. **Google Cloud Setup**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project.
   - Enable **Google Sheets API** and **Google Drive API**.
   - Go to **Credentials** -> **Create Credentials** -> **Service Account**.
   - Create a key for the service account (JSON format).
   - Rename the downloaded file to `service_account.json` and place it in the project root.

3. **Share the Sheet**:
   - Open your [Google Sheet](https://docs.google.com/spreadsheets/d/1ekdjU2lJK1MnBzwFr3B8ws2E8GnK1omLJNbIU8puXPI/edit).
   - Click **Share**.
   - Add the email address of your service account (found in `service_account.json`) as an **Editor**.

4. **Run the App**:
   ```bash
   python main.py
   ```
   Access the UI at `http://localhost:8000`.

## 🛠 Project Structure

- `main.py`: FastAPI application and routing.
- `sheets_service.py`: Core logic for interacting with Google Sheets.
- `templates/`: HTML templates (Jinja2).
- `static/`: CSS and assets.
- `requirements.txt`: Python package dependencies.
