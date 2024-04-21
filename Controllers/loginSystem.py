from flask import request,session,jsonify
from firebase_admin import auth
from pyrebase import initialize_app
import os
import json

def login():
    if request.method == 'POST':
        email = request.json['email']
        password = request.json['password']
        print("email = "+email+", password = "+password)
        try:
            config = json.loads(os.getenv("FIREBASE"))
            firebase = initialize_app(config)
            authenticate = firebase.auth()
            user = auth.get_user_by_email(email=email)
            if user:
                auth_user =  authenticate.sign_in_with_email_and_password(email, password)
                session['user'] = auth_user['localId']
            return jsonify({"data":f"Successfully login, Welcome {auth_user['email']}","login":True}),200
        except Exception as e:
            return jsonify({"An error occured":e,"login":False}),404
            

def logout():
    if 'user' in session:
        session.pop('user')
        return jsonify({"data":"Successfully logged out","login":False}),200
    else:
        return jsonify({"data":"First login to log out !","login":False}),200
