import pyrebase

config = {
    "apiKey": "YOUR_API_KEY",
    "authDomain": "YOUR_AUTH_DOMAIN",
    "projectId": "YOUR_PROJECT_ID",
    "storageBucket": "YOUR_STORAGE_BUCKET",
    "messagingSenderId": "YOUR_MESSAGING_SENDER_ID",
    "appId": "YOUR_APP_ID",
    "databaseURL": "YOUR_DATABASE_URL"
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

class FirebaseService:
    def save_user_data(self, user_data):
        db.child("users").push(user_data)