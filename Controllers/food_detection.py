from flask import session,jsonify

def food_detection():
    if 'user' not in session:
         return jsonify({"response":"unauthorized","statusCode":401,"data":"Login to use this feature"})
    return "<h1>Welcome to food detection</h1>",200