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

