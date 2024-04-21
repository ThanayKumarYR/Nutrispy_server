import os

def home():
    return f"<h1>{str(os.getenv('SECRETE_EMAIL'))}</h1>"