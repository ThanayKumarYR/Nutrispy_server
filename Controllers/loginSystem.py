from flask import request, session, jsonify
from pyrebase import initialize_app
import os
import json
def login():
    if request.method == 'POST':
        if 'user' in session:
            return jsonify({"response": "Failed", "statusCode": 400, "data": "User is already logged in"})
        
        email = request.json['email']
        password = request.json['password']
        
        try:
            cred = json.loads(os.getenv("FIREBASE"))
            firebase = initialize_app(cred)
            authenticate = firebase.auth()
            
            
            auth_user = authenticate.sign_in_with_email_and_password(email, password)
            session['user'] = auth_user['localId']
                
            return jsonify({"response": "Success", "statusCode": 200, "data": f"Successfully logged in. Welcome {auth_user['email']}"})
        
        except Exception as e:
            return jsonify({"response": "Failed", "statusCode": 404, "data": e.args[0]})

            
def logout():
    if 'user' in session:
        session.pop('user')
        return jsonify({"response":"Success","statusCode":200,"data":"Successfully logged out"})
    else:
        return jsonify({"response":"Failed","statusCode":404,"data":"First login to log out !"})
