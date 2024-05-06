from flask import session,jsonify,request
from Utilities import is_admin
from Config import configFirebase_admin
from firebase_admin import firestore
from Utilities import get_food_recommender_answer
from datetime import datetime

def diet_recommendation():
    if is_admin():
        return jsonify({"response": "unauthorized", "statusCode": 401, "data": "Admins cannot access this route"})
    elif 'user' in session:
        return "<h1>Welcome to food diet recommendation</h1>", 200
    else:
        return jsonify({"response": "unauthorized", "statusCode": 401, "data": "Login to use this feature"})
    

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
