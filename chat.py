import os

def list_chats(user):
    """
    List all chat files involving the specified user, indicating the other participant.

    Args:
        user (str): The username to search for in the chat files.

    Returns:
        list: A list of tuples where each tuple contains the filename and the other participant.
    """
    chat_files = []
    for filename in os.listdir("."):
        if filename.startswith("chat_") and filename.endswith(".txt"):
            participants = filename[5:-4].split("_")
            if user in participants:
                other_person = participants[0] if participants[1] == user else participants[1]
                chat_files.append((filename, other_person))
    return chat_files

def start_chat(user1, user2):
    """
    Start a chat session between two users.
    Args:
        user1 (str): The name of the first user.
        user2 (str): The name of the second user.
    """
    sender = user1
    user1, user2 = sorted([user1, user2])

    chat_file = f"chat_{user1}_{user2}.txt"
    print(f"\nOpening chat between {user1} and {user2}")

    if not os.path.exists(chat_file):
        with open(chat_file, "w") as file:
            file.write(f"Chat between {user1} and {user2}\n")
            file.write("="*30 + "\n")

    while True:
        print("\nOptions:")
        print("1. Send a message")
        print("2. View chat history")
        print("3. Exit chat")

        choice = input("Choose an option (1/2/3): ").strip()

        if choice == "1":
            message = input("Enter your message: ").strip()
            with open(chat_file, "a") as file:
                file.write(f"{sender}: {message}\n")
                print("Message sent!")
        elif choice == "2":
            with open(chat_file, "r") as file:
                print("\nChat history:")
                print(file.read())
        elif choice == "3":
            print("Exiting chat...")
            break
        else:
            print("Invalid choice. Please choose 1, 2, or 3.")
