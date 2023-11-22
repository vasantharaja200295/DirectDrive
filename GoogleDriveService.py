from Google import Create_Service
from googleapiclient.http import MediaIoBaseUpload
from io import BufferedReader

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
        
    def deleteFile(self, file_id):
        try:
            self.service.files().delete(fileId=file_id).execute()
            return True
        except Exception as e:
            print(e)
            return False
        
    def uploadFile(self, uploadFile, mimeType):
        if uploadFile:
            try:
                buffer_reader = BufferedReader(uploadFile)
                media = MediaIoBaseUpload(buffer_reader,mimetype=mimeType ,resumable=True)
                self.service.files().create(
                    media_body = media,
                    body={'name': uploadFile.name}
                ).execute()
                return {'status':'success', 'message':"File Upload Successfull"}
            except Exception as e:
                return {'status':'success', 'message':f"File upload Failed,\nError: {e}"}
        else:
            return {'status':'success', 'message':"Please select a file"}


    def get_storage_usage(self):
        try:
            about = self.service.about().get(fields='storageQuota').execute()
            storage_quota = about.get('storageQuota', {})
            used_storage = storage_quota.get('usage')
            total_storage = storage_quota.get('limit')
            print(storage_quota)
            return used_storage, total_storage
        except Exception as e:
            print(e)

