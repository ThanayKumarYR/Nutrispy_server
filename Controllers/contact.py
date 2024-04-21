from flask import request,jsonify,session,redirect
from flask_mailman import EmailMessage
import os
from firebase_admin import firestore
from Config import configFirebase


def contactEmail():
    if(request.method == 'POST'): 
        name = request.json["name"]
        email = request.json["email"]
        number = request.json["number"]
        company = request.json["company"]
        message = request.json["message"]
        msg = EmailMessage(
            str(f"Hello, this is {name} from company {company if company else 'No company'}"),
            str(f'{message}.\nEmail me @ {email}\nCall me @ {number}'),
            str(os.getenv("SECRETE_EMAIL")),
            [str(os.getenv("SECRETE_BCC"))],
            [str(os.getenv("SECRETE_BCC")),str(os.getenv("SECRETE_BCC1")),str(os.getenv("SECRETE_BCC2")),str(os.getenv("SECRETE_BCC3"))],
            reply_to=[email]
        )
        msg.send()
        return jsonify({"response":"success","status":200,"data":"email sent"})
    return "<h1>Contact-Email get request-response</h1>"

def contactFirebase():
    if request.method == 'POST':
        configFirebase()
        db = firestore.client()
        data = request.json
        contact_ref = db.collection("contacts").document()
        contact_ref.set(data)
        return jsonify({"response": "success", "status": 200, "message": "email sent"})
    return "<h1>Contact get request-response</h1>"

def getContacts():
    if 'user' not in session:
        return jsonify({"data":"Login to use this feature","login":False}),200
    configFirebase()
    db = firestore.client()
    contacts_ref = db.collection("contacts").stream()
    contacts = [contact.to_dict() for contact in contacts_ref]
    if contacts:
        return jsonify({"response": "success", "status": 200, "data": contacts})
    else:
        return jsonify({"response": "success", "status": 200, "message": "No contacts found"})
