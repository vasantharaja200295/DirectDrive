from flask import Flask
from dotenv import load_dotenv

load_dotenv('.env')

app = Flask(__name__)

@app.route("/")
def main():
    return "Working"


if __name__ == "__main__":
    app.run(debug=True)