from flask import Flask, render_template, redirect, Response, request
from flask_cors import CORS
from GoogleDriveService import DriveService
from dbService import dbService
import utils

app = Flask(__name__)
cors = CORS(app)
db = dbService()
drive = DriveService(Client_secret=db.getCredentials())

@app.route('/', methods=['POST','GET'])
@app.route('/login', methods=['POST',"GET"])
def login():
    if request.method == 'POST':
        userData = request.form
        stats = db.login(username=userData.get('username'), password=userData.get('password'))
        if stats.get('login') and stats.get('status')=='success':
            return redirect('/dashboard')
        else:
            return render_template('login.html', message=stats.get('message'))
    else:
        return render_template('login.html')


@app.route('/register', methods=['POST','GET'])
def register():
    if request.method == 'POST':
        formData = request.form
        username = formData.get("username")
        password = formData.get('password')
        confirmPassword = formData.get('confPassword')
        if password != confirmPassword:
            return render_template('signup.html', message='Password does not match')
        else:
            res = db.register(username=username, password=utils.hash(password))
            if res.get('status')=='success':
                return redirect('/login')
            else:
                return render_template('signup.html', message=res.get('message'))
    return render_template('signup.html')

@app.route("/dashboard")
def main():
    displayData = drive.display()
    return render_template("index.html", data=displayData)

@app.route('/file/<filename>')
def get_file_by_name(filename):
    data = drive.get_file_by_name(filename)
    file_data = drive.download_file_by_id(file_id=data.get('id'))
    
    if file_data:
        response = Response(file_data, content_type='image/jpeg')  # Set the content type according to your file type
        response.headers['Content-Disposition'] = 'inline'
        return response
    else:
        return "File not found", 404
    
@app.route('/refresh')
def refresh():
    drive.load()
    return redirect('/dashboard')

@app.route('/about')
def storage():
    storage = drive.get_storage_usage()
    used = round(storage[0], 5)
    total = storage[1]
    value = (used / total) * 100
    return render_template('about.html', used=used, total=total,value=value )

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == "POST":
        data = request.form.get('uploadFile')
        print(data)
        msg = drive.uploadFile(data)
        return render_template('upload.html', msg=msg)
    else:
        return render_template('upload.html')
    


if __name__ == "__main__":
    app.run(debug=True)
