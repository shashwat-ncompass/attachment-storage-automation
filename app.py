from flask import Flask, request, jsonify
from subprocess import run
import os

app = Flask(__name__)

@app.route('/')
def index():
    return 'Welcome to the Flask app!'

@app.route('/send_email', methods=['POST'])
def send_email():
    data = request.get_json()
    to = data.get('to')
    subject = data.get('subject')
    body = data.get('body')
    attachments = data.get('attachments', [])

    attachment_paths = attachments if isinstance(attachments, list) else [attachments]

    cmd = ['python', 'gmail/send_email.py', to, subject, body]
    for attachment_path in attachment_paths:
        cmd.extend([attachment_path])

    result = run(cmd)
    
    return jsonify({'result': result.returncode})

@app.route('/upload_to_dropbox', methods=['POST'])
def upload_to_dropbox():
    data = request.get_json()
    file_paths = data.get('file_paths', [])

    cmd = ['python', 'dropbox/download_upload.py']
    for file_path in file_paths:
        cmd.extend(['--file', file_path])

    result = run(cmd)
    
    return jsonify({'result': result.returncode})

if __name__ == '__main__':
    app.run(debug=True)
