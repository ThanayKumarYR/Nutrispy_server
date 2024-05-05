from flask import session
import os

def is_admin():
    if 'user' in session:
        return session['user'] == os.getenv("ADMIN_SECRET")
    return False
