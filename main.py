from flask import Flask, render_template, redirect, Response
from dotenv import load_dotenv
from flask_cors import CORS
from GoogleDriveService import DriveService


load_dotenv('.env')

app = Flask(__name__)
cors = CORS(app)

drive = DriveService()

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

if __name__ == "__main__":
    app.run(debug=True)
