"""
Module Name: assistant.py

Description:
This module contains functions for setting up, and interacting with a real estate assistant.
It utilizes the OpenAI Assistants API to pass a model/llm a property details json file.
Here is the link to the Assistants documentation: https://platform.openai.com/docs/assistants/overview

The goal of assistant is to serve as a stand-in for someone more knowledgeable than the can user about real estate.
As a result, they should be about to answer any questions a user may have about a property.

Functions:
- 

Usage:
"""

from openai import OpenAI
import os
import shelve
import time
import sys
import json
import re

sys.path.append('../Main')
from data_acquisition import get_property_detail
from database import DatabaseManager
from config import API_KEY

# === Hardcoded assistant id ===
ASSISTANT_ID = "asst_jzMUaqyzjNcKF4oAKbzLYYjh"  # we want ONE assistant with many different threads running off of it for specific applications!

client = OpenAI()
# NOTE: OpenAI() defaults to getting your key using os.environ.get("OPENAI_API_KEY") and will error out if not set in your system.
# if you have the key set under a different name or not at all, you can pass the key as a parameter instead:
# client = OpenAI(api_key="YOUR_API_KEY_HERE")


# HELPER FUNCTIONS
# ---------------------------------------------------------------------

# Upload file-like object that can be used across various endpoints. returns an OpenAI File object.
def upload_data(data):
    # Expected entry at `file` parameter to be bytes, an io.IOBase instance, PathLike or a tuple
    file = client.files.create(file=json.dumps(data).encode(), purpose="assistants")
    return file

# Creates an assistant tied to your OpenAI account
def create_assistant():
    assistant = client.beta.assistants.create(
        name="Real Estate Advisor",
        instructions="""You are a highly knowledgeable real estate advisor that can assist others looking for information about a property. 
        Your role is to summarize extensive property data, extract key figures and data, and give advice on a property.
        Use your knowledge base to best respond to customer queries. 
        If you don't know the answer, simply say that the question is outside of your scope of knowledge.
        Be concise.""",
        tools=[{"type": "retrieval"}],
        model="gpt-4-1106-preview",
        file_ids=[],
    )
    return assistant

# --------------------------------------------------------------
# Thread Management Functions
# --------------------------------------------------------------
# Returns thread_id or None if DNE
def check_if_thread_exists(zpid):
    with shelve.open("threads_db") as threads_shelf:
        return threads_shelf.get(zpid, None)

# Adds a (zpid : thread_id) pair to the threads_db
def store_thread(zpid, thread_id):
    with shelve.open("threads_db", writeback=True) as threads_shelf:
        threads_shelf[zpid] = thread_id

# DESC: These functions utilize the "shelve" library.
# Think of a shelf as a dictionary that persists on a filesystem
# We are using them to store the thread_id corresponding to each zpid!  
# Notice there is no create thread function because its just "thread = client.beta.threads.create()"


# --------------------------------------------------------------
# Get a response to a message about a property!
# --------------------------------------------------------------
def generate_response(message_body, zpid):
    # Check if there is already a thread_id for a zpid that is saved
    thread_id = check_if_thread_exists(zpid)

    # If there is no thread for a property, create one and store it
    if thread_id is None:
        # A new thread should be initialized with a file containing all the data on a property

        # 1.) get the property json data from the database
        db = DatabaseManager('zillow_listings.db')
        data_obj = json.loads(db.get_JSON(zpid))

        # 2.) convert the json to an OpenAI file object
        # file = client.files.create(file=json.dumps(json_obj).encode(), purpose="assistants")
        file = upload_data(data_obj)

        # 3.) create the thread. pass the thread the file object!
        print(f"Creating new thread for zpid {zpid}")
        thread = client.beta.threads.create(    
            messages=[
                {
                "role": "user",
                "content": "Utilize this file containing data on a property to answer any questions a user may have on the property going forward.",
                "file_ids": [file.id]
                }
            ]
        ) 
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

    # RUN THE THREAD AND RETURN ITS RESPONSE
    new_message = run_assistant(thread)
    print(f"To User:", new_message)     # logging the response for debugging
    return new_message

# --------------------------------------------------------------
# Run the assistant!
# --------------------------------------------------------------
def run_assistant(thread):
    # Retrieve the Assistant
    assistant = client.beta.assistants.retrieve(ASSISTANT_ID)

    # Run the provided thread
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    # Wait for the API/LLM to finish running
    while run.status != "completed":
        # Be nice to the API
        time.sleep(0.5)
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

    # Retrieve the the messages in the thread and get the most recent response
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    new_response = messages.data[0].content[0].text.value

    # Use re.sub() to remove the matched source tags from the API response
    pattern = r'【\d+†source】'
    cleaned_response = re.sub(pattern, '', new_response)

    return cleaned_response


def main():
    # This driver is used to test the AI Assistant from the command line.
    
    # INSTRUCTIONS:
    # STEP 1: Pick a zpid of a property that is already in the database (specifically the propertyDetails table)
    # STEP 2: Put that zpid in the second field of the generate_response function below.
    # STEP 3: Run the program.


    # NOTE: 
    # The assistant id is HARDCODED. All threads are made from this single assistant.
    # If you create a NEW assistant you must update the new assistant id in the ASSISTANT_ID variable.
    # i.e. uncomment the code below, run it, then copy-paste the printed id into ASSISTANT_ID.

    # Create an assistant (Uncomment this to create a new assistant)
    # assistant = create_assistant()
    # assistant_id = assistant.id
    # print(assistant_id)

    
    while True:
        user_input = input("Please enter your message (or 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break
        else:
            print()
            generate_response(user_input, "247389523")
                #         INSERT ZPID HERE ^^^^^^^^


if __name__ == "__main__":
    main()

