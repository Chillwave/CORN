import firebase_admin
from firebase_admin import credentials, firestore

# Correct relative path to the service account key file
cred = credentials.Certificate("secrets/communityoutreachnetwork-93747-firebase-adminsdk-y2lmo-1a9a85fd2b.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
