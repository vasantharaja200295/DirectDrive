from Google import Create_Service


class DriveService:
    def __init__(self) -> None:
        CLIENT_SECRET_FILE = "credentials.json"
        API_NAME = 'drive'
        API_VERSION = 'v3'
        SCOPES = ['https://www.googleapis.com/auth/drive']

        self.service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    def listFiles(self, folder_id='15_1P_z-Lu8z88Ccd6Af2uWv2MyRoB7No'):
        query = f"parents = '{folder_id}'"
        response = self.service.files().list(q=query).execute()
        return response['files']
    
    def getFile(self, file_id='1AiBMkeDEeIaRMcOGw8sp_gvMe7rtgb_6'):
        request_body = {
            'role':'reader',
            'type':'anyone'
        }

        baseUrl = f"https://drive.google.com/uc?export=download&id="

        self.service.permissions().create(
            fileId=file_id,
            body=request_body
        ).execute()

        share_link = baseUrl+file_id

        return share_link
    

    def testfile(self ,file_id='1AiBMkeDEeIaRMcOGw8sp_gvMe7rtgb_6' ):
        baseUrl = f"https://drive.google.com/uc?export=download&id={file_id}"
        return baseUrl