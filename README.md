# Google Drive uploader

This Python 3 script allows to archive a local folder, as a ZIP file, and upload it to a Google Drive folder. It allows to easily backup a folder from a server for example.

By using the very specific OAuth2 scope `https://www.googleapis.com/auth/drive.file`, the token generated for this app only gives access to Google Drive and only to the folder and the files this script has created (or the user has decided to give access to). If the token is leaked it is less dangerous than disclosing the full Google account credentials!

Here is how this permission is displayed by Google when granting access to the application:
![](/img/gdrive_uploader_authorize.png)

You can review or revoke this given permission on <https://myaccount.google.com/permissions>:
![](/img/gdrive_uploader_account.png)

Code inspired from: [Google Drive Python quickstart](https://developers.google.com/drive/activity/v1/quickstart/python)

## credentials.json
This file is required for the script to work.
See instructions on: <https://developers.google.com/drive/activity/v1/quickstart/python#step_1_turn_on_the>
1. Create an app and give it a name
2. Choose "Desktop app" type
3. Click on "Download client configuration" and you will get the credentials.json file you need!
This will declare the OAuth2 application.

Then you need to authorize it to access the Google Drive space of your Google account, so for the first time run the application on your desktop as you will get prompted in the browser. Then it can work fine on a headless server.

## Known limitations
* ZIP file is prepared in-memory, so be careful with its size!