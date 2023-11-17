from flask import Flask, render_template, redirect, Response
from flask_cors import CORS
from GoogleDriveService import DriveService
from dbService import dbService


app = Flask(__name__)
cors = CORS(app)
db = dbService()
drive = DriveService(Client_secret=db.getCredentials())

@app.route("/")
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
    return redirect('/')

@app.route('/about')
def storage():
    storage = drive.get_storage_usage()
    return f"{storage}"

if __name__ == "__main__":
    app.run(debug=True)
