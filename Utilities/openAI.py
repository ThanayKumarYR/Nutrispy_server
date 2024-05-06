import openai 
import os
import time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI API
# openai.api_key = os.getenv("OPENAI_API")


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

# Function to query OpenAI API and get answer
def get_openai_answer(question):
    # Send the user's question to the OpenAI API
    response = openai.Completion.create(
        engine="text-davinci-004",  # Use the GPT-4 Turbo model for responses
        prompt=question,
        max_tokens=50  # Set the maximum length of the answer
    )
    
    # Extract and return the generated answer
    answer = response.choices[0].text.strip()
    return answer

def get_demo_answer(question):
    if question != None and question != "":
        answer = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur."

        return answer