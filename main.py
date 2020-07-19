import os.path
import pickle
import sys
import zipfile
from io import BytesIO

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.file']

os.chdir(os.path.dirname(__file__))


def zipdir(zip_folder_path):
    mem_zip = BytesIO()

    with zipfile.ZipFile(mem_zip, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(zip_folder_path):
            for file in files:
                # we want to designate the zip_folder_path as an absolute path, while having the path tree in the ZIP
                # relative to it (we don't want the full absolute path reproduced in the zip...)
                file_path = os.path.join(root, file)
                file_rel_path = os.path.relpath(file_path, zip_folder_path)

                zf.write(file_path, arcname=file_rel_path)

    return mem_zip


def main():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    # ------ search for upload folder, or create it ------
    results = service.files().list(q=f"mimeType='application/vnd.google-apps.folder' and name='{sys.argv[1]}'",
                                   spaces='drive',
                                   pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('Folder not found, creating it...')
        file_metadata = {
            'name': sys.argv[1],
            'mimeType': 'application/vnd.google-apps.folder'
        }
        file = service.files().create(body=file_metadata,
                                      fields='id').execute()
        folder_id = file.get('id')
    else:
        folder_id = items[0]['id']
    print(f'Folder ID: {folder_id}')

    # ------ ZIP folder ------
    zip_file = zipdir(sys.argv[2])

    # ------ upload file ------
    file_metadata = {
        'name': os.path.basename(sys.argv[3]),
        'parents': [folder_id]
    }
    media = MediaIoBaseUpload(zip_file,
                              mimetype="application/zip",
                              resumable=True)
    file = service.files().create(body=file_metadata,
                                  media_body=media,
                                  fields='id').execute()
    print(f'Upload success. File ID: {file.get("id")}')


if __name__ == '__main__':
    if len(sys.argv) != 4:
        sys.exit("Wrong number of arguments. "
                 "Usage: main.py <GDrive folder name> <local folder path> <ZIP filename>")

    main()
