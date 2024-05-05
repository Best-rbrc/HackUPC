import os

def list_chats(username):
    chat_files = []
    for filename in os.listdir("."):
        if filename.endswith(".chat"):
            with open(filename, "r") as file:
                participants = file.readline().strip().split(", ")
                if username in participants:
                    other_person = participants[1] if participants[0] == username else participants[0]
                    chat_files.append((filename, other_person))
    return chat_files

def start_chat(user1, user2):
    filename = f"{user1}_{user2}.chat" if user1 < user2 else f"{user2}_{user1}.chat"
    with open(filename, "a") as file:
        while True:
            message = input(f"{user1}: ")
            if message.lower() == "exit":
                break
            file.write(f"{user1}: {message}\n")
            reply = input(f"{user2}: ")
            if reply.lower() == "exit":
                break
            file.write(f"{user2}: {reply}\n")
