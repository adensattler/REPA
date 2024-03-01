"""
Module Name: assistant_operations.py

Description:
This module serves as an EXAMPLE for how to set up and interact with an OpenAI's assistants API.

"""

from openai import OpenAI
import time
import os

# Utilizes an environmental variable for your api key. will error out if not set in your system.
client = OpenAI()

# Here is an alternative:
# client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "<your OpenAI API key if not set as env var>"))

'''
completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
  ]
)

print(completion.choices[0].message)
'''


# HELPER FUNCTIONS
# ---------------------------------------------------------------------
# Creates and returns an OpenAI File object 
def upload_file(path):
    # Upload a file with an "assistants" purpose
    file = client.files.create(file=open(path, "rb"), purpose="assistants")
    return file

# Creates and retuns an OpenAI Assistant object
def create_assistant():
    assistant = client.beta.assistants.create(
        name="Math Tutor",
        instructions="You are a personal math tutor. Answer questions briefly, in a sentence or less.",
        model="gpt-4-1106-preview",
    )
    return assistant

# Creates a thread and then calls on that thread to run with a provided input
def create_thread_and_run(user_input):
    #returns a Thread object and a Run object
    thread = client.beta.threads.create()
    run = submit_message(MATH_ASSISTANT_ID, thread, user_input)
    return thread, run

def submit_message(assistant_id, thread, user_message):
    ''' 
    Submits a message to an specific conversation thread and runs that thread
    Returns the corresponding Run object 
    '''
    client.beta.threads.messages.create(thread_id=thread.id, role="user", content=user_message)
    return client.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistant_id)

# Waits for a run to complete before proceeding
def wait_on_run(run, thread):
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run

# Returns a list of OpenAI Message objects for a thread
def get_response(thread):
    return client.beta.threads.messages.list(thread_id=thread.id, order="asc")

# Pretty prints the messages in a more readable format
def pretty_print(messages):
    print("# Messages")
    for m in messages:
        print(f"{m.role}: {m.content[0].text.value}")
    print()





# DRIVER
# ------------------------------------------------------------------------------------------
assistant = create_assistant()
MATH_ASSISTANT_ID = assistant.id  # or a hard-coded ID like "asst-..."

# Create multiple threads that handle multiple asynchronous 
thread1, run1 = create_thread_and_run("I need to solve the equation `3x + 11 = 14`. Can you help me?")
thread2, run2 = create_thread_and_run("Could you explain linear algebra to me?")
thread3, run3 = create_thread_and_run("I don't like math. What can I do?")

# Now all Runs are executing...

# Wait for Run 1
run1 = wait_on_run(run1, thread1)
pretty_print(get_response(thread1))

# Wait for Run 2
run2 = wait_on_run(run2, thread2)
pretty_print(get_response(thread2))

# Wait for Run 3
run3 = wait_on_run(run3, thread3)
pretty_print(get_response(thread3))

# Thank our assistant on Thread 3 :)
run4 = submit_message(MATH_ASSISTANT_ID, thread3, "Thank you!")
run4 = wait_on_run(run4, thread3)
pretty_print(get_response(thread3))









# THIS IS ME TRYING TO GET SOMETHING WORKING ON MY OWN
# Run assistant
def run_assistant(thread):
    # Retrieve the Assistant
    assistant = client.beta.assistants.retrieve(assistant.id)

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
    print(f"Generated message: {new_message}")
    return new_message

