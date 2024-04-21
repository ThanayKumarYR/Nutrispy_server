import os

def config(app,mail):
    app.config["MAIL_SERVER"] = "smtps-proxy.fastmail.com"
    app.config["MAIL_PORT"] = 80
    app.config["MAIL_USERNAME"] = str(os.getenv("SECRETE_EMAIL"))
    app.config["MAIL_PASSWORD"] = str(os.getenv("SECRETE_PASSWORD"))
    app.config["MAIL_USE_TLS"] = False
    app.config["MAIL_USE_SSL"] = True
    mail.init_app(app)

