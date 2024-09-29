from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Initialize Firebase and load environment variables
import firebase_config

load_dotenv()

app = Flask(__name__, template_folder="templates")
CORS(app)

# Load configs from .env
app.config["AUTH0_CLIENT_ID"] = os.getenv("AUTH0_CLIENT_ID")
app.config["AUTH0_CLIENT_SECRET"] = os.getenv("AUTH0_CLIENT_SECRET")
app.config["AUTH0_DOMAIN"] = os.getenv("AUTH0_DOMAIN")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "mysecret")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///community.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["GOOGLE_MAPS_API_KEY"] = os.getenv("GOOGLE_MAPS_API_KEY")

db = SQLAlchemy(app)
ma = Marshmallow(app)

from routes import *

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
