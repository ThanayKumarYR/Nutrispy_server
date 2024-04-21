from flask import request,jsonify
from flask_mailman import EmailMessage
import os

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
        return jsonify({"response":"success","status":200,"message":"email sent"})
    return "<h1>Contact-Email get request-response</h1>"