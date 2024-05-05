from flask import request, session, jsonify
from Config import configPyrebase_auth, configFirebase_admin
import os
from firebase_admin import auth

def login():
    if request.method == 'POST':
        if 'user' in session:
            return jsonify({"response": "Failed", "statusCode": 400, "data": "User is already logged in"})
        
        email = request.json['email']
        password = request.json['password']
        
        try:
            authenticate = configPyrebase_auth()

            configFirebase_admin()
            user = auth.get_user_by_email(email=email)
            
            if user:
                try:
                    auth_user = authenticate.sign_in_with_email_and_password(user.email,password)
                except Exception as e:
                    return jsonify({"response":"Failed","statusCode":404,"data":"Incorrect password"})
                if user.email == os.getenv("ADMIN_EMAIL"):
                    session['user'] = os.getenv("ADMIN_SECRET")
                else:
                    session['user'] = auth_user['localId']
                    
                return jsonify({"response": "Success", "statusCode": 200, "data": f"Successfully logged in. Welcome {auth_user['email']}"})
            else:
                return jsonify({"response": "Failed", "statusCode": 404, "data": f"Invalid, No user with email id present {email}"})
        except Exception as e:
            return jsonify({"response": "Failed", "statusCode": 404, "data": e.args[0]})

            
def logout():
    if 'user' in session:
        session.pop('user')
        return jsonify({"response":"Success","statusCode":200,"data":"Successfully logged out"})
    else:
        return jsonify({"response":"Failed","statusCode":404,"data":"First login to log out !"})
    
