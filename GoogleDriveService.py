from Google import Create_Service

class DriveService:
    def __init__(self) -> None:
        CLIENT_SECRET_FILE = "credentials.json"
        API_NAME = 'drive'
        API_VERSION = 'v3'
        SCOPES = ['https://www.googleapis.com/auth/drive']

        self.service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
        folder_id='1f_OmKk4pBeFPzCqvyzWmlL_-m1laDMep'
        self.query = f"parents = '{folder_id}'"
        response = self.service.files().list(q=self.query).execute()
        self.files = response.get('files', [])

    def refresh(self):
        response = self.service.files().list(q=self.query).execute()
        self.files = response.get('files', [])


    def get_file_by_name(self, filename=""):
        index = {item.get('name'): item for item in self.files}
        return index.get(filename)
    

    def display(self, file_id=''):
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
