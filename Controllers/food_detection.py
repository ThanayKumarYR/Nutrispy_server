from flask import session,jsonify

def food_detection():
    if 'user' not in session:
        return jsonify({"data":"Login to use this feature","login":False}),200
    return "<h1>Welcome to food detection</h1>",200