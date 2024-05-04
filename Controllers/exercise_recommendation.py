from flask import session,jsonify

def exercise_recommendation():
    if 'user' not in session:
         return jsonify({"response":"unauthorized","statusCode":401,"data":"Login to use this feature"})
    return "<h1>Welcome to exercise recommedation</h1>",200