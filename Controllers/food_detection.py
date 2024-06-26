from flask import session,jsonify
from Utilities import is_admin

def food_detection():
    if is_admin():
        return jsonify({"response": "unauthorized", "statusCode": 401, "data": "Admins cannot access this route"})
    elif 'user' in session:
        return "<h1>Welcome to food detection</h1>", 200
    else:
        return jsonify({"response": "unauthorized", "statusCode": 401, "data": "Login to use this feature"})