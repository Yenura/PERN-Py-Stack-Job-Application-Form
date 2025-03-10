import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from config import BREVO_API_KEY

def schedule_followup_email(to_email, name):
    """
    Send a follow-up email to the applicant
    """
    # Configure API key authorization
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = BREVO_API_KEY
    
    # Create an instance of the API class
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    
    # Create a sender
    sender = {"name": "Metana HR", "email": "hr@metana.io"}
    
    # Create the email
    subject = "Your application at Metana is under review"
    html_content = f"""
    <html>
    <body>
        <p>Dear {name},</p>
        <p>Thank you for applying to Metana. We would like to inform you that your CV is currently under review by our team.</p>
        <p>We will get back to you shortly with further updates on your application.</p>
        <p>Best regards,<br/>Metana HR Team</p>
    </body>
    </html>
    """
    
    # Create send email object
    send_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": to_email, "name": name}],
        sender=sender,
        subject=subject,
        html_content=html_content
    )
    
    try:
        # Send the email
        api_response = api_instance.send_transac_email(send_email)
        return api_response
    except ApiException as e:
        print("Exception when calling TransactionalEmailsApi->send_transac_email: %s\n" % e)
        raise e