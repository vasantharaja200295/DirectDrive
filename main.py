from flask import Flask, render_template, redirect, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv('.env')

app = Flask(__name__)
cors = CORS(app)


from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://vasantharaja200295:cjcCN2FklWjw427W@cluster0.vpzkuqi.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


db = client.mydb.users

@app.route("/")
def main():
    return render_template("index.html")

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json  
    print(data)
    row = db.find_one({'username':data['username']})
    if row and row['password'] == data['password']:
        response_data = {'message': 'login Successfull', "code":'ok'}
    else:
        response_data = {'message': 'login failed', "code":'falied'}
    return jsonify(response_data)


@app.route('/api/register', methods=['POST'])
def register():
    data = request.json  # Assuming you are sending JSON data
    row = db.find_one({'username':data['username']})
    if not row:
        db.insert_one({'username':data['username'], "password":data["password"]})
        response_data = {'message':'register sucessfull', "code":'ok'}
    else:
        response_data= {'message':'user already exists', "code":'exists'}
    return jsonify(response_data)


@app.route("/api/<appid>/hello")
def test(appid):
    if appid == "1":
        return "you are authorized"
    return "you are not authorized"



if __name__ == "__main__":
    app.run(debug=True)
