#basic template of flask to get started.

from flask import Flask,request,jsonify
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.exceptions import NotFound
from flask_cors import CORS
import os
from dotenv import load_dotenv
from flask_mailman import Mail,EmailMessage

mail = Mail()

load_dotenv()

app1 = Flask(__name__)
CORS(app1,resources={r"/*":{"origins":"https://thanaykumaryr.github.io/*"}})
# CORS(app1,resources={r"/*":{"origins":"*"}})

app1.config["MAIL_SERVER"] = "smtps-proxy.fastmail.com"
app1.config["MAIL_PORT"] = 80
app1.config["MAIL_USERNAME"] = str(os.getenv("SECRETE_EMAIL"))
app1.config["MAIL_PASSWORD"] = str(os.getenv("SECRETE_PASSWORD"))
app1.config["MAIL_USE_TLS"] = False
app1.config["MAIL_USE_SSL"] = True
mail.init_app(app1)

@app1.route('/',methods=['GET'])
def index():
    return f"<h1>{str(os.getenv('SECRETE_EMAIL'))}</h1>"

@app1.route('/contact',methods=['GET','POST'])
def contact():
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

app = Flask(__name__)

app.wsgi_app = DispatcherMiddleware(NotFound,{"/api/v1":app1})

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=30000,debug=True)

