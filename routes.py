import logging
from flask import render_template, request, redirect, url_for, flash, session, send_from_directory
from authlib.integrations.flask_client import OAuth
from werkzeug.utils import secure_filename
from app import app, db
import firebase_config
import os
import uuid
from datetime import datetime

# Set up basic logging
logging.basicConfig(level=logging.DEBUG)

# OAuth Configuration with Auth0
oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id=app.config['AUTH0_CLIENT_ID'],
    client_secret=app.config['AUTH0_CLIENT_SECRET'],
    api_base_url=f"https://{app.config['AUTH0_DOMAIN']}",
    access_token_url=f"https://{app.config['AUTH0_DOMAIN']}/oauth/token",
    authorize_url=f"https://{app.config['AUTH0_DOMAIN']}/authorize",
    client_kwargs={'scope': 'openid profile email'}
)

# Upload folder configuration
UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload path exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_user(email, username):
    user_data = {
        'username': username,
        'email': email,
        'role': 'submitter'
    }
    firebase_config.db.collection('users').add(user_data)

@app.route('/')
def home():
    google_maps_api_key = app.config["GOOGLE_MAPS_API_KEY"]
    username = session.get('username', 'Unnamed User')
    issues_ref = firebase_config.db.collection('issues')
    issues_stream = issues_ref.where('resolved', '==', False).stream()
    issues = [{**doc.to_dict(), 'id': doc.id} for doc in issues_stream]
    return render_template('home.html', google_maps_api_key=google_maps_api_key, username=username, issues=issues)

@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri='https://communityoutreachnet.work/login/callback')

@app.route('/login/callback')
def authorize():
    token = auth0.authorize_access_token()
    if token is None:
        logging.error('Authorization failed: Token is None')
        flash('Authorization failed')
        return redirect(url_for('home'))

    logging.debug('Token: %s', token)
    user_info = auth0.get('userinfo').json()
    logging.debug('User Info: %s', user_info)

    email = user_info.get('email')
    username = user_info.get('name')

    if email is None or username is None:
        logging.error('Missing user info: email or username is None')
        flash('Failed to retrieve user information')
        return redirect(url_for('home'))

    users_ref = firebase_config.db.collection('users')
    query_ref = users_ref.where('email', '==', email).stream()
    user = None
    for doc in query_ref:
        user = doc.to_dict()
        break

    if not user:
        logging.debug('Creating new user: %s', email)
        create_user(email, username)

    session['user'] = email
    session['username'] = username
    session['token'] = token
    flash('You are logged in as ' + username)
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('username', None)
    session.pop('token', None)
    flash('You have been logged out')
    return redirect(url_for('home'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user' not in session:
        flash('You need to be logged in to view this page')
        return redirect(url_for('login'))

    user_email = session['user']
    users_ref = firebase_config.db.collection('users')
    query_ref = users_ref.where('email', '==', user_email).stream()
    user = None
    doc_id = None
    for doc in query_ref:
        user = doc.to_dict()
        doc_id = doc.id
        break

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        user_update_data = {
            'username': username,
            'email': email
        }
        users_ref.document(doc_id).update(user_update_data)
        session['username'] = username
        flash('Profile updated successfully')
        return redirect(url_for('profile'))

    issues_ref = firebase_config.db.collection('issues')
    resolved_issues_stream = issues_ref.where('resolved', '==', True).where('email', '==', user_email).stream()
    resolved_issues = [doc.to_dict() for doc in resolved_issues_stream]

    return render_template('profile.html', user=user, resolved_issues=resolved_issues)

@app.route('/report_issue', methods=['GET', 'POST'])
def report_issue():
    if 'user' not in session:
        flash('You need to be logged in to report an issue')
        return redirect(url_for('login'))

    if request.method == 'POST':
        description = request.form['description']
        place = request.form['place']
        case_number = str(uuid.uuid4().hex[:6].upper())

        issue_data = {
            'description': description,
            'place': place,
            'case_number': case_number,
            'resolved': False,
            'email': session['user'],
            'username': session['username']
        }

        if 'attachment' in request.files:
            file = request.files['attachment']
            if file and allowed_file(file.filename):
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                ext = file.filename.rsplit('.', 1)[1].lower()
                filename = secure_filename(f"{timestamp}.{ext}")
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                issue_data['attachment_url'] = f"uploads/{filename}"

        firebase_config.db.collection('issues').add(issue_data)
        flash('Issue reported successfully')
        return redirect(url_for('home'))
    return render_template('report_issue.html', google_maps_api_key=app.config['GOOGLE_MAPS_API_KEY'])

@app.route('/manage_issues', methods=['GET'])
def manage_issues():
    issues_ref = firebase_config.db.collection('issues')
    query_ref = issues_ref.where('resolved', '==', False).stream()
    issues = [doc.to_dict() for doc in query_ref]
    return render_template('manage_issues.html', issues=issues)

@app.route('/resolve_issue/<string:case_number>', methods=['POST'])
def resolve_issue(case_number):
    issues_ref = firebase_config.db.collection('issues')
    query_ref = issues_ref.where('case_number', '==', case_number).stream()
    for doc in query_ref:
        issues_ref.document(doc.id).update({'resolved': True})
        break
    flash('Issue resolved successfully')
    return redirect(url_for('manage_issues'))

# Serve uploaded files from 'static/uploads'
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
