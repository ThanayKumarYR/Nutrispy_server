#basic template of flask to get started.

from flask import Flask,request 
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.exceptions import NotFound
from flask_cors import CORS

app1 = Flask(__name__)
CORS(app1,resources={r"/*":{"origins":"https://thanaykumaryr.github.io/*"}})

@app1.route('/',methods=['GET'])
def index():
    return "<h1>Welcome to Nutrispy Server</h1>"

@app1.route('/contact',methods=['GET','POST'])
def contact():
    if(request.method == 'POST'): 
        name = request.json["name"]
        email = request.json["email"]
        number = request.json["number"]
        company = request.json["company"]
        message = request.json["message"]
        print(f"{name} working with {company if company else 'No Comapany'} has email {email} and number {number} with message: \n'{message}.'")
        return str(f"{name} working with {company if company else 'No Comapany'} has email {email} and number {number} with message: \n'{message}.'")

app = Flask(__name__)

app.wsgi_app = DispatcherMiddleware(NotFound,{"/api/v1":app1})

