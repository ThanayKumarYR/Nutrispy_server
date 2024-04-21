#basic template of flask to get started.

from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.exceptions import NotFound
from flask_cors import CORS
from dotenv import load_dotenv
from flask_mailman import Mail

from Config import config
from Routes import routing

mail = Mail()

load_dotenv()

Deliveredapp = Flask(__name__)
# CORS(app1,resources={r"/*":{"origins":"https://thanaykumaryr.github.io/*"}})
CORS(Deliveredapp,resources={r"/*":{"origins":"*"}})

config(Deliveredapp,mail)

routing(Deliveredapp)

app = Flask(__name__)

app.wsgi_app = DispatcherMiddleware(NotFound,{"/api/v1":Deliveredapp})

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=30000,debug=True)

