from flask import session,jsonify
from Utilities import is_admin

def exercise_recommendation():
    if is_admin():
        return jsonify({"response": "unauthorized", "statusCode": 401, "data": "Admins cannot access this route"})
    elif 'user' in session:
        return "<h1>Welcome to exercise recommendation</h1>", 200
    else:
        return jsonify({"response": "unauthorized", "statusCode": 401, "data": "Login to use this feature"})

