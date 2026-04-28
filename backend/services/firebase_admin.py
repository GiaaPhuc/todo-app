import firebase_admin
from firebase_admin import credentials
import os
from dotenv import load_dotenv

load_dotenv()


def init_firebase():
    if not firebase_admin._apps:
        cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH", "./firebase-adminsdk.json")
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
