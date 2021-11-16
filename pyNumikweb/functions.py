import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from pyNumikweb.settings import STATIC_DIR

creds = os.path.join(STATIC_DIR, 'numik-app-firebase-adminsdk-wqov8-87f8076bdb.json')

def api():
    
    if not firebase_admin._apps:
        cred = credentials.Certificate(creds)
        firebase_admin.initialize_app(cred)
        
    db = firestore.client()
    
    return db
