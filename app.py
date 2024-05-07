#basic template of flask to get started.
from flask import Flask,session
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
import atexit
from flask.sessions import SecureCookieSessionInterface
from itsdangerous import URLSafeTimedSerializer

class CustomSessionInterface(SecureCookieSessionInterface):
    def get_signing_serializer(self, app):
        if not app.secret_key:
            return None
        signer_kwargs = dict(
            key_derivation=self.key_derivation,
            digest_method=self.digest_method
        )
        return URLSafeTimedSerializer(app.secret_key, salt=self.salt, serializer=self.serializer, signer_kwargs=signer_kwargs)

mail = Mail()

load_dotenv()

Deliveredapp = Flask(__name__)
# CORS(Deliveredapp,resources={r"/*":{"origins":"https://thanaykumaryr.github.io/*"}})
CORS(Deliveredapp,resources={r"/*":{"origins":"*"}},supports_credentials=True, allow_headers="*")
Deliveredapp.session_interface = CustomSessionInterface()

# configEmail(Deliveredapp,mail)

Deliveredapp.secret_key = os.getenv("SECRET_KEY")

# Deliveredapp.config['SESSION_TYPE'] = 'redis'
# Deliveredapp.config['SESSION_REDIS'] = redis.from_url('redis://localhost:6379')

# Session(Deliveredapp)

routing(Deliveredapp)

app = Flask(__name__)

# Function to clear session when the application is terminated
def clear_session():
    session.clear()

# Register the clear_session function to be called when the application is terminated
atexit.register(clear_session)

app.wsgi_app = DispatcherMiddleware(NotFound,{"/api/v1":Deliveredapp})

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=30000,debug=True)

