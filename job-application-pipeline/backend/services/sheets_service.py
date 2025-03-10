import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from config import GOOGLE_SHEETS_CREDENTIALS, GOOGLE_SHEET_ID

def get_sheets_service():
    # Load credentials from JSON string
    credentials_info = json.loads(GOOGLE_SHEETS_CREDENTIALS)
    credentials = service_account.Credentials.from_service_account_info(
        credentials_info, scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    service = build('sheets', 'v4', credentials=credentials)
    return service

def add_to_google_sheet(name, email, phone, cv_url, cv_data):
    service = get_sheets_service()
    
    # Format the data
    education = ", ".join(cv_data.get("education", []))[:1000]
    qualifications = ", ".join(cv_data.get("qualifications", []))[:1000]
    projects = ", ".join(cv_data.get("projects", []))[:1000]
    
    # Prepare row data
    row = [
        name,
        email,
        phone,
        cv_url,
        education,
        qualifications,
        projects
    ]
    
    # Append to sheet
    body = {
        'values': [row]
    }
    
    result = service.spreadsheets().values().append(
        spreadsheetId=GOOGLE_SHEET_ID,
        range='Sheet1',
        valueInputOption='RAW',
        insertDataOption='INSERT_ROWS',
        body=body
    ).execute()
    
    return result