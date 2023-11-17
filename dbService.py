from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os
import pickle

load_dotenv('.env')


class dbService:
    def __init__(self) -> None:
        uri = f"mongodb+srv://{os.getenv('MONGOUSERNAME')}:{os.getenv('MONGOPASSWORD')}@cluster0.vpzkuqi.mongodb.net/?retryWrites=true&w=majority"
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.fernet = Fernet
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
            self.secureDb = self.client['Secure']['DirectDrive']

        except Exception as e:
            print(e)

    def getCredentials(self):
        data = self.secureDb.find()[0]
        cipherSuite = Fernet(data['key'])
        decrypted = pickle.loads(cipherSuite.decrypt(data['credentials']))
        return decrypted
