from Google import Create_Service
from googleapiclient.http import MediaFileUpload
import os
class DriveService:
    def __init__(self, Client_secret) -> None:
        CLIENT_SECRET_FILE = Client_secret
        API_NAME = 'drive'
        API_VERSION = 'v3'
        SCOPES = ['https://www.googleapis.com/auth/drive']

        self.service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
        self.load()

    def load(self):
        response = self.service.files().list(q="'root' in parents", fields="files(id, name)").execute()
        self.files = response.get('files', [])


    def get_file_by_name(self, filename=""):
        index = {item.get('name'): item for item in self.files}
        return index.get(filename)
    

    def display(self):
        request_body = {
            'role': 'reader',
            'type': 'anyone'
        }
        baseUrl = "https://drive.google.com/uc?export=download&id="

        displayData = []

        for item in self.files:
            temp = {}
            id = item.get('id')
            temp['id'] = id
            self.service.permissions().create(fileId=id, body=request_body).execute()
            temp['image'] = baseUrl + id
            temp['name'] = item.get('name')
            displayData.append(temp)


        return displayData

    def download_file_by_id(self, file_id):
        try:
            request = self.service.files().get_media(fileId=file_id)
            response = request.execute()
            return response
        except Exception as e:
            return None
        
    def uploadFile(self, uploadFile):
        if uploadFile:
            try:
                media = MediaFileUpload(uploadFile.replace('"',''), resumable=True)
                self.service.files().create(
                    media_body = media,
                    body={'name': os.path.basename(uploadFile)}
                ).execute()
                return "File Upload Successfull"
            except Exception as e:
                return f"File upload Failed,\nError: {e}"
        else:
            return "Please select a file"


    def get_storage_usage(self):
        try:
            about = self.service.about().get(fields='storageQuota').execute()
            storage_quota = about.get('storageQuota', {})
            used_storage = storage_quota.get('usage')
            total_storage = storage_quota.get('limit')

            print(f'Used Storage: {int(used_storage)/(1024**3)} GB')
            print(f'Total Storage: {int(total_storage)/(1024**3)} GB')
            return int(used_storage)/(1024**3), int(total_storage)/(1024**3)
        except Exception as e:
            print('Error retrieving storage usage.')
            print(e)

