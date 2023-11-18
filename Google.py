from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime

def Create_Service(service_account_data, api_name, api_version, *scopes):
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]

    credentials = service_account.Credentials.from_service_account_info(service_account_data, scopes=SCOPES)
    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
        print(f"{str.capitalize(API_SERVICE_NAME)} service created successfully")
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None

def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
    return dt
