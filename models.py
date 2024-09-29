from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(10))  # 'submitter' or 'volunteer'

class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(500), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    comments = db.Column(db.String(500))
    photo_url = db.Column(db.String(200))
    doc_url = db.Column(db.String(200))
    case_number = db.Column(db.String(20), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.Column(db.String(50))
    volunteer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    resolved = db.Column(db.Boolean, default=False)
