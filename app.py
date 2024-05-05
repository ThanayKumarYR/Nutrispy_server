#basic template of flask to get started.
from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.exceptions import NotFound
from flask_cors import CORS
from dotenv import load_dotenv
from flask_mailman import Mail
import os
from Config import configEmail
from Routes import routing
import redis
from flask_session import Session

mail = Mail()

load_dotenv()

Deliveredapp = Flask(__name__)
# CORS(Deliveredapp,resources={r"/*":{"origins":"https://thanaykumaryr.github.io/*"}})
CORS(Deliveredapp,resources={r"/*":{"origins":"*"}})

configEmail(Deliveredapp,mail)

Deliveredapp.secret_key = os.getenv("SECRET_KEY")

# Deliveredapp.config['SESSION_TYPE'] = 'redis'
# Deliveredapp.config['SESSION_REDIS'] = redis.from_url('redis://localhost:6379')

# Session(Deliveredapp)

routing(Deliveredapp)

app = Flask(__name__)

app.wsgi_app = DispatcherMiddleware(NotFound,{"/api/v1":Deliveredapp})

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=30000,debug=True)

