"""
Module Name: assistant_flask.py

Description:
This module contains functions for setting up, and interacting with a real estate assistant.
It utilizes the OpenAI Assistants API to pass a model/llm a property details json file.
Here is the link to the Assistants documentation: https://platform.openai.com/docs/assistants/overview

The goal of assistant is to serve as a stand-in for someone more knowledgeable than the can user about real estate.
As a result, they should be about to answer any questions a user may have about a property.
"""

from openai import OpenAI
import os
import shelve
import time


client = OpenAI()
# defaults to getting the key using os.environ.get("OPENAI_API_KEY") and will error out if not set in your system.
# if you have the key set under a different name or not at all, you can pass the key as a parameter:
# client = OpenAI(api_key="YOUR_API_KEY_HERE")

# HELPER FUNCTIONS
# ---------------------------------------------------------------------

# Upload file
def upload_file(path):
    # Upload a file with an "assistants" purpose
    file = client.files.create(file=open(path, "rb"), purpose="assistants")
    return file

def create_assistant(file):
    assistant = client.beta.assistants.create(
        name="Real Estate Advisor",
        instructions="""You are a highly knowledgeable real estate advisor that can assist others looking for information about a property. 
        Your role is to summarize extensive property data, extract key figures and data, and give advice on a property.
        Use your knowledge base to best respond to customer queries. 
        If you don't know the answer, say simply that you cannot help with question.
        Be concise.""",
        tools=[{"type": "retrieval"}],
        model="gpt-4-1106-preview",
        file_ids=[file.id],
    )
    return assistant

# --------------------------------------------------------------
# Thread Management Functions
# --------------------------------------------------------------
def check_if_thread_exists(zpid):
    with shelve.open("threads_db") as threads_shelf:
        return threads_shelf.get(zpid, None)

def store_thread(zpid, thread_id):
    with shelve.open("threads_db", writeback=True) as threads_shelf:
        threads_shelf[zpid] = thread_id

# DESC: These functions utilize the "shelve" library.
# Think of a shelf as a dictionary that persists on a filesystem
# We are using them to store our threads for each zpid!  
# notice there is no create thread func because its super easy( see generate_response) 


# --------------------------------------------------------------
# Get a response to a message!
# --------------------------------------------------------------
def generate_response(message_body, zpid):
    # Check if there is already a thread_id for the wa_id
    thread_id = check_if_thread_exists(zpid)

    # If there is no thread for a property, create one and store it
    if thread_id is None:
        print(f"Creating new thread for zpid {zpid}")
        thread = client.beta.threads.create()
        store_thread(zpid, thread.id)
        thread_id = thread.id

    # Otherwise, retrieve the existing thread from the shelf
    else:
        print(f"Retrieving existing thread for zpid {zpid}")
        thread = client.beta.threads.retrieve(thread_id)

    # Add message to thread
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message_body,
    )

    # RUN THE ASSISTANT AND RETURN ITS RESPONSE
    new_message = run_assistant(thread)
    print(f"To User:", new_message)
    return new_message

# --------------------------------------------------------------
# Run the assistant!
# --------------------------------------------------------------
def run_assistant(thread):
    # Retrieve the Assistant
    assistant = client.beta.assistants.retrieve(assistant_id)

    # Run the assistant
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    # Wait for completion
    while run.status != "completed":
        # Be nice to the API
        time.sleep(0.5)
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    # Retrieve the Messages
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    new_message = messages.data[0].content[0].text.value
    return new_message


# DRIVER
# ------------------------------------------------------------------------------------------
# STEP 1: Upload a file to OpenAI embeddings
filepath = os.path.join("property_details.json")
file_object = upload_file(filepath)


# STEP 2: Create your assistant
# We want ONE assistant with many different threads running off of it for specific applications!
# assistant = create_assistant(file_object)
# assistant_id = assistant.id
assistant_id = 'asst_iAw4avGg18DWqV7zf9zVyvif'

# message = 'Testing. Please respond with "Yes".'
# print(generate_response(message, zpid='123'))