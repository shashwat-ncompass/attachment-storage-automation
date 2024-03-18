import base64
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from Google import Create_Service

def send_email(to, subject, body, attachments=None):
    CLIENT_SECRET_FILE = 'credentials.json'
    API_NAME = 'gmail'
    API_VERSION = 'v1'
    SCOPES = ['https://mail.google.com/']
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    email_msg = MIMEMultipart()
    email_msg['to'] = to
    email_msg['subject'] = subject
    email_msg.attach(MIMEText(body, 'plain'))

    if attachments:
        for attachment_path in attachments:
            if os.path.exists(attachment_path):
                attachment_filename = os.path.basename(attachment_path)
                attachment = open(attachment_path, 'rb')
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename= {attachment_filename}')
                email_msg.attach(part)
            else:
                print(f"Attachment not found: {attachment_path}")

    raw_string = base64.urlsafe_b64encode(email_msg.as_bytes()).decode()

    message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
    return message

if __name__ == '__main__':
    import sys
    to = sys.argv[1]
    subject = sys.argv[2]
    body = sys.argv[3]
    attachments = sys.argv[4:] if len(sys.argv) >= 5 else []

    if attachments and attachments[0].lower() != 'none':
        message = send_email(to, subject, body, attachments)
    else:
        message = send_email(to, subject, body)
    print(message)
