from openai import OpenAI

client = OpenAI()

def get_all_assistant_ids():
    assistants = client.beta.assistants.list(
        order="desc",
        limit="20",
    )
    return [assistant.id for assistant in assistants.data]


def main():
    assistant_ids = get_all_assistant_ids()
    print(f"\nList of assistant_ids: {assistant_ids}")

    # delete each assistant
    for id in assistant_ids:
        client.beta.assistants.delete(id)

    # Confirm all assistants are deleted
    assistant_ids = get_all_assistant_ids()
    if len(assistant_ids) == 0:
        print("All assistants deleted successfully!\n")
    else:
        print("Not all assistants were deleted. Try debugging.")

if __name__ == "__main__":
    main()