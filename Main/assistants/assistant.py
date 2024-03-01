"""
Module Name: assistant.py

Description:
This module contains functions for setting up, and interacting with a real estate assistant.
It utilizes the OpenAI Assistants feature to pass a model/llm a property details json file.
The AI assistant can then interact with a user and answer any questions they may have about a property.
Th assistant serves as a stand-in for a real estate professional!

Functions:
- 

Usage:
"""

from openai import OpenAI
import os

# Utilizes an environmental variable for your api key. will error out if not set in your system.
client = OpenAI()


# HELPER FUNCTIONS
# ---------------------------------------------------------------------

# Upload file
def upload_file(path):
    # Upload a file with an "assistants" purpose
    file = client.files.create(file=open(path, "rb"), purpose="assistants")
    return file

def create_assistant():
    assistant = client.beta.assistants.create(
        name="Math Tutor",
        instructions="You are a personal math tutor. Answer questions briefly, in a sentence or less.",
        model="gpt-4-1106-preview",
    )
    return assistant

