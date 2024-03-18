import os
import base64
import dropbox
import dropbox.files

from Google import Create_Service

CLIENT_SECRET_FILE = './dropbox/credentials.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']

def gmail_api():
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    return service

def dropbox_api():
    with open("./dropbox/token.txt", "r") as f:
        token = f.read()
    dbx = dropbox.Dropbox(token)
    return dbx

def download_attachments(service, user_id='me'):
    results = service.users().messages().list(userId=user_id, q='is:unread has:attachment').execute()
    messages = results.get('messages', [])
    
    for message in messages:
        msg = service.users().messages().get(userId=user_id, id=message['id']).execute()
        if msg['labelIds'] and 'UNREAD' in msg['labelIds']:
            for part in msg['payload']['parts']:
                if part['filename']:
                    attachment_id = part['body']['attachmentId']
                    attachment = service.users().messages().attachments().get(userId=user_id, messageId=message['id'], id=attachment_id).execute()
                    file_data = base64.urlsafe_b64decode(attachment['data'].encode('UTF-8'))

                    file_path = os.path.join('./downloads', part['filename'])
                    with open(file_path, 'wb') as file:
                        file.write(file_data)

                    yield file_path

def upload_to_dropbox(dbx, file_paths):
    for file_path in file_paths:
        try:
            with open(file_path, 'rb') as file:
                dbx.files_upload(file.read(), f'/downloads/{os.path.basename(file_path)}')
            print(f"Uploaded {os.path.basename(file_path)} successfully.")
        except Exception as e:
            print(f"Failed to upload {os.path.basename(file_path)}:", str(e))

def main():
    gmail_service = gmail_api()
    dbx = dropbox_api()
    
    downloaded_files = download_attachments(gmail_service)
    upload_to_dropbox(dbx, downloaded_files)

if __name__ == '__main__':
    main()

