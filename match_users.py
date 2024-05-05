import os

def load_user_activities():
    """
    Load all user activities from their respective files.
    
    Returns:
        dict: A dictionary where the key is the username and the value is a list of liked activities.
    """
    user_activities = {}
    for filename in os.listdir("."):
        if filename.endswith("_data.txt"):
            username = filename[:-9]  # Remove "_data.txt"
            with open(filename, "r") as file:
                liked_activities = [
                    line.strip().split(": ", 1)[1]
                    for line in file if line.startswith("Liked activity in")
                ]
            user_activities[username] = liked_activities
    return user_activities

def match_users(logged_in_user, user_activities):
    """
    Match the logged-in user with other users who like the same activities.
    
    Args:
        logged_in_user (str): The username of the logged-in user.
        user_activities (dict): The dictionary containing users and their liked activities.

    Returns:
        dict: A dictionary where the key is another username and the value is a list of common activities.
    """
    matched_users = {}
    logged_in_activities = set(user_activities.get(logged_in_user, []))

    for other_user, activities in user_activities.items():
        if other_user == logged_in_user:
            continue

        common_activities = logged_in_activities & set(activities)
        if common_activities:
            matched_users[other_user] = list(common_activities)

    return matched_users
