from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os
import pickle
import utils
import pymongo

load_dotenv('.env')


class dbService:
    def __init__(self) -> None:
        uri = f"mongodb+srv://{os.getenv('MONGOUSERNAME')}:{os.getenv('MONGOPASSWORD')}@cluster0.vpzkuqi.mongodb.net/?retryWrites=true&w=majority"
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.fernet = Fernet
        self.userName = ""
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
            self.secureDb = self.client['Secure']['DirectDrive']
            self.db = self.client['DirectDrive']['Users']
            self.db.create_index("username", unique=True)
        except Exception as e:
            print(e)

    def getCredentials(self):
        data = self.secureDb.find()[0]
        cipherSuite = Fernet(data['key'])
        decrypted = pickle.loads(cipherSuite.decrypt(data['credentials']))
        return decrypted
    
    def login(self, username, password):
        user = self.db.find_one({"username":username})
        if user:
            if user.get('password') == utils.hash(password) and user.get('username') == username:
                self.userName = user.get('username')
                return {'login':True, 'status': "success", 'message':"Login Sucessfull", 'uid':user.get('_id')}
            else:
                return {'login':False, 'status': "failed", 'message':"Invalid Username or Password"}
        else:
            return {'login':False, 'status': "failed", 'message':"No User Found"}
        
    def register(self, username, password):
        try:
            self.db.insert_one({"username":username, 'password':password})
            return {'status':'success', 'message':'User Successfully Registered'}
        except pymongo.errors.DuplicateKeyError:
            return {'status':'failed', 'message':'Username Already Exists'}
