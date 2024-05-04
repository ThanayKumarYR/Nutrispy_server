import os
import firebase_admin
from firebase_admin import credentials

def configEmail(app,mail):
    app.config["MAIL_SERVER"] = "smtps-proxy.fastmail.com"
    app.config["MAIL_PORT"] = 80
    app.config["MAIL_USERNAME"] = os.getenv("SECRETE_EMAIL")
    app.config["MAIL_PASSWORD"] = os.getenv("SECRETE_PASSWORD")
    app.config["MAIL_USE_TLS"] = False
    app.config["MAIL_USE_SSL"] = True
    mail.init_app(app)

def configFirebase():
    try:
        path =  os.getcwd() + "/key1.json"
        cred = credentials.Certificate(path)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        print(e)


