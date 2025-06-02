from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory, abort, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from tinydb import TinyDB, Query
from functools import wraps
import os
import logging
from logging.handlers import RotatingFileHandler
from app_cfg import (SECRET_KEY, UPLOAD_FOLDER, MAX_CONTENT_LENGTH, DB_FILE, 
                    SESSION_COOKIE_NAME, PERMANENT_SESSION_LIFETIME,
                    LOG_FILE, LOG_LEVEL, LOG_FORMAT)
import random
import string
from datetime import datetime, timedelta

app = Flask(__name__)

# Configure logging
def setup_logging():
    handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=1024 * 1024,  # 1MB
        backupCount=5
    )
    handler.setFormatter(logging.Formatter(LOG_FORMAT))
    app.logger.addHandler(handler)
    app.logger.setLevel(LOG_LEVEL)

setup_logging()

# Load configuration from app_cfg.py
app.secret_key = SECRET_KEY
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.config['SESSION_COOKIE_NAME'] = SESSION_COOKIE_NAME
app.config['PERMANENT_SESSION_LIFETIME'] = PERMANENT_SESSION_LIFETIME

# TinyDB setup
db = TinyDB(DB_FILE)
User = Query()

def generate_activation_code():
    return ''.join(random.choices(string.digits, k=ACTIVATION_CODE_LENGTH))
  
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            app.logger.warning('Unauthorized access attempt')
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('login'))
        
        # Check if account is activated
        user = db.search(User.id == session['user_id'])
        if user and not user[0].get('activated', True):
            session.pop('user_id', None)
            flash('Your account requires activation. Please log in with your activation code.', 'danger')
            return redirect(url_for('login'))
        
        return f(*args, **kwargs)
    return decorated_function
  
@app.route('/')
@login_required
def index():
    files = []
    upload_folder = app.config['UPLOAD_FOLDER']
    if os.path.exists(upload_folder):
        files = os.listdir(upload_folder)
    app.logger.info(f"User {session.get('user_id')} accessed index page")
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        app.logger.warning('No file selected for upload')
        flash('No file selected', 'danger')
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        app.logger.warning('Empty filename in upload attempt')
        flash('No file selected', 'danger')
        return redirect(url_for('index'))
    
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        app.logger.info(f"User {session.get('user_id')} uploaded file: {filename}")
        flash('File uploaded successfully', 'success')
    
    return redirect(url_for('index'))

@app.route('/download/<filename>')
@login_required
def download_file(filename):
    try:
        app.logger.info(f"User {session.get('user_id')} downloaded file: {filename}")
        return send_from_directory(
            app.config['UPLOAD_FOLDER'],
            filename,
            as_attachment=True
        )
    except FileNotFoundError:
        app.logger.error(f"File not found for download: {filename}")
        abort(404)

@app.route('/delete/<filename>')
@login_required
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        app.logger.info(f"User {session.get('user_id')} deleted file: {filename}")
        flash('File deleted successfully', 'success')
    else:
        app.logger.warning(f"Delete attempt failed - file not found: {filename}")
        flash('File not found', 'danger')
    return redirect(url_for('index'))

# Modified register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            app.logger.warning(f"Password mismatch during registration for: {username}")
            flash('Passwords do not match', 'danger')
            return redirect(url_for('register'))
        
        if db.search(User.username == username):
            app.logger.warning(f"Username already exists: {username}")
            flash('Username already exists', 'danger')
            return redirect(url_for('register'))
        
        activation_code = generate_activation_code()
        user_id = len(db) + 1
        
        db.insert({
            'id': user_id,
            'username': username,
            'password': generate_password_hash(password),
            'activation_code': activation_code,
            'activated': False,
            'activation_expires': (datetime.now() + timedelta(hours=ACTIVATION_CODE_EXPIRE_HOURS)).isoformat()
        })
        
        # Log the activation code (in production, you would email/SMS this)
        app.logger.info(f"New user registered: {username}. Activation code: {activation_code}")
        
        flash('Registration successful! Please check your activation code and log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

# Modified login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        activation_code = request.form.get('activation_code', '')
        
        user = db.search(User.username == username)
        if user:
            user = user[0]  # Get first match
            
            # Check if account needs activation
            if not user.get('activated', False):
                if activation_code != user.get('activation_code', ''):
                    app.logger.warning(f"Invalid activation code for user: {username}")
                    flash('Invalid activation code', 'danger')
                    return render_template('login.html', needs_activation=True)
                
                # Activate the account
                db.update({
                    'activated': True,
                    'activation_code': None,
                    'activation_expires': None
                }, User.username == username)
                app.logger.info(f"User account activated: {username}")
            
            # Verify password
            if check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                app.logger.info(f"User logged in: {username}")
                flash('Logged in successfully!', 'success')
                return redirect(url_for('index'))
        
        app.logger.warning(f"Failed login attempt for username: {username}")
        flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            app.logger.warning(f"Password mismatch during registration for: {username}")
            flash('Passwords do not match', 'danger')
            return redirect(url_for('register'))
        
        if db.search(User.username == username):
            app.logger.warning(f"Username already exists: {username}")
            flash('Username already exists', 'danger')
            return redirect(url_for('register'))
        
        user_id = len(db) + 1
        db.insert({
            'id': user_id,
            'username': username,
            'password': generate_password_hash(password)
        })
        session['user_id'] = user_id
        app.logger.info(f"New user registered: {username}")
        flash('Registration successful! You are now logged in.', 'success')
        return redirect(url_for('index'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    user_id = session.get('user_id')
    session.pop('user_id', None)
    app.logger.info(f"User logged out: {user_id}")
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    from app_cfg import HOST, PORT, DEBUG
    app.run(host=HOST, port=PORT, debug=DEBUG)
