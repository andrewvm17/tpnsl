from flask import Flask
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("tpnsl-c0752-firebase-adminsdk-gstnb-2caeeab7f4.json")
firebase_admin.initialize_app(cred)

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(debug=True)
