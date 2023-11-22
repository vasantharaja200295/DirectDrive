from flask import Flask, render_template, redirect, Response, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from flask_cors import CORS
from GoogleDriveService import DriveService
from dbService import dbService
import utils
import os
import io


app = Flask(__name__)
cors = CORS(app)
app.config['SECRET_KEY'] = '08-~91*(3}~_o|/_yn.Z$EhB^TzWf-4sK"yGi]ys?2;W=O6J:s'
app.config['UPLOAD_FOLDER'] = 'uploads'
loginManager = LoginManager(app)
db = dbService()
drive = DriveService(Client_secret=db.getCredentials())



class User(UserMixin):
    def __init__(self, user_id) -> None:
        self.id = user_id


@loginManager.user_loader
def load_user(user_id):
    return User(user_id)


@app.route('/', methods=['POST', 'GET'])
@app.route('/login', methods=['POST', "GET"])
def login():
    if request.method == 'POST':
        userData = request.form
        stats = db.login(username=userData.get('username'),
                         password=userData.get('password'))
        if stats.get('login') and stats.get('status') == 'success':
            login_user(User(stats.get('uid')))
            return redirect('/dashboard')
        else:
            return render_template('login.html', message=stats.get('message'))
    else:
        return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
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
            if res.get('status') == 'success':
                return redirect('/login')
            else:
                return render_template('signup.html', message=res.get('message'))
    return render_template('signup.html')


@loginManager.unauthorized_handler
def unauthorized():
    return redirect('/login')


@app.route("/dashboard")
@login_required
def main():
    displayData = drive.display()
    return render_template("index.html", data=displayData)


@app.route('/file/<filename>')
def get_file_by_name(filename):
    data = drive.get_file_by_name(filename)
    file_data = drive.download_file_by_id(file_id=data.get('id'))

    if file_data:
        response = Response(file_data, content_type='image/jpeg')
        response.headers['Content-Disposition'] = 'inline'
        return response
    else:
        return "File not found", 404


@app.route('/delete/<fileName>')
@login_required
def delete(fileName):
    data = drive.get_file_by_name(fileName)
    res = drive.deleteFile(file_id=data.get('id'))
    if res:
        return redirect('/refresh')
    else:
        return "error Deleting file"


@app.route('/refresh')
def refresh():
    drive.load()
    return redirect('/dashboard')


@app.route('/about')
@login_required
def storage():
    storage = drive.get_storage_usage()
    used = round(storage[0], 5)
    total = storage[1]
    value = (used / total) * 100
    return render_template('about.html', used=used, total=total, value=value)


@app.route('/upload', methods=['POST', 'GET'])
@login_required
def upload():
    
    if request.method == "POST":
        data = request.files.get('uploadFile')
        filename = secure_filename(data.filename)
        buffer = io.BytesIO()
        buffer.name = filename
        data.save(buffer)
        if utils.contains_file(drive.files, filename):
            return render_template('upload.html', msg="File Already Exists")
        else:
            res = drive.uploadFile(buffer, data.mimetype)
            # if res['status'] == 'success':
            #     os.remove(filePath)
            return render_template('upload.html', msg=res['message'])
        
    else:
        return render_template('upload.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('login')


if __name__ == "__main__":
    app.run(debug=True)
