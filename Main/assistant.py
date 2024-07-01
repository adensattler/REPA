"""
Module Name: assistant.py

Description:
This module contains functions for setting up and interacting with a real estate assistant. 
The assistant leverages the OpenAI Assistants API to process property details provided in a JSON format.
For more information on Assistants API, refer to the documentation: 
https://platform.openai.com/docs/assistants/overview

The goal of this assistant is to act as a substitute for someone with deep knowledge of real estate,
capable of answering user inquiries regarding a property.

For setting up your OpenAI Key, please follow the instructions at: 
https://platform.openai.com/docs/quickstart/step-2-set-up-your-api-key

In our application there is ONE Assistant with many different threads (or conversations) tied to that assistant.
Each thread represents a conversation about a specific property. 
The references to these conversations are stored in threads_db since this functionality is not built in to the Assistants API.

Functions:
- upload_data(data): Uploads a file-like object to be used across various endpoints and returns an OpenAI File object.
- create_assistant(): Creates a Real Estate assistant tied to your OpenAI account.
- check_if_thread_exists(zpid): Checks if there's an existing thread for a given Zillow Property ID (ZPID).
- store_thread(zpid, thread_id): Stores a ZPID-thread ID pair in the database for thread management.
- generate_response(message_body, zpid): Generates a response to a message about a property, managing threads as needed.
- run_assistant(thread): Runs the assistant thread and returns the response.
- main(): Driver function to test the AI Assistant from the command line.

Usage:
1. Ensure you have set up your OpenAI API key.
2. Use the main() function to interact with the assistant via command line.
"""

from openai import OpenAI
import shelve
import time
import json
import re
import os
from dotenv import load_dotenv
from database import DatabaseManager
from config import API_KEY

load_dotenv()   # Load environment variables from .env file
ASSISTANT_ID = os.getenv("ASSISTANT_ID")

# Create the OpenAI client for API interactions
# NOTE: You MUST set your OPENAI_API_KEY in a .env file or this will error out!
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



# FUNCTIONS
# -----------------------------------------------------------------------------------------------------

# Upload file-like object that can be used across various endpoints. returns an OpenAI File object.
def upload_data(data):
    # Expected entry at `file` parameter to be bytes, an io.IOBase instance, PathLike or a tuple
    file = client.files.create(file=json.dumps(data).encode(), purpose="assistants")
    return file

# Creates a Real Estate assistant tied to your OpenAI account
def create_assistant():
    assistant = client.beta.assistants.create(
        name="Real Estate Advisor",
        instructions="""You are a highly knowledgeable real estate advisor that can assist others looking for information about a property. 
        Your role is to summarize extensive property data, extract key figures and data, and give advice on a property.
        Use your knowledge base to best respond to customer queries. 
        If you don't know the answer, simply say that the question is outside of your scope of knowledge.
        Be concise.""",
        tools=[{"type": "retrieval"}],
        model="gpt-3.5-turbo-1106",
        file_ids=[],
    )
    # In order for an assistant to handle files from threads, you MUST set the file_ids parameter to [].
    return assistant


# Thread Management Functions
# --------------------------------------------------------------
# DESC: These functions utilize the "shelve" library.
# Think of a shelf as a dictionary that persists on a filesystem
# We are using shelve to store the {zpid : thread_id} pair so we can "remember" current conversations.
# Note that thread creation is handled when generating a response.

# Returns thread_id from threads_db or None if DNE
def check_if_thread_exists(zpid):
    with shelve.open("threads_db") as threads_shelf:
        return threads_shelf.get(zpid, None)

# Adds a (zpid : thread_id) pair to threads_db
def store_thread(zpid, thread_id):
    with shelve.open("threads_db", writeback=True) as threads_shelf:
        threads_shelf[zpid] = thread_id


# Get a response to a message about a property!
def generate_response(message_body, zpid):
    # Check if there is already a thread_id for a zpid that is saved
    thread_id = check_if_thread_exists(zpid)

    # If there is no thread for a property, create one and store it
    if thread_id is None:
        # A new thread should be initialized with a file containing all the data on a property

        # 1.) get the property json data from the database
        db = DatabaseManager('zillow_listings.db')
        data_obj = json.loads(db.get_JSON(zpid))

        # 2.) convert the data to an OpenAI file object
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
    # YOU MUST CREATE AN ASSISTANT. You can do so by running the code below 
    # OR by making an assistant on the OPENAI Assistants dashboard
    # All threads are made from a SINGLE assistant and reference one assistant id.

    # If you create a NEW assistant you must update the new assistant id in the ASSISTANT_ID env variable.
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

