# Flask-File-Manager-with-TinyDB-Auth
## Flask File Manager with TinyDB Authentication

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
Edit app_cfg.py to customize (just copy app_cfg.example.py):

```python
SECRET_KEY = 'your-very-secret-key'  # Change this!
DEBUG = False  # Set to False in production
PORT = 5000    # Change port if needed
```
### 5. Run the application
```bash
python app.py
```
The application will be available at:
http://localhost:5000 (or your configured port)
