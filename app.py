#basic template of flask to get started.

from flask import Flask,request 
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.exceptions import NotFound
from flask_cors import CORS

app = Flask(__name__)
CORS(app,resources={r"/*":{"origins":"https://thanaykumaryr.github.io/*"}})

@app.route('/contact',methods=['GET','POST'])
def index():
    if(request.method == 'POST'): 
        name = request.json["name"]
        email = request.json["email"]
        number = request.json["number"]
        company = request.json["company"]
        message = request.json["message"]
        print(f"{name} working with {company if company else 'No Comapany'} has email {email} and number {number} with message: \n'{message}.'")
        return str(f"{name} working with {company if company else 'No Comapany'} has email {email} and number {number} with message: \n'{message}.'")
    return "<h1>Welcome to Nutrispy Server</h1>"

hostedApp = Flask(__name__)

hostedApp.wsgi_app = DispatcherMiddleware(NotFound,{"/api/v1":app})

# if __name__ == "__main__":
#     hostedApp.run(port=30000,host="0.0.0.0",debug=True)

