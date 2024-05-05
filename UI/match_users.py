import os

def load_user_activities():
    user_activities = {}
    for filename in os.listdir("."):
        if filename.endswith("_data.txt"):
            with open(filename, "r") as file:
                username = filename.split("_")[0]
                user_activities[username] = set(line.strip().split(": ")[-1] for line in file if "Liked activity" in line)
    return user_activities

def match_users(username, user_activities):
    matches = {}
    user_likes = user_activities.get(username, set())
    for other_user, other_likes in user_activities.items():
        if other_user != username:
            common_activities = user_likes & other_likes
            if common_activities:
                matches[other_user] = common_activities
    return matches
