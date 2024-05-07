from flask import Flask,session,request,jsonify
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.exceptions import NotFound
from flask_cors import CORS
from dotenv import load_dotenv
import os
import atexit
import firebase_admin
import pyrebase
from firebase_admin import firestore,auth,credentials
import json
import time
from openai import OpenAI
import re
import datetime


load_dotenv()

def count_tokens(sentence):
    # Define a regular expression pattern to identify tokens
    pattern = r'\w+|[^\w\s]'

    # Use the pattern to find all tokens in the sentence
    tokens = re.findall(pattern, sentence)

    # Return the count of tokens
    return len(tokens)

def configFirebase_admin():
    try:
        path =  os.getcwd() + "/key1.json"
        cred = credentials.Certificate(path)
        return firebase_admin.initialize_app(cred)
    except Exception as e:
        print(e)

def configPyrebase_auth():
    cred = json.loads(os.getenv("FIREBASE"))
    firebase =  pyrebase.initialize_app(cred)
    return firebase.auth()

def is_admin():
    if 'user' in session:
        return session['user'] == os.getenv("ADMIN_SECRET")
    return False

def get_food_recommender_answer(question):
    # Enter your Assistant ID here.
    ASSISTANT_ID = os.getenv("ASSISTANT_ID")
    # Make sure your API key is set as an environment variable.
    client = OpenAI()
    # Create a thread with a message.
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                # Update this with the query you want to use.
                "content": question,
            }
        ]
    )
    # Submit the thread to the assistant (as a new run).
    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=ASSISTANT_ID)
    print(f"👉 Run Created: {run.id}")
    # Wait for run to complete.
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        print(f"🏃 Run Status: {run.status}")
        time.sleep(1)
    else:
        print(f"🏁 Run Completed!")
    # Get the latest message from the thread.
    message_response = client.beta.threads.messages.list(thread_id=thread.id)
    messages = message_response.data
    # Print the latest message.
    latest_message = messages[0]
    return latest_message.content[0].text.value

Deliveredapp = Flask(__name__)
CORS(Deliveredapp,resources={r"/*":{"origins":"*"}})

Deliveredapp.secret_key = os.getenv("SECRET_KEY")

@Deliveredapp.route('/',methods=['GET'])
def home():
    return f"<h1>Welcome to nutrispy !</h1>",200


@Deliveredapp.route('/contact',methods=['POST'])
def contactFirebase():
    if request.method == 'POST':
        configFirebase_admin()
        db = firestore.client()
        data = request.json
        contact_ref = db.collection("contacts").document()
        contact_ref.set(data)
        return jsonify({"response": "Success", "statusCode": 201, "data": "Data as been sent"})


@Deliveredapp.route('/contact', methods=['GET','DELETE'])
def contact_operations():
    if not is_admin():
        return jsonify({"response": "unauthorized", "statusCode": 401, "data": "Admin privileges required"})
    
    configFirebase_admin()
    db = firestore.client()
    
    if request.method == 'GET':
        contacts_ref = db.collection("contacts").stream()
        contacts = [{"id": contact.id, **contact.to_dict()} for contact in contacts_ref]
        if contacts:
            return jsonify({"response": "success", "statusCode": 200, "data": contacts})
        else:
            return jsonify({"response": "Failed", "statusCode": 404, "data": "No contacts found"})
    
    elif request.method == 'DELETE':
        contacts_ref = db.collection("contacts")
        contacts = contacts_ref.stream()
        for contact in contacts:
            contact.reference.delete()
        return jsonify({"response": "success", "status": 200, "data": "All contacts deleted successfully"}) 


@Deliveredapp.route('/contact/<contact_id>', methods=['DELETE'])
def deleteContact(contact_id):
    if not is_admin():
        return jsonify({"response": "unauthorized", "statusCode": 401, "data": "Admin privileges required"})
    
    configFirebase_admin()
    db = firestore.client()
    contact_ref = db.collection("contacts").document(contact_id)
    contact = contact_ref.get()
    if contact.exists:
        contact_ref.delete()
        return jsonify({"response": "success", "status": 200, "message": "Contact deleted successfully"})
    else:
        return jsonify({"response": "failure", "status": 404, "message": "Contact not found"})

