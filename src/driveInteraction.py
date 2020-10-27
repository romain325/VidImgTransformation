from __future__ import print_function
import pickle
import io
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def pathToId(folderPath):
    return folderPath.split('/')[-1]

def authentication():
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('creds.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', "wb") as token:
            pickle.dump(creds,token)
    
    service = build('drive', 'v3', credentials=creds)
    return service

def list_files(folderId, service):
    fileArray = []
    results = service.files().list(q="'"+folderId+"' in parents and (mimeType='image/png' or mimeType='image/jpeg')", pageSize=80, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    
    if not items:
        print("Empty")
    else:
        for i in items:
            fileArray.append({i['name']: i['id']})

    return fileArray

def downloadFile(file_id,fileName,folderPath, service):
    req = service.files().get_media(fileId=file_id)
    fh = io.FileIO(folderPath+ "/" + "driveRenderTMP_"+fileName, 'wb')
    DLer = MediaIoBaseDownload(fh, req)
    done = False
    while not done:
        status, done = DLer.next_chunk()
        print("Downloading of "+fileName+" %d%%" % int(status.progress() * 100))

def dl_drive_folder(folderId, dlPath):
    service = authentication()
    fileArray = list_files(pathToId(folderId), service)

    print("**************************************")
    print("Start Drive Downlaods")
    print("**************************************")

    for file in fileArray:
        for x in file:
            downloadFile(file[x], x,dlPath,service)

    print("**************************************")
    print("All the Downloads are complete")
    print("**************************************")
