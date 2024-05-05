import auth
import travel
import match_users as match
import chat
import blackjack

def main():
    """
    Main function to run the user authentication application.
    Allows the user to choose between registering, logging in, exploring activities, and matching with others.
    """
    users = auth.load_users()
    activities = travel.load_activities()

    authenticated = False
    username = None
    while not authenticated:
        print("\nWelcome to the Travel App!")
        print("1. Register")
        print("2. Login")
        choice = input("Please select an option (1/2): ").strip()

        if choice == "1":
            auth.register_user(users)
        elif choice == "2":
            username = auth.login_user(users)
            authenticated = username is not None
        else:
            print("Invalid choice. Please select 1 or 2.")

    while True:
        print(f"\nWelcome, {username}!")
        print("1. Explore Activities")
        print("2. Match with Others")
        print("3. Chats")
        print("4. Gambling")
        print("5. Exit")
        choice = input("Please select an option (1/2/3/4/5): ").strip()

        if choice == "1":
            travel.swipe_and_add_activities(username, activities)
        elif choice == "2":
            user_activities = match.load_user_activities()
            matched_users = match.match_users(username, user_activities)
            if matched_users:
                print(f"\nMatching users who like the same activities as you:")
                user_list = list(matched_users.items())
                for i, (other_user, common_activities) in enumerate(user_list):
                    print(f"{i+1}: {other_user} - common activities: {', '.join(common_activities)}")

                contact_choice = input("Do you want to contact any of them? (y/n): ").strip().lower()
                if contact_choice == "y":
                    user_index = input("Enter the index of the user you want to contact: ").strip()
                    if user_index.isdigit():
                        user_index = int(user_index)-1
                        if 0 <= user_index < len(user_list):
                            selected_user, selected_activities = user_list[user_index]
                            chat.start_chat(username, selected_user)
                        else:
                            print("Invalid index")
                    else:
                        print("Invalid input. Please enter a valid index.")
                elif contact_choice == "n":
                    continue
                else:
                    print("Invalid input.")
            else:
                print(f"No matches found for {username}.")
        elif choice == "3":
            chat_files = chat.list_chats(username)
            if chat_files:
                print("\nAvailable chats:")
                for i, (filename, other_person) in enumerate(chat_files, start=1):
                    print(f"{i}: Chat between you and {other_person}")
                chat_choice = input("Enter the index of the chat you want to open: ").strip()
                if chat_choice.isdigit():
                    chat_index = int(chat_choice) - 1
                    if 0 <= chat_index < len(chat_files):
                        filename, other_user = chat_files[chat_index]
                        chat.start_chat(username, other_user)
                    else:
                        print("Invalid index")
                else:
                    print("Invalid input. Please enter a valid index.")
            else:
                print("No chats found.")
        elif choice == "4":
            blackjack.blackjack()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()
