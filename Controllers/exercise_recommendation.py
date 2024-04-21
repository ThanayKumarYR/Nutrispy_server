from flask import session,jsonify

def exercise_recommendation():
    if 'user' not in session:
        return jsonify({"data":"Login to use this feature","login":False}),200
    return "<h1>Welcome to exercise recommedation</h1>",200