@Deliveredapp.route('/login',methods=['POST'])
def login():
    if request.method == 'POST':
        if 'user' in session:
            return jsonify({"response": "Failed", "statusCode": 400, "data": "User is already logged in"})
        
        email = request.json['email']
        password = request.json['password']
        
        try:
            authenticate = configPyrebase_auth()

            configFirebase_admin()
            user = auth.get_user_by_email(email=email)
            
            if user:
                try:
                    auth_user = authenticate.sign_in_with_email_and_password(user.email,password)
                    if user.email == os.getenv("ADMIN_EMAIL"):
                        session['user'] = os.getenv("ADMIN_SECRET")
                    else:
                        session['user'] = auth_user['localId']
                    # Store user data in Firestore
                    db = firestore.client()
                    user_ref = db.collection('users').document(auth_user['localId'])
                    user_doc = user_ref.get()
                    if not user_doc.exists:
                        user_ref.set({
                            'email': email,
                            'uid': auth_user['localId']
                        })
                    return jsonify({"response": "Success", "statusCode": 200, "data": f"Successfully logged in. Welcome {auth_user['email']}"})
                except Exception as e:
                    return jsonify({"response":"Failed","statusCode":404,"data":"Incorrect password"})
            else:
                return jsonify({"response": "Failed", "statusCode": 404, "data": f"Invalid, No user with email id present {email}"})
        except Exception as e:
            return jsonify({"response": "Failed", "statusCode": 404, "data": e.args[0]})
@Deliveredapp.route('/logout',methods=['GET'])  
def logout():
    if 'user' in session:
        session.pop('user')
        return jsonify({"response":"Success","statusCode":200,"data":"Successfully logged out"})
    else:
        return jsonify({"response":"Failed","statusCode":404,"data":"First login to log out !"})
    
  
@Deliveredapp.route('/detect',methods=['GET'])
def food_detection():
    if is_admin():
        return jsonify({"response": "unauthorized", "statusCode": 401, "data": "Admins cannot access this route"})
    elif 'user' in session:
        return "<h1>Welcome to food detection</h1>", 200
    else:
        return jsonify({"response": "unauthorized", "statusCode": 401, "data": "Login to use this feature"})

@Deliveredapp.route('/recommend',methods=['GET','POST'])
def recommedation():
    if is_admin():
        return jsonify({"response": "unauthorized", "statusCode": 401, "data": "Admins cannot access this route"})
    elif 'user' not in session:
        return jsonify({"response": "Failed", "statusCode": 401, "data": "User not logged in"})
    
    user_id = session['user']

    configFirebase_admin()
    db = firestore.client()
    
    if request.method == 'POST':
        # Handle POST request to store conversation
        question = request.json["question"]
        if(count_tokens(question)>100):
            return jsonify({"response": "Failed", "statusCode": 404,"data": "Request cannot exceed 100 tokens."})
        answer = get_food_recommender_answer(question=str(question))
        conversation = {
            "question" : question,
            "answer" : answer,
            "timestamp": datetime.now()
        }
        
        # Get reference to the user's conversations collection
        user_conv_ref = db.collection('users').document(user_id).collection('conversations')
        
        # Add the new conversation
        new_conv_ref = user_conv_ref.add(conversation)
        
        # Query the user's conversations and order by timestamp in descending order
        user_conv_query = user_conv_ref.order_by('timestamp', direction=firestore.Query.DESCENDING).limit(11)  # Fetch 11 to check for excess
        
        # Get the latest conversations
        latest_conversations = user_conv_query.get()
        
        # If there are more than 10 conversations, delete the excess ones
        if len(latest_conversations) > 10:
            excess_conversations = latest_conversations[10:]
            for conv in excess_conversations:
                conv.reference.delete()
        
        return jsonify({"response": "Success", "statusCode": 200, "data": "Conversation stored successfully"})
    
    elif request.method == 'GET':
        # Handle GET request to fetch last 10 conversations
        # Get reference to the user's conversations collection
        user_conv_ref = db.collection('users').document(user_id).collection('conversations')
        # print(user_conv_ref)
        # # Query the user's conversations and order by timestamp in descending order
        user_conv_query = user_conv_ref.order_by('timestamp').limit(10)
        # print(user_conv_ref)
        # # Get the latest 10 conversations
        latest_conversations = user_conv_query.stream()
        # print(latest_conversations)
        conversations_data = [{"id": conv.id, **conv.to_dict()} for conv in latest_conversations]
        
        
        return jsonify({"response": "Success", "statusCode": 200, "data": conversations_data})

@Deliveredapp.route('/check_session')
def check_session():
    if 'user' in session:
        return jsonify({"User ID" : session['user']})
    else:
        return jsonify({"User ID" : None})

app = Flask(__name__)

# Function to clear session when the application is terminated
def clear_session():
    session.clear()

# Register the clear_session function to be called when the application is terminated
atexit.register(clear_session)

app.wsgi_app = DispatcherMiddleware(NotFound,{"/api/v1":Deliveredapp})

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=30000,debug=True)

