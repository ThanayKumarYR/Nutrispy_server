from flask import session,jsonify

def check_session():
    if 'user' in session:
        return jsonify({"User ID" : session['user']})
    else:
        return jsonify({"User ID" : None})