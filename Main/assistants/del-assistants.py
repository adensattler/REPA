"""
Script to delete all OpenAI assistants.

This script retrieves a list of assistant IDs, deletes each assistant, and confirms successful deletion.

Usage:
    - Ensure OpenAI API credentials are configured.
    - Run the script.

Note: Be cautious as this script permanently deletes assistants. 
You will have to create a new assistant before running the assistant again.

"""
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()   # Load environment variables from .env file

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_assistant_ids():
    assistants = client.beta.assistants.list(
        order="desc",
        limit="20",
    )
    return [assistant.id for assistant in assistants.data]

def get_all_vector_stores():
    vstores = client.beta.vector_stores.list(
        order="desc",
        limit="20",
    )
    return [vs.id for vs in vstores.data]


def main():
    # assistant_ids = get_assistant_ids()
    # print(f"\nList of assistant_ids: {assistant_ids}")

    # # delete each assistant
    # for id in assistant_ids:
    #     client.beta.assistants.delete(id)

    # # Confirm all assistants are deleted
    # assistant_ids = get_assistant_ids()
    # if len(assistant_ids) == 0:
    #     print("All assistants deleted successfully!\n")
    # else:
    #     print("Not all assistants were deleted. Try debugging.")


    vs_ids = get_all_vector_stores()
    print(f"\nList of vector store ids: {vs_ids}")

    # delete each assistant
    for id in vs_ids:
        client.beta.vector_stores.delete(id)
        print(f"deleted {id}")

    # Confirm all assistants are deleted
    vs_ids = get_all_vector_stores()
    if len(vs_ids) == 0:
        print("All vector stores deleted successfully!\n")
    else:
        print("Not all vector stores were deleted. Try debugging.")

if __name__ == "__main__":
    main()