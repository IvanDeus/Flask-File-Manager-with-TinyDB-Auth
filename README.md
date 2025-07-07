# Flask-File-Manager-with-TinyDB-Auth
## Web-based Flask File Manager with TinyDB Authentication

A lightweight file management web application built with Flask, featuring:
- User authentication (login/register)
- File upload/download/delete operations
- Mobile-optimized responsive interface
- TinyDB-based user database
- Secure password hashing

## Features

- 📁 File management (upload, download, delete)
- 🔐 User authentication system
- 📱 Mobile-friendly interface
- 🛡️ Secure password storage
- ⚡ Lightweight and easy to deploy

## Requirements

- Python 3.7+
- Pip package manager

## Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/IvanDeus/Flask-File-Manager-with-TinyDB-Auth.git
cd Flask-File-Manager-with-TinyDB-Auth
```
### 2. Create and activate virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Configuration
Copy app_cfg.example.py to app_cfg.py:
```bash
cp app_cfg.example.py app_cfg.py
```
And edit app_cfg.py to customize:
> SECRET_KEY = 'your-very-secret-key'  # Change this!
> 
> DEBUG = False  # Set to False in production
> 
> PORT = 5000    # Change port if needed

### 5. Run the application
```bash
python app.py
```
The application will be available at:
http://localhost:5000 (or your configured port)

## First-Time Setup
- Access the application in your browser

- Register a new user account

- Log in with your credentials and activation code (from a local app.log file)

- Start uploading and managing files!

## Production Deployment
For production environments, consider:

Using Gunicorn or uWSGI as a WSGI server

Setting up Nginx or Apache as a reverse proxy

Changing SECRET_KEY to a strong random value

Setting DEBUG = False in app_cfg.py

Using a proper database system (SQLite/PostgreSQL/MySQL)

## License
MIT License - Free for personal and commercial use

## Troubleshooting
- Issue: File upload fails
  Solution: Check MAX_CONTENT_LENGTH in app_cfg.py and ensure sufficient permissions on static/uploaded_files/

- Issue: Database problems
  Solution: Delete users.json to reset all user accounts

2025 [ivan deus]
