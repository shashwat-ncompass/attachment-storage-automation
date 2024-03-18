import base64
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

from Google import Create_Service

CLIENT_SECRET_FILE = 'credentials.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

emailMsg = 'You won $100,000'
mimeMessage = MIMEMultipart()
mimeMessage['to'] = 'shashwat@ncompass.inc'
mimeMessage['subject'] = 'You won'
mimeMessage.attach(MIMEText(emailMsg, 'plain'))

# Add attachment
attachment_path = '../dropbox/local_files/img1.jpeg'
attachment_filename = os.path.basename(attachment_path)
attachment = open(attachment_path, "rb")
part = MIMEBase('application', 'octet-stream')
part.set_payload(attachment.read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', f'attachment; filename= {attachment_filename}')
mimeMessage.attach(part)

raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
print(message)