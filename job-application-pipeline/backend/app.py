from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import tempfile
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import pytz
from apscheduler.schedulers.background import BackgroundScheduler
import json

# Import custom modules
from config import API_HOST, API_PORT, CANDIDATE_EMAIL
from services.db_service import init_db, insert_application, get_application_by_id
from services.storage_service import upload_file
from services.parser_service import extract_cv_data
from services.sheets_service import add_to_google_sheet
from services.webhook_service import send_webhook
from services.email_service import schedule_followup_email

app = Flask(__name__)
CORS(app)

# Initialize the database
init_db()

# Initialize the scheduler
scheduler = BackgroundScheduler()
scheduler.start()

@app.route('/api/applications', methods=['POST'])
def submit_application():
    try:
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        
        # Check if CV file is included
        if 'cv' not in request.files:
            return jsonify({'error': 'No CV file uploaded'}), 400
        
        cv_file = request.files['cv']
        if cv_file.filename == '':
            return jsonify({'error': 'No CV file selected'}), 400
        
        # Save file temporarily
        temp_dir = tempfile.gettempdir()
        filename = secure_filename(cv_file.filename)
        file_path = os.path.join(temp_dir, filename)
        cv_file.save(file_path)
        
        # Upload to Cloudinary
        upload_result = upload_file(file_path, folder="cvs")
        cv_public_url = upload_result.get('secure_url')
        
        # Extract data from CV
        cv_data = extract_cv_data(file_path)
        cv_data['cv_public_link'] = cv_public_url
        
        # Insert into database
        submission_status = request.form.get('status', 'testing')  # Default to testing
        application_id = insert_application(name, email, phone, cv_public_url, 
                                         json.dumps(cv_data), submission_status)
        
        # Add to Google Sheet
        add_to_google_sheet(name, email, phone, cv_public_url, cv_data)
        
        # Send webhook
        timestamp = datetime.now(pytz.utc).isoformat()
        webhook_payload = {
            "cv_data": cv_data,
            "metadata": {
                "applicant_name": name,
                "email": email,
                "status": submission_status,
                "cv_processed": True,
                "processed_timestamp": timestamp
            }
        }
        send_webhook(webhook_payload, CANDIDATE_EMAIL)
        
        # Schedule follow-up email for next day
        if submission_status == "prod":
            user_timezone = pytz.timezone('Asia/Kolkata')  # Default to IST (+5:30 GMT)
            now = datetime.now(user_timezone)
            send_time = (now + timedelta(days=1)).replace(hour=10, minute=0, second=0)
            scheduler.add_job(
                schedule_followup_email,
                'date',
                run_date=send_time,
                args=[email, name]
            )
        
        # Clean up temp file
        os.remove(file_path)
        
        return jsonify({
            'id': application_id,
            'message': 'Application submitted successfully',
            'cv_url': cv_public_url
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host=API_HOST, port=API_PORT, debug=True)