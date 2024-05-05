from PyQt5.QtWidgets import QInputDialog, QMessageBox
ACTIVITY_FILE = "activities.txt"

def load_activities():
    activities = {}
    try:
        with open(ACTIVITY_FILE, "r") as file:
            for line in file:
                location, activity = line.strip().split(":", 1)
                if location in activities:
                    activities[location].append(activity)
                else:
                    activities[location] = [activity]
    except FileNotFoundError:
        pass
    return activities

def save_activity(location, activity):
    with open(ACTIVITY_FILE, "a") as file:
        file.write(f"{location}:{activity}\n")

def swipe_on_activities(username, location, liked_activities):
    """
    Save liked activities to the user's file.
    
    Args:
        username (str): The username of the current user.
        location (str): The location to explore activities for.
        liked_activities (list): The list of liked activities.
    """
    with open(f"{username}_data.txt", "a") as file:
        for liked in liked_activities:
            file.write(f"Liked activity in {location}: {liked}\n")

    print("You liked the following activities:")
    for liked in liked_activities:
        print(f"- {liked}")


def add_activity(location, activities):
    """
    Add a new activity to the specified location's activity list.
    
    Args:
        location (str): The name of the place.
        activities (list): The list of activities for the location.
    """
    with open("activities.txt", "a") as file:
        for activity in activities:
            file.write(f"{location}:{activity}\n")


def swipe_and_add_activities(username, activities):
    run = True
    while run:
        location = input("Enter the location you want to explore: ").strip()
        if location in activities:
            print(f"Exploring activities for {location}.")
            while True:
                choice = input("Do you want to swipe on activities or add a new activity or exit(swipe/add/exit)? ").lower()
                if choice == "swipe":
                    swipe_on_activities(username, location, activities[location])
                elif choice == "add":
                    add_activity(location, activities[location])
                elif choice == "exit":
                    run = False
                    break
                else:
                    print("Invalid choice.")
        else:
            choice = input(f"No activities found for {location}. Would you like to add one?(y/n)")
            if choice == "y":
                add_activity(location, [])
            run = choice != 'y'

            if not run:
                print("Thanks for stopping by. See you soon...")
                break
