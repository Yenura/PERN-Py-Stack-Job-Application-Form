import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
API_HOST = os.getenv('API_HOST', '0.0.0.0')
API_PORT = int(os.getenv('API_PORT', 5000))

# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME')
CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY')
CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET')

# Database Configuration
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_PORT = int(os.getenv('DB_PORT', 5432))

# Google Sheets Configuration
GOOGLE_SHEETS_CREDENTIALS = os.getenv('GOOGLE_SHEETS_CREDENTIALS')
GOOGLE_SHEET_ID = os.getenv('GOOGLE_SHEET_ID')

# Email Configuration (Brevo)
BREVO_API_KEY = os.getenv('BREVO_API_KEY')

# Webhook URL
WEBHOOK_URL = 'https://rnd-assignment.automations-3d6.workers.dev/'
CANDIDATE_EMAIL = os.getenv('CANDIDATE_EMAIL')  # Your email used for application